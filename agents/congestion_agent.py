"""
TCS ATLAS — Congestion Agent
Calculates port congestion risk based on approved reroutes.
If multiple repositioning decisions funnel to the same port,
the congestion score rises — modelling finite berth contention.
"""
from config import PORT_BERTHS, ATLAS_PORTS


class CongestionAgent:
    """
    Agent D — Port Congestion Risk Scorer.

    Logic
    -----
    congestion_score(port) = (approved_reroutes_to_port / available_berths) * 100
    Risk levels:
        Low    0–30  — Normal operations
        Medium 31–60 — Monitor closely
        High   61–80 — Berth contention likely; delay vessels
        Critical >80 — Recommend alternative port
    """

    RISK_THRESHOLDS = {
        "Low":      (0,  30),
        "Medium":   (31, 60),
        "High":     (61, 80),
        "Critical": (81, 100),
    }

    def run(self, approved_routes: list, vessel_plans: list | None = None) -> dict:
        """
        Parameters
        ----------
        approved_routes : list of dicts — each with 'port_id' key
        vessel_plans    : list of dicts — optional, adds vessel-level context

        Returns
        -------
        dict {
            "port_scores":   {port_id: {"score": float, "risk": str, "reroutes": int}},
            "hotspots":      [port_ids with High/Critical risk],
            "stream_lines":  list[str],
            "recommendation": str,
        }
        """
        # Count reroutes per port
        reroute_counts: dict[str, int] = {}
        for route in approved_routes:
            pid = route.get("port_id", "")
            # Handle combined ports like "PKG+SGP"
            for p in pid.split("+"):
                p = p.strip()
                if p:
                    reroute_counts[p] = reroute_counts.get(p, 0) + 1

        # Also count vessel plan diversions if provided
        if vessel_plans:
            for vp in vessel_plans:
                new_port = vp.get("new_dest_port", "")
                if new_port and vp.get("diverted", False):
                    reroute_counts[new_port] = reroute_counts.get(new_port, 0) + 1

        # Score each port
        port_scores: dict[str, dict] = {}
        for pid, pdata in ATLAS_PORTS.items():
            berths   = PORT_BERTHS.get(pid, 4)
            reroutes = reroute_counts.get(pid, 0)
            score    = min(100.0, (reroutes / berths) * 100)
            risk     = self._risk_level(score)
            port_scores[pid] = {
                "score":    round(score, 1),
                "risk":     risk,
                "reroutes": reroutes,
                "berths":   berths,
                "name":     pdata["name"],
            }

        hotspots = [p for p, d in port_scores.items() if d["risk"] in ("High", "Critical")]

        stream_lines = [
            "[ATLAS CONGESTION AGENT] Analysing port berth utilisation...",
            f"Approved reroutes tracked : {len(approved_routes)}",
            f"Ports in network          : {len(ATLAS_PORTS)}",
            "",
        ]

        # Report top congested ports
        sorted_ports = sorted(port_scores.items(), key=lambda x: x[1]["score"], reverse=True)
        for pid, data in sorted_ports[:6]:
            if data["score"] > 0:
                risk_icon = "🔴" if data["risk"] == "Critical" else ("🟠" if data["risk"] == "High" else ("🟡" if data["risk"] == "Medium" else "🟢"))
                stream_lines.append(
                    f"  {risk_icon} {data['name']:28s} Score: {data['score']:5.1f}  "
                    f"Reroutes: {data['reroutes']}  Berths: {data['berths']}  Risk: {data['risk']}"
                )

        if hotspots:
            stream_lines.append(f"\n⚠ HOTSPOTS DETECTED: {', '.join(ATLAS_PORTS[p]['name'] for p in hotspots if p in ATLAS_PORTS)}")
            recommendation = f"Redirect future bookings away from {', '.join(hotspots[:2])} — berth contention likely."
        else:
            stream_lines.append("\n✓ No critical congestion detected. Network operating normally.")
            recommendation = "No action required. Monitor as additional approvals are processed."

        stream_lines.append(f"\nRECOMMENDATION: {recommendation}")

        return {
            "port_scores":     port_scores,
            "hotspots":        hotspots,
            "stream_lines":    stream_lines,
            "recommendation":  recommendation,
        }

    @staticmethod
    def _risk_level(score: float) -> str:
        if score > 80:  return "Critical"
        if score > 60:  return "High"
        if score > 30:  return "Medium"
        return "Low"

    @staticmethod
    def compute_vessel_new_plan(vessel: dict, approved_route: dict,
                                demand_port_id: str, extra_delay_days: float = 0.3) -> dict:
        """
        Given an approved repositioning route for a vessel, compute the
        new voyage plan: updated route list, new ETA, diversion reason.
        """
        orig_route = vessel["original_route"][:]
        orig_eta   = vessel["original_eta_days"]

        # Insert demand port into the route
        dest_idx = len(orig_route) - 1
        if demand_port_id not in orig_route:
            new_route = orig_route[:dest_idx] + [demand_port_id] + [orig_route[dest_idx]]
        else:
            new_route = orig_route[:]

        new_eta = round(orig_eta + extra_delay_days + 0.5, 1)

        return {
            "vessel_id":       vessel["id"],
            "vessel":          vessel["vessel"],
            "original_route":  " → ".join(
                ATLAS_PORTS.get(p, {}).get("name", p).split("(")[0].strip()
                for p in orig_route
            ),
            "new_route":       " → ".join(
                ATLAS_PORTS.get(p, {}).get("name", p).split("(")[0].strip()
                for p in new_route
            ),
            "original_eta":    f"{orig_eta:.1f} days",
            "new_eta":         f"{new_eta:.1f} days",
            "eta_delta":       f"+{new_eta - orig_eta:.1f}d",
            "diversion_reason": f"Empty container delivery to {ATLAS_PORTS.get(demand_port_id, {}).get('name', demand_port_id)} — {approved_route.get('teu', 847):,} TEUs offloaded",
            "diverted":        True,
            "new_dest_port":   demand_port_id,
            "orig_route_list": orig_route,
            "new_route_list":  new_route,
            "from_lat":        ATLAS_PORTS.get(vessel["from_port"], {}).get("lat", 0),
            "from_lon":        ATLAS_PORTS.get(vessel["from_port"], {}).get("lon", 0),
            "orig_dest_lat":   ATLAS_PORTS.get(orig_route[-1], {}).get("lat", 0),
            "orig_dest_lon":   ATLAS_PORTS.get(orig_route[-1], {}).get("lon", 0),
            "new_dest_lat":    ATLAS_PORTS.get(demand_port_id, {}).get("lat", 0),
            "new_dest_lon":    ATLAS_PORTS.get(demand_port_id, {}).get("lon", 0),
        }
