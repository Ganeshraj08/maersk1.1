"""
ATLAS Maritime Intelligence — FastAPI Backend
Provides all data endpoints and SSE-based agent streaming for the React frontend.
"""
import asyncio
import json
import random
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

app = FastAPI(
    title="ATLAS Maritime Intelligence API",
    version="3.0.0",
    description="Real-time maritime container repositioning intelligence platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Data layer (mirrors frontend maritimeData.js) ────────────────────────────

ATLAS_PORTS = {
    "SGP":  {"id":"SGP",  "name":"Singapore",        "country":"Singapore",   "region":"SEA",   "lat":1.29,  "lon":103.83,"berths":55, "surplusTEU":2847, "invStatus":"Surplus",  "depot":True},
    "VNCMT":{"id":"VNCMT","name":"Ho Chi Minh City", "country":"Vietnam",     "region":"SEA",   "lat":10.77, "lon":106.70,"berths":18, "surplusTEU":-1247,"invStatus":"Shortage", "depot":False},
    "PKG":  {"id":"PKG",  "name":"Port Klang",        "country":"Malaysia",    "region":"SEA",   "lat":3.00,  "lon":101.40,"berths":32, "surplusTEU":1890, "invStatus":"Surplus",  "depot":True},
    "SHA":  {"id":"SHA",  "name":"Shanghai",          "country":"China",       "region":"NEAC",  "lat":31.23, "lon":121.47,"berths":120,"surplusTEU":5420, "invStatus":"Surplus",  "depot":True},
    "RTM":  {"id":"RTM",  "name":"Rotterdam",         "country":"Netherlands", "region":"NWEUR", "lat":51.90, "lon":4.48,  "berths":95, "surplusTEU":6100, "invStatus":"Surplus",  "depot":True},
    "LAX":  {"id":"LAX",  "name":"Los Angeles / LB",  "country":"USA",         "region":"NAWC",  "lat":33.74, "lon":-118.27,"berths":70,"surplusTEU":3850, "invStatus":"Surplus",  "depot":True},
    "AEDJB":{"id":"AEDJB","name":"Jebel Ali Dubai",  "country":"UAE",         "region":"MEA",   "lat":24.97, "lon":55.07, "berths":70, "surplusTEU":4200, "invStatus":"Surplus",  "depot":True},
    "INBOM":{"id":"INBOM","name":"Mumbai JNPT",       "country":"India",       "region":"IOSC",  "lat":18.93, "lon":72.93, "berths":21, "surplusTEU":-2100,"invStatus":"Shortage", "depot":True},
    "BDCTG":{"id":"BDCTG","name":"Chittagong",        "country":"Bangladesh",  "region":"IOSC",  "lat":22.33, "lon":91.83, "berths":12, "surplusTEU":-1870,"invStatus":"Shortage", "depot":False},
    "LCCHG":{"id":"LCCHG","name":"Laem Chabang",      "country":"Thailand",    "region":"SEA",   "lat":13.08, "lon":100.88,"berths":22, "surplusTEU":1240, "invStatus":"Surplus",  "depot":False},
    "DEHAM":{"id":"DEHAM","name":"Hamburg",           "country":"Germany",     "region":"NWEUR", "lat":53.55, "lon":9.98,  "berths":65, "surplusTEU":2890, "invStatus":"Surplus",  "depot":True},
    "NLAMF":{"id":"NLAMF","name":"Amsterdam",         "country":"Netherlands", "region":"NWEUR", "lat":52.38, "lon":4.90,  "berths":20, "surplusTEU":507,  "invStatus":"Surplus",  "depot":True},
}

FLEET_VESSELS = [
    {"id":"MSC-AURORA",  "name":"MSC AURORA",      "type":"Neo-Panamax", "capacityTEU":14000,"cargoPct":78,"emptyTEU":3080,"fromPort":"SHA",  "toPort":"VNCMT","status":"En Route","eta":"Apr 14","speed":18.2,"lat":20.5, "lon":115.2},
    {"id":"EVER-GOLDEN", "name":"EVER GOLDEN",     "type":"ULCV",        "capacityTEU":20000,"cargoPct":82,"emptyTEU":3600,"fromPort":"PKG",  "toPort":"RTM",  "status":"Departed","eta":"Apr 17","speed":19.5,"lat":3.8,  "lon":98.5},
    {"id":"MAERSK-ELENA","name":"MAERSK ELENA",    "type":"Triple-E",    "capacityTEU":18000,"cargoPct":91,"emptyTEU":1620,"fromPort":"RTM",  "toPort":"SHA",  "status":"Loading", "eta":"Apr 19","speed":0,   "lat":51.9, "lon":4.48},
    {"id":"CMA-LIBERTY", "name":"CMA CGM LIBERTY", "type":"Panamax",     "capacityTEU":9000, "cargoPct":65,"emptyTEU":3150,"fromPort":"SGP",  "toPort":"INBOM","status":"En Route","eta":"Apr 15","speed":17.0,"lat":6.5,  "lon":82.3},
    {"id":"OOCL-TIANJIN","name":"OOCL TIANJIN",    "type":"New Panamax", "capacityTEU":12000,"cargoPct":74,"emptyTEU":3120,"fromPort":"KRPUS","toPort":"LAX",  "status":"En Route","eta":"Apr 16","speed":20.1,"lat":37.0, "lon":168.4},
    {"id":"HMM-DANUBE",  "name":"HMM DANUBE",      "type":"Feeder",      "capacityTEU":4800, "cargoPct":55,"emptyTEU":2160,"fromPort":"LCCHG","toPort":"SGP",  "status":"Anchored","eta":"Apr 13","speed":0,   "lat":10.5, "lon":104.1},
]

DEMAND_SCENARIOS = {
    "vietnam_surge": {
        "id":"vietnam_surge","name":"Vietnam Manufacturing Surge",
        "portId":"VNCMT","portName":"Ho Chi Minh City","region":"Vietnam – HCMC",
        "teuRequired":847,"containerType":"40ft Dry","destination":"Ho Chi Minh City",
        "requiredBy":"April 17","slaWindow":"72 hours","urgency":"CRITICAL",
        "confidence":94,"customer":"Vinamih Vietnam","sapRef":"VNM-2026-0047",
        "prediction":{"demand":"800–900 TEUs","region":"Vietnam","window":"April 14–16","confidence":94},
    },
    "bangladesh_crisis": {
        "id":"bangladesh_crisis","name":"Bangladesh Garment Export Crisis",
        "portId":"BDCTG","portName":"Chittagong","region":"Bangladesh",
        "teuRequired":620,"containerType":"20ft Dry","destination":"Chittagong",
        "requiredBy":"April 20","slaWindow":"96 hours","urgency":"HIGH",
        "confidence":87,"customer":"DBL Group","sapRef":"BGD-2026-0089",
        "prediction":{"demand":"580–650 TEUs","region":"Bangladesh","window":"April 16–20","confidence":87},
    },
}

# ─── Agent log generators ────────────────────────────────────────────────────

async def _run_demand_agent(scenario: dict):
    logs = [
        (0.3,  "DEMAND", "#00B4D8", "Initialising Demand Sensing Agent v2.4..."),
        (0.7,  "DEMAND", "#00B4D8", f"Connecting to PortSight™ Live feed — {scenario['portName']}..."),
        (1.1,  "DATA",   "#42B4E6", "Vietnam PMI 54.2 → export signal STRONG (+18% MoM)"),
        (1.5,  "DATA",   "#42B4E6", f"SAP PO scan: 3 new orders totalling {scenario['teuRequired']} TEU detected"),
        (1.9,  "WEATHER","#F59E0B", "Typhoon Malakas track north — 14-day port window CLEAR"),
        (2.3,  "AIS",    "#42B4E6", "MSC AURORA: SHA→VNCMT, ETA Apr 14, 3,080 empty TEU on board"),
        (2.7,  "RESULT", "#10B981", f"DEMAND CONFIRMED: {scenario['prediction']['demand']}, {scenario['region']}, confidence {scenario['confidence']}%"),
    ]
    for delay, prefix, color, text in logs:
        await asyncio.sleep(delay)
        yield {"agent":"demand","prefix":f"[{prefix}]","color":color,"text":text,"time":datetime.now().strftime("%H:%M:%S")}

async def _run_supply_agent(scenario: dict):
    logs = [
        (0.2,  "SUPPLY",   "#8B5CF6", "Initialising Supply Finder Agent v1.9..."),
        (0.6,  "SUPPLY",   "#8B5CF6", "Scanning 68 depot locations in SEA region..."),
        (1.0,  "SCAN",     "#42B4E6", "SGP: 2,847 TEU listed — cross-checking AIS vessel feed..."),
        (1.4,  "CONFLICT", "#EF4444", "SGP REJECTED: MSC AURORA offload Apr 14 = only 263 TEU net available"),
        (1.8,  "SCAN",     "#42B4E6", "PKG: 890 TEU confirmed — no conflicting arrivals in window"),
        (2.2,  "MATCH",    "#10B981", "PKG SELECTED: EVER GOLDEN departs Apr 15 06:00 — perfect window"),
        (2.6,  "RESULT",   "#10B981", "3 supply options ranked: PKG(91%) > LCCHG(82%) > SGP(23% real SLA)"),
    ]
    for delay, prefix, color, text in logs:
        await asyncio.sleep(delay)
        yield {"agent":"supply","prefix":f"[{prefix}]","color":color,"text":text,"time":datetime.now().strftime("%H:%M:%S")}

async def _run_optimization_agent(scenario: dict):
    logs = [
        (0.2, "OPTIM",  "#F97316", "Initialising Optimization Agent v3.1 (XGBoost ensemble)..."),
        (0.6, "OPTIM",  "#F97316", "Running cost/SLA/carbon multi-objective optimisation..."),
        (1.0, "CALC",   "#42B4E6", "PKG route: cost $215/TEU, 2.8 days, CO₂ -23%, SLA 91%"),
        (1.4, "CALC",   "#42B4E6", "Co-load opportunity: Philips 507 TEU AMS→SGP→PKG detected"),
        (1.8, "COLOAD", "#10B981", "Co-load net saving: $286,455 vs empty repositioning (-$106,470)"),
        (2.2, "RESULT", "#10B981", "RECOMMENDATION: Port Klang via EVER GOLDEN + Philips co-load"),
    ]
    for delay, prefix, color, text in logs:
        await asyncio.sleep(delay)
        yield {"agent":"optimization","prefix":f"[{prefix}]","color":color,"text":text,"time":datetime.now().strftime("%H:%M:%S")}

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"service":"ATLAS Maritime Intelligence API","version":"3.0.0","status":"operational"}

@app.get("/api/health")
def health():
    return {"status":"ok","timestamp":datetime.now().isoformat()}

@app.get("/api/ports")
def get_ports(region: Optional[str] = None, status: Optional[str] = None):
    ports = list(ATLAS_PORTS.values())
    if region and region != "All Regions":
        ports = [p for p in ports if p["region"] == region]
    if status and status != "All Status":
        ports = [p for p in ports if p["invStatus"] == status]
    return ports

@app.get("/api/ports/{port_id}")
def get_port(port_id: str):
    port = ATLAS_PORTS.get(port_id.upper())
    if not port:
        return JSONResponse({"error":"Port not found"}, status_code=404)
    return port

@app.get("/api/fleet")
def get_fleet():
    # Simulate live position drift
    vessels = []
    for v in FLEET_VESSELS:
        vessel = dict(v)
        if v["speed"] > 0:
            vessel["lat"] = round(v["lat"] + random.uniform(-0.05, 0.05), 3)
            vessel["lon"] = round(v["lon"] + random.uniform(-0.05, 0.05), 3)
        vessels.append(vessel)
    return vessels

@app.get("/api/scenarios")
def get_scenarios():
    return list(DEMAND_SCENARIOS.values())

@app.get("/api/dashboard")
def get_dashboard():
    return {
        "kpis": {
            "emptyRepositioningCost": {"value":"$1.47B","change":-8.3,"label":"Empty Repositioning Cost"},
            "slaAdherence":           {"value":"82.4%", "change":+4.1, "label":"SLA Adherence"},
            "manualTimeline":         {"value":"68 hrs","change":0,    "label":"Manual Repositioning Time"},
            "decisionTime":           {"value":"4.2s",  "change":-99,  "label":"AI Decision Time"},
            "activeAlerts":           {"value":1,       "change":0,    "label":"Active Notifications"},
            "coLoadSavings":          {"value":"$286K", "change":0,    "label":"Co-load Savings"},
        },
        "network": {
            "ports":524,"countries":130,"vessels":737,"depots":68,"emptyTEUs":1_247_000
        }
    }

@app.get("/api/agents/stream")
async def stream_agents(scenario_id: str = "vietnam_surge"):
    """SSE endpoint: streams all 3 agents sequentially."""
    scenario = DEMAND_SCENARIOS.get(scenario_id, DEMAND_SCENARIOS["vietnam_surge"])

    async def generator():
        yield {"event":"start","data":json.dumps({"scenario":scenario_id})}

        # Demand agent
        yield {"event":"agent_start","data":json.dumps({"agent":"demand"})}
        async for log in _run_demand_agent(scenario):
            yield {"event":"log","data":json.dumps(log)}
        yield {"event":"agent_done","data":json.dumps({"agent":"demand"})}

        await asyncio.sleep(0.3)

        # Supply agent
        yield {"event":"agent_start","data":json.dumps({"agent":"supply"})}
        async for log in _run_supply_agent(scenario):
            yield {"event":"log","data":json.dumps(log)}
        yield {"event":"agent_done","data":json.dumps({"agent":"supply"})}

        await asyncio.sleep(0.3)

        # Optimization agent
        yield {"event":"agent_start","data":json.dumps({"agent":"optimization"})}
        async for log in _run_optimization_agent(scenario):
            yield {"event":"log","data":json.dumps(log)}
        yield {"event":"agent_done","data":json.dumps({"agent":"optimization"})}

        yield {"event":"complete","data":json.dumps({"status":"success","recommendation":"PKG via EVER GOLDEN"})}

    return EventSourceResponse(generator())

@app.post("/api/approve")
async def approve_repositioning(scenario_id: str = "vietnam_surge"):
    """Approve and execute repositioning — returns SAP order details."""
    scenario = DEMAND_SCENARIOS.get(scenario_id, DEMAND_SCENARIOS["vietnam_surge"])
    return {
        "approved":True,
        "timestamp":datetime.now().isoformat(),
        "sapOrder":{
            "id":"TM-2026-04729",
            "vessel":"EVER GOLDEN",
            "from":"PKG","to":scenario["portId"],
            "teu":scenario["teuRequired"],
            "eta":"April 18",
            "revenue_usd":199_985,
        },
        "message":"SAP TM order created. Vessel slot confirmed. Customer notified."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
