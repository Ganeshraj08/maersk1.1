"""
app.py — TCS ATLAS v3.0  |  Maritime Control Tower
TCS Crystallus × A.P. Moller-Maersk
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time, html as _h
from datetime import datetime

from config import (
    SYSTEM_NAME, SYSTEM_FULL, CLIENT_NAME, PLATFORM_NAME, ATLAS_VERSION,
    NETWORK_PORTS, NETWORK_COUNTRIES, TOTAL_VESSELS, DEPOT_LOCATIONS, GLOBAL_EMPTY_TEUS,
    MAERSK_DARK, MAERSK_BLUE, MAERSK_LIGHT, MAERSK_TEAL,
    BG_PAGE, BG_CARD, BG_SIDEBAR, BG_ALT,
    TEXT_H, TEXT_BODY, TEXT_MUTED, TEXT_CAPTION, TEXT_INV,
    BORDER, BORDER_STRONG,
    SUCCESS, WARNING, DANGER, INFO,
    USE_CASES,
    ATLAS_PORTS, DEPOT_INVENTORY, FLEET_VESSELS, CUSTOMERS,
    DEMAND_SCENARIOS, BASELINE_STATIC,
    ROUTE_OPTIONS_BASE, WHATIF_SCENARIOS, WEIGHT_PROFILES, IMPACT, DEMAND_ALERTS,
    MONITOR_PORTS, CONTAINER_INVENTORY, DATA_SOURCES, NEWS_ITEMS,
)
from atlas_agents import DemandSensingAgent, SupplyFinderAgent, OptimizationAgent, CongestionAgent

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TCS ATLAS — Maritime Control Tower",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LOGO_TCS    = "https://i.pinimg.com/736x/36/04/03/36040350b2a262a4015440374807b4d6.jpg"
LOGO_MAERSK = "https://i.pinimg.com/1200x/aa/a2/45/aaa245759726ab04e968b9bff4981a52.jpg"

# ══════════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Hide ALL Streamlit chrome ── */
header,header[data-testid="stHeader"],[data-testid="stHeader"],
[data-testid="stToolbar"],[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],[data-testid="stStatusWidget"],
[data-testid="stDecoration"],#MainMenu,footer,[data-testid="stFooter"],
.viewerBadge_container__1QSob,.viewerBadge_link__qRIco {{
    display:none!important;height:0!important;overflow:hidden!important;
}}

/* ── Global reset & font scale ── */
html{{font-size:16.5px!important;}}
html,body,.stApp,[data-testid="stAppViewContainer"]{{
    background-color:{BG_PAGE}!important;
    font-family:'Segoe UI',Arial,sans-serif!important;
    color:{TEXT_BODY}!important;
}}
.block-container{{
    padding-top:0!important;padding-bottom:2rem!important;
    padding-left:2rem!important;padding-right:2rem!important;
    max-width:1440px!important;
}}
[data-testid="stSidebar"]{{display:none!important;}}
h1,h2,h3,h4,h5,h6{{color:{TEXT_H}!important;font-family:'Segoe UI',Arial,sans-serif!important;}}
.stMarkdown p,div.stMarkdown,[data-testid="stText"],
[data-testid="stCaptionContainer"]{{color:{TEXT_BODY}!important;}}
label,.stSelectbox label,.stRadio label,.stCheckbox label{{
    color:{TEXT_BODY}!important;font-size:0.9rem!important;
}}

/* ── Widgets ── */
[data-baseweb="select"] *,[data-baseweb="select"] div{{
    color:{TEXT_BODY}!important;background-color:{BG_CARD}!important;
    border-color:{BORDER}!important;font-size:0.9rem!important;
}}
[data-baseweb="input"] input{{color:{TEXT_BODY}!important;background:{BG_CARD}!important;}}
[data-testid="stMetricValue"]{{color:{TEXT_H}!important;font-weight:700!important;font-size:1.5rem!important;}}
[data-testid="stMetricLabel"]{{color:{TEXT_MUTED}!important;font-size:0.82rem!important;}}
[data-testid="stMetricDelta"]{{font-size:0.82rem!important;}}

/* ── Buttons ── */
.stButton>button{{
    background-color:{MAERSK_BLUE}!important;color:#fff!important;
    border:none!important;border-radius:6px!important;
    font-weight:600!important;padding:0.5rem 1.4rem!important;
    font-size:0.9rem!important;transition:all 0.2s!important;
    letter-spacing:0.02em!important;
}}
.stButton>button:hover{{background-color:{MAERSK_DARK}!important;transform:translateY(-1px)!important;}}
.stButton>button:disabled{{
    background-color:{BORDER}!important;color:{TEXT_MUTED}!important;cursor:not-allowed!important;
    transform:none!important;
}}

/* ── SC Sub-navbar (radio as tabs) ── */
/* FIX 1: hardcode text/bg so tabs are always readable regardless of theme vars */
div[data-testid="stRadio"]>label{{display:none!important;}}
div[data-testid="stRadio"] [role="radiogroup"]{{
    display:flex!important;gap:0!important;
    border-bottom:2px solid #CBD5E1!important;
    flex-wrap:nowrap!important;
    background:{BG_ALT}!important;
    border-radius:8px 8px 0 0!important;
    padding:0.3rem 0.5rem 0 0.5rem!important;
    box-shadow:0 2px 6px rgba(0,36,61,0.06)!important;
}}
div[data-testid="stRadio"] [role="radiogroup"] label{{
    display:flex!important;align-items:center!important;
    padding:0.55rem 1.1rem!important;
    border-radius:6px 6px 0 0!important;
    cursor:pointer!important;font-size:0.88rem!important;
    font-weight:500!important;color:#000000!important;
    border:1px solid transparent!important;
    border-bottom:none!important;
    transition:all 0.15s!important;margin-bottom:-2px!important;
    white-space:nowrap!important;
}}
div[data-testid="stRadio"] [role="radiogroup"] label:hover{{
    color:#000000!important;background:#EFF6FF!important;
}}
div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked){{
    background:#FFFFFF!important;color:{MAERSK_BLUE}!important;
    border-color:#CBD5E1!important;border-bottom:3px solid {MAERSK_BLUE}!important;
    font-weight:700!important;
}}
div[data-testid="stRadio"] [role="radiogroup"] label input{{display:none!important;}}
div[data-testid="stRadio"] [role="radiogroup"] label p{{
    margin:0!important;color:#000000!important;font-size:0.88rem!important;
    font-weight:inherit!important;
}}
div[data-testid="stRadio"] [role="radiogroup"] label span{{
    color:#000000!important;
}}

/* ── Cards ── */
.ent-card{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;
    padding:1.25rem;box-shadow:0 2px 8px rgba(0,36,61,0.07);margin-bottom:0.8rem;
}}
.kpi-tile{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;
    padding:0.95rem 1rem;text-align:center;
    box-shadow:0 1px 4px rgba(0,36,61,0.05);
}}
.sec-header{{
    font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
    text-transform:uppercase;color:{TEXT_MUTED};
    border-bottom:2px solid {MAERSK_BLUE};
    padding-bottom:0.35rem;margin-bottom:0.9rem;display:inline-block;
}}

/* ── Agent terminal ── */
.agent-terminal{{
    background:#0D1117;border-radius:8px;
    padding:1rem 1.2rem;max-height:440px;overflow-y:auto;
    line-height:1.7;border:1px solid #21262D;
    font-family:'Cascadia Code','Fira Code','Courier New',monospace;
    font-size:0.78rem;
}}

/* ── Reasoning block ── */
.reasoning-block{{
    background:{BG_ALT};border-left:3px solid {MAERSK_BLUE};
    padding:0.75rem 1rem;border-radius:0 6px 6px 0;
    margin:0.3rem 0;font-size:0.88rem;color:{TEXT_BODY};line-height:1.55;
}}
.reasoning-label{{
    font-size:0.7rem;font-weight:700;text-transform:uppercase;
    color:{MAERSK_BLUE};letter-spacing:0.07em;margin-bottom:0.4rem;
}}

/* ── Table ── */
.ent-table{{width:100%;border-collapse:collapse;font-size:0.87rem;}}
.ent-table th{{
    background:{MAERSK_DARK};color:{TEXT_INV};
    padding:0.5rem 0.75rem;text-align:left;
    font-weight:600;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.05em;
}}
.ent-table td{{padding:0.5rem 0.75rem;border-bottom:1px solid {BORDER};color:{TEXT_BODY};}}
.ent-table tr:hover td{{background:{BG_ALT};}}
.rank-1 td:first-child{{border-left:3px solid {SUCCESS};}}
.rank-2 td:first-child{{border-left:3px solid {WARNING};}}
.rank-3 td:first-child{{border-left:3px solid {DANGER};}}

/* ── Badges ── */
.badge-live{{background:{SUCCESS};color:#fff;border-radius:12px;padding:2px 10px;font-size:0.7rem;font-weight:700;}}
.badge-dev{{background:#6366F1;color:#fff;border-radius:12px;padding:2px 10px;font-size:0.7rem;font-weight:700;}}
.badge-critical{{background:{DANGER};color:#fff;border-radius:4px;padding:2px 8px;font-size:0.72rem;font-weight:700;}}
.badge-high{{background:{WARNING};color:#fff;border-radius:4px;padding:2px 8px;font-size:0.72rem;font-weight:700;}}

/* ── News ticker ── */
.news-ticker{{
    background:{MAERSK_DARK};color:{TEXT_INV};padding:0.4rem 1rem;
    border-radius:4px;font-size:0.82rem;font-weight:500;
    display:flex;align-items:center;gap:0.7rem;
}}

/* ── Comparison tiles ── */
.before-tile{{background:#FFF8F0;border:1px solid #F59E0B;border-top:3px solid {WARNING};border-radius:8px;padding:0.9rem;text-align:center;}}
.after-tile{{background:#F0FFF4;border:1px solid #22C55E;border-top:3px solid {SUCCESS};border-radius:8px;padding:0.9rem;text-align:center;}}

/* ── Plotly ── */
.js-plotly-plot .plotly .main-svg{{background:transparent!important;}}

/* ── FIX 5: Expander (What-If) — always readable text + hover ── */
[data-testid="stExpander"]{{
    background:#FFFFFF!important;border:1px solid {BORDER}!important;
    border-radius:8px!important;margin-bottom:0.5rem!important;
}}
[data-testid="stExpander"] summary{{
    color:#1E293B!important;font-weight:600!important;font-size:0.9rem!important;
    background:#F8FAFC!important;border-radius:8px!important;
    padding:0.6rem 0.9rem!important;
}}
[data-testid="stExpander"] summary:hover{{
    background:#EFF6FF!important;color:{MAERSK_BLUE}!important;
    cursor:pointer!important;
}}
[data-testid="stExpander"] [data-testid="stExpanderDetails"]{{
    background:#FFFFFF!important;color:#1E293B!important;
    padding:0.8rem 0.5rem!important;
}}
[data-testid="stExpander"] .ent-table td{{
    color:#1E293B!important;background:#FFFFFF!important;
}}
[data-testid="stExpander"] .ent-table tr:hover td{{
    background:#F1F5F9!important;
}}
[data-testid="stExpander"] .ent-table th{{
    background:{MAERSK_DARK}!important;color:#FFFFFF!important;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def _init_state():
    """Initialize session state variables.
    
    Uses state-based routing: no navigate_to_console flag needed.
    All navigation is driven by sc_tab state variable and button clicks.
    """
    for k, v in {
        "page": "home",
        "sc_tab": "overview",
        "scenario_key": "vietnam_surge",
        "weight_profile": "Balanced",
        "console_phase": "setup",   # "setup" | "running" | "complete" | "approved"
        "demand_result": None,
        "supply_result": None,
        "opt_result": None,
        "approved_route": None,
        "news_idx": 0,
        "terminal_lines": [],       # Persist terminal output across phases
        "active_alert": None,
        "alert_timestamp": None,
        "alert_visible": False,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


@st.cache_resource
def _get_optimizer():
    """v3.1 — Kilotons CO2, weight_profile"""
    return OptimizationAgent().train()


# ══════════════════════════════════════════════════════════════════════════════
#  SEA-LANE WAYPOINTS
# ══════════════════════════════════════════════════════════════════════════════
_SEA_LANES = {
    ("PKG","VNCMT"):  [(3.0,101.4),(5.0,102.8),(7.5,104.5),(9.5,106.0),(10.6,107.0)],
    ("SGP","VNCMT"):  [(1.3,103.8),(4.0,104.5),(7.0,105.5),(9.0,106.5),(10.6,107.0)],
    ("HKG","VNCMT"):  [(22.3,114.2),(18.5,114.0),(15.0,112.0),(12.5,110.0),(10.6,107.0)],
    ("PUS","VNCMT"):  [(35.1,129.0),(28.0,126.0),(22.0,121.0),(18.0,115.0),(14.0,111.0),(10.6,107.0)],
    ("SHA","VNCMT"):  [(31.4,121.7),(25.0,122.0),(20.0,118.0),(16.0,113.0),(12.0,110.0),(10.6,107.0)],
    ("MUM","VNCMT"):  [(18.9,72.8),(8.0,77.0),(5.5,80.5),(5.0,95.0),(4.5,100.5),(5.5,104.0),(8.5,107.0),(10.6,107.0)],
    ("DXB","VNCMT"):  [(25.0,55.1),(12.5,51.0),(8.5,53.0),(8.0,72.0),(5.5,80.0),(5.0,95.0),(5.0,100.5),(5.5,104.0),(10.6,107.0)],
    ("CMB","VNCMT"):  [(6.9,79.9),(5.5,82.0),(5.0,90.0),(5.0,98.0),(4.5,101.0),(5.5,104.0),(8.5,107.0),(10.6,107.0)],
    ("RTM","VNCMT"):  [(51.9,4.5),(36.0,5.0),(30.0,32.0),(12.0,43.0),(11.5,51.0),(8.0,72.0),(5.0,80.0),(5.0,100.0),(5.5,104.0),(10.6,107.0)],
    ("PKG","CHT"):    [(3.0,101.4),(5.0,96.0),(10.0,88.0),(14.0,90.0),(22.3,91.8)],
    ("SGP","CHT"):    [(1.3,103.8),(5.0,96.0),(10.0,88.0),(14.0,90.0),(22.3,91.8)],
    ("CMB","CHT"):    [(6.9,79.9),(8.0,82.0),(12.0,85.0),(18.0,89.0),(22.3,91.8)],
    ("SGP","MUM"):    [(1.3,103.8),(5.0,98.0),(7.0,82.0),(10.0,76.0),(14.0,74.0),(18.9,72.8)],
    ("DXB","MUM"):    [(25.0,55.1),(20.0,63.0),(18.9,72.8)],
    ("PUS","LAX"):    [(35.1,129.0),(38.0,145.0),(42.0,160.0),(45.0,175.0),(40.0,-155.0),(35.0,-135.0),(33.7,-118.3)],
    ("SHA","LAX"):    [(31.4,121.7),(35.0,140.0),(42.0,158.0),(45.0,175.0),(40.0,-155.0),(35.0,-135.0),(33.7,-118.3)],
    ("DXB","PSE"):    [(25.0,55.1),(20.0,45.0),(15.0,42.0),(12.0,43.0),(15.0,38.0),(25.0,34.0),(31.3,32.3)],
    ("RTM","PSE"):    [(51.9,4.5),(36.0,5.0),(31.3,32.3)],
}

def _get_waypoints(from_id, to_id):
    key = (from_id, to_id)
    if key in _SEA_LANES: return _SEA_LANES[key]
    rkey = (to_id, from_id)
    if rkey in _SEA_LANES: return list(reversed(_SEA_LANES[rkey]))
    p1, p2 = ATLAS_PORTS.get(from_id,{}), ATLAS_PORTS.get(to_id,{})
    if p1 and p2: return [(p1["lat"],p1["lon"]),(p2["lat"],p2["lon"])]
    return []


# ══════════════════════════════════════════════════════════════════════════════
#  TERMINAL RENDERER
# ══════════════════════════════════════════════════════════════════════════════
def _fmt_line(raw: str) -> str:
    s = _h.escape(raw)
    if not s.strip():
        return '<div style="height:0.4rem;"></div>'
    if s.startswith(("═","─","━")):
        return f'<div style="color:#4EC9B0;font-weight:600;">{s}</div>'
    if s.strip().startswith("[") and "]" in s:
        i = s.index("]") + 1
        return (f'<div><span style="color:#4EC9B0;font-weight:700;">{s[:i]}</span>'
                f'<span style="color:#9CDCFE;">{s[i:]}</span></div>')
    if any(k in s.upper() for k in ("COMPLETE","SUCCESS","APPROVED","MATCHED")):
        return f'<div style="color:#4FC614;font-weight:700;">{s}</div>'
    if any(k in s.upper() for k in ("RECOMMENDATION","SELECTED","OPTIMAL","WINNER")):
        return f'<div style="color:#E5C07B;font-weight:700;">{s}</div>'
    if any(k in s.upper() for k in ("RISK","BREACH","PENALTY","CRITICAL")):
        return f'<div style="color:#F97583;">{s}</div>'
    if s.startswith("  ") or s.startswith("\t"):
        return f'<div style="color:#ABB2BF;">{s}</div>'
    return f'<div style="color:#58D68D;">{s}</div>'

def _terminal_html(lines: list) -> str:
    inner = "".join(_fmt_line(l) for l in lines[-120:])
    return f'<div class="agent-terminal">{inner}</div>'


# ══════════════════════════════════════════════════════════════════════════════
#  MAP BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def _build_map(demand_port_id, ranked_routes, show_demand=True, height=420, scale=3.5):
    fig = go.Figure()
    plats,plons,ptexts,pcolors = [],[],[],[]
    for pid,p in ATLAS_PORTS.items():
        if pid == demand_port_id: continue
        c = DANGER if p["inv_status"]=="Shortage" else (SUCCESS if p["inv_status"]=="Surplus" else WARNING)
        plats.append(p["lat"]); plons.append(p["lon"])
        ptexts.append(f"{p['name']}<br>{p['inv_status']}: {p['surplus_teu']:+,} TEU"); pcolors.append(c)
    fig.add_trace(go.Scattergeo(lat=plats,lon=plons,mode="markers",
        marker=dict(size=7,color=pcolors,opacity=0.8,line=dict(width=1,color="white")),
        text=ptexts,hoverinfo="text",name="Ports"))
    route_colors = [SUCCESS,WARNING,DANGER,INFO]
    dp = ATLAS_PORTS.get(demand_port_id,{})
    for i,route in enumerate(ranked_routes[:3]):
        fid = route.get("port_id","")
        fids = [x.strip() for x in fid.split("+") if x.strip() in ATLAS_PORTS]
        rc = route_colors[i%len(route_colors)]
        for f in fids:
            wps = _get_waypoints(f,demand_port_id)
            if wps:
                fig.add_trace(go.Scattergeo(
                    lat=[w[0] for w in wps],lon=[w[1] for w in wps],mode="lines",
                    line=dict(width=2.5 if i==0 else 1.5,color=rc,dash="solid" if i==0 else "dot"),
                    opacity=0.9 if i==0 else 0.5,
                    name=f"Route #{route['rank']} — {route['from_port']}",hoverinfo="skip"))
            fp=ATLAS_PORTS.get(f)
            if fp:
                fig.add_trace(go.Scattergeo(
                    lat=[fp["lat"]],lon=[fp["lon"]],mode="markers+text",
                    marker=dict(size=13 if i==0 else 9,color=rc,symbol="circle",line=dict(width=2,color="white")),
                    text=[f"#{route['rank']}"],textfont=dict(size=8,color="white"),textposition="middle center",
                    hovertext=f"Route #{route['rank']}: {route['from_port']}<br>Cost: ${route['cost_per_teu']}/TEU | SLA: {route['sla_pct']}%",
                    hoverinfo="text",showlegend=False))
    if show_demand and dp:
        fig.add_trace(go.Scattergeo(
            lat=[dp["lat"]],lon=[dp["lon"]],mode="markers+text",
            marker=dict(size=18,color=DANGER,symbol="star",line=dict(width=2,color="white")),
            text=["⚡ DEMAND"],textfont=dict(size=9,color=DANGER,family="Arial Black"),
            textposition="top center",hovertext=f"DEMAND: {dp['name']}",
            hoverinfo="text",name="Demand Port"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=0,b=0),height=height,
        geo=dict(projection_type="natural earth",showland=True,landcolor="#E8EDF3",
                 showocean=True,oceancolor="#D4E8F7",showcoastlines=True,
                 coastlinecolor="#B0BEC5",coastlinewidth=0.8,
                 showcountries=True,countrycolor="#CBD5E1",countrywidth=0.5,
                 showlakes=True,lakecolor="#D4E8F7",showrivers=False,
                 center=dict(lat=dp.get("lat",10),lon=dp.get("lon",107)),
                 projection_scale=scale,bgcolor="rgba(0,0,0,0)"),
        legend=dict(bgcolor="rgba(255,255,255,0.9)",bordercolor=BORDER,borderwidth=1,
                    font=dict(size=11,color=TEXT_BODY),x=0.01,y=0.99),
        font=dict(family="Segoe UI",color=TEXT_BODY))
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  TOP NAVBAR (with logos + hide Streamlit chrome)
# ══════════════════════════════════════════════════════════════════════════════
def _render_topnav():
    page = st.session_state.page
    st.markdown(
        f'<div style="background:{MAERSK_DARK};padding:0.55rem 1.5rem;'
        f'display:flex;align-items:center;justify-content:space-between;'
        f'border-radius:0 0 8px 8px;box-shadow:0 2px 10px rgba(0,0,0,0.2);margin-bottom:0.2rem;">'
        # left: TCS logo + brand
        f'<div style="display:flex;align-items:center;gap:0.9rem;">'
        f'<img src="{LOGO_TCS}" style="height:36px;border-radius:4px;object-fit:contain;" />'
        f'<div style="width:1px;height:28px;background:rgba(255,255,255,0.18);"></div>'
        f'<div>'
        f'<div style="color:{TEXT_INV};font-size:1.05rem;font-weight:700;letter-spacing:0.03em;">TCS ATLAS</div>'
        f'<div style="color:{MAERSK_TEAL};font-size:0.66rem;letter-spacing:0.02em;">{SYSTEM_FULL}&nbsp;·&nbsp;v{ATLAS_VERSION}</div>'
        f'</div></div>'
        # centre: stats
        f'<div style="display:flex;align-items:center;gap:1.2rem;">'
        f'<span style="color:#94A3B8;font-size:0.78rem;">'
        f'🌐 {NETWORK_PORTS} Ports &nbsp;|&nbsp; 🚢 {TOTAL_VESSELS} Vessels &nbsp;|&nbsp; 📦 {GLOBAL_EMPTY_TEUS:,} TEUs'
        f'</span>'
        f'<span style="background:{MAERSK_TEAL};color:{MAERSK_DARK};padding:2px 10px;border-radius:12px;'
        f'font-size:0.68rem;font-weight:800;letter-spacing:0.06em;">● LIVE</span>'
        f'</div>'
        # right: Maersk logo + home btn
        f'<div style="display:flex;align-items:center;gap:0.9rem;">'
        f'<img src="{LOGO_MAERSK}" style="height:30px;border-radius:4px;object-fit:contain;" />'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if page == "container_sc":
        c1, c2 = st.columns([10,1])
        with c2:
            if st.button("← Home", key="nav_home"):
                st.session_state.page = "home"
                st.session_state.sc_tab = "overview"
                st.session_state.console_phase = "setup"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  HOME PAGE  ─  Maritime Control Tower
# ══════════════════════════════════════════════════════════════════════════════
def _build_uc_card(uc: dict) -> str:
    kpi_divs = "".join(
        f'<div style="background:{BG_ALT};border-radius:5px;padding:0.4rem 0.5rem;text-align:center;">'
        f'<div style="font-size:0.95rem;font-weight:700;color:{uc["color"]};">{v}</div>'
        f'<div style="font-size:0.65rem;color:{TEXT_MUTED};line-height:1.2;">{k}</div>'
        f'</div>'
        for k, v in uc["kpis"]
    )
    feat_divs = "".join(
        f'<div style="font-size:0.78rem;color:{TEXT_MUTED};padding:0.1rem 0;">'
        f'<span style="color:{SUCCESS};">✓</span> {f}</div>'
        for f in uc["features"][:3]
    )
    badge = (
        f'<span class="badge-live">● Live</span>' if uc["status"] == "Live"
        else f'<span class="badge-dev">In Development</span>'
    )
    return (
        f'<div class="ent-card" style="border-top:3px solid {uc["color"]};min-height:310px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.7rem;">'
        f'<span style="font-size:2rem;">{uc["icon"]}</span>{badge}</div>'
        f'<div style="font-size:1.05rem;font-weight:700;color:{TEXT_H};margin-bottom:0.12rem;">{uc["title"]}</div>'
        f'<div style="font-size:0.7rem;color:{uc["color"]};font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.06em;margin-bottom:0.5rem;">{uc["domain"]}</div>'
        f'<div style="font-size:0.82rem;color:{TEXT_MUTED};margin-bottom:0.8rem;line-height:1.4;">{uc["short"]}</div>'
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.35rem;margin-bottom:0.8rem;">'
        f'{kpi_divs}</div>{feat_divs}'
        f'<div style="margin-top:0.55rem;font-size:0.73rem;color:{TEXT_CAPTION};">'
        f'Annual Value: <strong style="color:{uc["color"]};">{uc["annual_value"]}</strong></div>'
        f'</div>'
    )


def page_home():
    st.markdown(
        f'<div style="padding:1.1rem 0 0.5rem;">'
        f'<div style="font-size:0.78rem;font-weight:700;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:{MAERSK_BLUE};margin-bottom:0.3rem;">'
        f'{CLIENT_NAME} · {PLATFORM_NAME}</div>'
        f'<div style="font-size:1.9rem;font-weight:800;color:{TEXT_H};line-height:1.2;margin-bottom:0.4rem;">'
        f'Maritime Control Tower</div>'
        f'<div style="font-size:0.95rem;color:{TEXT_MUTED};max-width:680px;line-height:1.5;">'
        f'AI-powered autonomous decision intelligence across Maersk\'s global operations — '
        f'from port visibility to container repositioning, fuel optimisation, and commercial pricing.'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    stats = [
        ("🌐", f"{NETWORK_PORTS}", "Global Ports", f"{NETWORK_COUNTRIES} Countries"),
        ("🚢", f"{TOTAL_VESSELS}", "Active Vessels", "In-network fleet"),
        ("📦", f"{GLOBAL_EMPTY_TEUS:,}", "Empty TEUs", "Live tracking"),
        ("🏭", f"{DEPOT_LOCATIONS}", "Depot Locations", "Container depots"),
    ]
    for col, (icon, val, label, sub) in zip(st.columns(4), stats):
        with col:
            st.markdown(
                f'<div class="kpi-tile">'
                f'<div style="font-size:1.3rem;">{icon}</div>'
                f'<div style="font-size:1.65rem;font-weight:700;color:{MAERSK_DARK};">{val}</div>'
                f'<div style="font-size:0.8rem;font-weight:600;color:{TEXT_H};">{label}</div>'
                f'<div style="font-size:0.7rem;color:{TEXT_MUTED};">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Autonomous Intelligence Modules</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    for col, i in zip(st.columns(3), range(3)):
        with col:
            uc = USE_CASES[i]
            st.markdown(_build_uc_card(uc), unsafe_allow_html=True)
            if uc["active"]:
                if st.button(f"🚀 Launch — {uc['title']}", key=f"uc_{uc['id']}", use_container_width=True):
                    st.session_state.page = "container_sc"
                    st.session_state.sc_tab = "overview"
                    st.rerun()
            else:
                st.button(f"Explore {uc['title']}", key=f"uc_{uc['id']}", disabled=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, c1, c2, _ = st.columns([0.5, 2, 2, 0.5])
    for col, i in zip([c1, c2], range(3, 5)):
        with col:
            uc = USE_CASES[i]
            st.markdown(_build_uc_card(uc), unsafe_allow_html=True)
            st.button(f"Explore {uc['title']}", key=f"uc_{uc['id']}", disabled=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CONTAINER SC — SUB-NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
#  TAB NAVIGATION — Button-Based (No st.radio — Fixes State Conflicts)
# ══════════════════════════════════════════════════════════════════════════════
_SC_TABS = {
    "overview":  ("📊 Overview",      "View demand, port inventory, and trigger alerts"),
    "console":   ("🤖 Agent Console", "Run autonomous agents and optimize routes"),
    "settings":  ("⚙️ Settings",      "Configure demand scenarios and preferences"),
}


def _render_sc_tabs_buttons():
    """Render tab navigation using buttons (replaces st.radio).
    
    Benefits over st.radio:
    - No state desynchronization bugs
    - Clean button-click → state-update → rerun() flow
    - Each button directly updates st.session_state.sc_tab
    - Better contrast: gray inactive, blue active tabs
    """
    current_tab = st.session_state.sc_tab
    
    # Initialize list to hold button columns
    tab_cols = st.columns([1, 1, 1])
    
    for col_idx, (tab_key, (icon_label, tooltip)) in enumerate(_SC_TABS.items()):
        is_active = current_tab == tab_key
        
        with tab_cols[col_idx]:
            # Create a container with styled background
            bg_color = MAERSK_BLUE if is_active else BG_ALT
            text_color = "#FFFFFF" if is_active else TEXT_BODY
            font_wt = "700" if is_active else "600"
            
            # Use columns + markdown to create custom styled button appearance
            # The actual button is here but we style it with the markdown above
            st.markdown(
                f'<div style="'
                f'background-color: {bg_color}; '
                f'color: {text_color}; '
                f'padding: 0.7rem 1rem; '
                f'border-radius: 6px; '
                f'text-align: center; '
                f'font-weight: {font_wt}; '
                f'font-size: 0.95rem; '
                f'margin-bottom: 0.5rem; '
                f'border: 2px solid {MAERSK_BLUE if is_active else BORDER}; '
                f'cursor: pointer; '
                f'transition: all 0.2s; '
                f'">{icon_label}</div>',
                unsafe_allow_html=True
            )
            
            # Actual button (only registers click, no visual styling)
            if st.button(
                label="",
                key=f"nav_tab_{tab_key}",
                use_container_width=True,
                help=tooltip
            ):
                st.session_state.sc_tab = tab_key
                st.rerun()
    
    # Visual separator
    st.divider()


# ══════════════════════════════════════════════════════════════════════════════
#  OVERVIEW TAB
# ══════════════════════════════════════════════════════════════════════════════
def _show_demand_alert():
    """Generate alert from current selected demand scenario"""
    sc = DEMAND_SCENARIOS.get(st.session_state.scenario_key, {})
    port_id = sc.get("port_id")
    port_data = ATLAS_PORTS.get(port_id, {})
    
    # Create alert from demand scenario
    st.session_state.active_alert = {
        "demanding_port": port_id,
        "port_name": sc.get("port_name", "Unknown Port"),
        "shortage_teu": sc.get("teu_required", 0),
        "urgency_level": sc.get("urgency", "HIGH"),
        "description": sc.get("description", "Supply chain demand detected"),
        "candidate_vessels": sc.get("candidate_vessels", []),
        "potential_savings": sc.get("potential_savings", 0),
        "estimated_lead_time": "8-12 hours",
    }
    st.session_state.alert_visible = True

def _sc_overview():
    idx = st.session_state.news_idx % len(NEWS_ITEMS)
    st.session_state.news_idx += 1
    st.markdown(
        f'<div class="news-ticker">'
        f'<span style="background:{MAERSK_BLUE};color:#fff;padding:1px 8px;border-radius:3px;'
        f'font-size:0.65rem;font-weight:700;letter-spacing:0.05em;white-space:nowrap;">MARKET FEED</span>'
        f'<span>{NEWS_ITEMS[idx]}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Today's Challenge Card ─────────────────────────────────
    shortage_ports = [p for p in ATLAS_PORTS.values() if p["inv_status"] == "Shortage"]
    surplus_ports  = [p for p in ATLAS_PORTS.values() if p["inv_status"] == "Surplus"]
    shortage_total = abs(sum(p["surplus_teu"] for p in shortage_ports)) // 1000
    surplus_total  = sum(p["surplus_teu"] for p in surplus_ports) // 1000
    st.markdown(f'''
<div style="background:linear-gradient(135deg,#FEE2E2 0%,#FFE4E6 100%);
            border:2px solid {DANGER};border-radius:10px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;">
    <div style="font-size:1.05rem;font-weight:700;color:#7F1D1D;margin-bottom:0.5rem;">
        🎯 Today's Challenge
    </div>
    <div style="font-size:0.9rem;color:#991B1B;line-height:1.6;">
        Global network has <strong>{shortage_total}K TEU shortage</strong> and <strong>{surplus_total}K TEU surplus</strong> across {len(shortage_ports)} shortage ports.
        Deploy autonomous agents to reposition containers optimally, saving $85K–$125K per operation while meeting SLA targets.
    </div>
</div>''', unsafe_allow_html=True)

    if st.session_state.approved_route:
        ap = st.session_state.approved_route
        sc_key = st.session_state.scenario_key
        sc = DEMAND_SCENARIOS[sc_key]
        st.markdown(
            f'<div style="background:linear-gradient(90deg,{SUCCESS},#15803D);border-radius:8px;'
            f'padding:0.8rem 1.2rem;margin-bottom:0.8rem;display:flex;align-items:center;gap:1rem;">'
            f'<span style="font-size:1.4rem;">✅</span>'
            f'<div><div style="color:#fff;font-weight:700;">Route Approved — {ap["from_port"]} → {sc["port_name"]}</div>'
            f'<div style="color:#BBF7D0;font-size:0.78rem;">'
            f'${ap["cost_per_teu"]}/TEU · SLA {ap["sla_pct"]}% · Score {ap.get("_final","—")}/100 · '
            f'{ap.get("co2_kilotons",0):.3f} Kt CO₂</div></div>'
            f'<div style="margin-left:auto;">'
            f'<span style="color:#BBF7D0;font-size:0.75rem;">{datetime.now().strftime("%d %b %Y %H:%M")}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    left, right = st.columns([3, 2])
    with left:
        st.markdown(f'<span class="sec-header">Port Network — Inventory Status</span>', unsafe_allow_html=True)
        mc = st.columns(5)
        for col, pid in zip(mc, MONITOR_PORTS):
            p = ATLAS_PORTS[pid]
            sur = p["surplus_teu"]
            status = p["inv_status"]
            color = DANGER if status=="Shortage" else (SUCCESS if status=="Surplus" else WARNING)
            icon = "⬇" if status=="Shortage" else ("⬆" if status=="Surplus" else "↔")
            with col:
                st.markdown(
                    f'<div class="kpi-tile" style="border-top:2px solid {color};padding:0.65rem 0.4rem;">'
                    f'<div style="font-size:0.65rem;font-weight:700;color:{TEXT_MUTED};">{p["name"].split("(")[0].strip()}</div>'
                    f'<div style="font-size:0.95rem;font-weight:700;color:{color};">{icon} {abs(sur):,}</div>'
                    f'<div style="font-size:0.62rem;color:{color};font-weight:600;">{status}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<br>", unsafe_allow_html=True)

        # ── Inline Fleet Map ────────────────────────────────────
        st.markdown(f'<span class="sec-header">Live Fleet & Port Network Map</span>', unsafe_allow_html=True)
        fig_map = go.Figure()
        for pid, p in ATLAS_PORTS.items():
            c = DANGER if p["inv_status"]=="Shortage" else (SUCCESS if p["inv_status"]=="Surplus" else WARNING)
            sym = "triangle-down" if p["inv_status"]=="Shortage" else ("triangle-up" if p["inv_status"]=="Surplus" else "circle")
            fig_map.add_trace(go.Scattergeo(lat=[p["lat"]],lon=[p["lon"]],mode="markers+text",
                marker=dict(size=8,color=c,symbol=sym,line=dict(width=1,color="white")),
                text=[p["name"].split("(")[0].strip()[:8]],textposition="top center",
                textfont=dict(size=7,color=TEXT_BODY),
                hovertext=f"{p['name']}<br>{p['inv_status']}: {p['surplus_teu']:+,} TEU",
                hoverinfo="text",showlegend=False))
        for v in FLEET_VESSELS:
            fp = ATLAS_PORTS.get(v["from_port"],{})
            tp = ATLAS_PORTS.get(v["to_port"],{})
            if fp and tp:
                mid_lat = (fp["lat"]+tp["lat"])/2
                mid_lon = (fp["lon"]+tp["lon"])/2
                fig_map.add_trace(go.Scattergeo(
                    lat=[fp["lat"],mid_lat,tp["lat"]],lon=[fp["lon"],mid_lon,tp["lon"]],
                    mode="lines",line=dict(width=1.5,color=MAERSK_BLUE,dash="dot"),
                    opacity=0.5,hoverinfo="skip",showlegend=False))
                fig_map.add_trace(go.Scattergeo(lat=[mid_lat],lon=[mid_lon],mode="markers",
                    marker=dict(size=9,color=MAERSK_BLUE,symbol="diamond",line=dict(width=1,color="white")),
                    hovertext=f"{v['vessel']}<br>{v['from_port']}→{v['to_port']}<br>Empty: {v['empty_teu']:,} TEU",
                    hoverinfo="text",showlegend=False))
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0),height=340,
            geo=dict(projection_type="natural earth",showland=True,landcolor="#E8EDF3",
                     showocean=True,oceancolor="#D4E8F7",showcoastlines=True,
                     coastlinecolor="#B0BEC5",showcountries=True,countrycolor="#CBD5E1",
                     showlakes=True,lakecolor="#D4E8F7",bgcolor="rgba(0,0,0,0)"),
            font=dict(family="Segoe UI",color=TEXT_BODY))
        st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
        # Legend
        lc1,lc2,lc3 = st.columns(3)
        for col,(color,sym,label) in zip([lc1,lc2,lc3],[
            (DANGER,"▼","Shortage Port"),(SUCCESS,"▲","Surplus Port"),(MAERSK_BLUE,"◆","Active Vessel")]):
            with col:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.4rem;font-size:0.78rem;color:{TEXT_MUTED};">'
                    f'<span style="color:{color};font-size:0.95rem;">{sym}</span><span>{label}</span></div>',
                    unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Active Fleet Table ──────────────────────────────────
        st.markdown(f'<span class="sec-header">Active Fleet Plan</span>', unsafe_allow_html=True)
        if st.session_state.approved_route:
            approved = st.session_state.approved_route
            rows = ""
            for v in FLEET_VESSELS:
                pr = v.get("planned_route", {})
                planned_str = f"{pr.get('from_port', v['from_port'])} → {pr.get('to_port', v['to_port'])}"
                planned_cost = pr.get("cost_per_teu", "—")
                # Check if this vessel is the approved one
                is_optimized = approved.get("vessel","") == v["vessel"]
                if is_optimized:
                    opt_str = f"OPTIMIZED: {approved['from_port'][:6]}→{st.session_state.demand_result['port_id'] if st.session_state.demand_result else '...'}"
                    opt_cost = f"${approved['cost_per_teu']}"
                    delta = approved['cost_per_teu'] - (planned_cost if isinstance(planned_cost, int) else 0)
                    delta_str = f'<span style="color:{SUCCESS if delta<0 else DANGER};">{"−" if delta<0 else "+"} ${abs(delta)}</span>'
                else:
                    opt_str = "—"
                    opt_cost = "—"
                    delta_str = "—"
                rows += (
                    f'<tr><td>{v["vessel"].replace("MV ","")}</td>'
                    f'<td>{planned_str}</td>'
                    f'<td>{opt_str}</td>'
                    f'<td>{v["empty_teu"]:,} TEU</td>'
                    f'<td style="color:{"#16A34A" if v["status"]=="In Transit" else "#D97706"};">{v["status"]}</td>'
                    f'<td>${planned_cost}/TEU</td>'
                    f'<td>{delta_str}</td></tr>'
                )
            st.markdown(
                f'<div style="overflow-x:auto;border-radius:8px;border:1px solid {BORDER};">'
                f'<table class="ent-table"><thead><tr><th>Vessel</th><th>Planned Route</th>'
                f'<th>↓ Optimized Route</th><th>Empty TEU</th><th>Status</th><th>Plan Cost</th><th>Delta</th>'
                f'</tr></thead><tbody>{rows}</tbody></table></div>',
                unsafe_allow_html=True,
            )
        else:
            rows = "".join(
                f'<tr><td>{v["vessel"].replace("MV ","")}</td>'
                f'<td>{v.get("planned_route",{}).get("from_port",v["from_port"])} → {v.get("planned_route",{}).get("to_port",v["to_port"])}</td>'
                f'<td>{v["empty_teu"]:,} TEU</td>'
                f'<td style="color:{"#16A34A" if v["status"]=="In Transit" else "#D97706"};">{v["status"]}</td>'
                f'<td>${v.get("planned_route",{}).get("cost_per_teu","—")}/TEU</td></tr>'
                for v in FLEET_VESSELS
            )
            st.markdown(
                f'<div style="overflow:hidden;border-radius:8px;border:1px solid {BORDER};">'
                f'<table class="ent-table"><thead><tr><th>Vessel</th><th>Planned Route</th>'
                f'<th>Empty TEU</th><th>Status</th><th>Cost/TEU</th></tr></thead><tbody>{rows}</tbody></table></div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(f'<span class="sec-header">Container Inventory</span>', unsafe_allow_html=True)
        bc = {"Dry (20ft)":MAERSK_BLUE,"Dry (40ft)":MAERSK_LIGHT,"Reefer":MAERSK_TEAL,"In Transit":WARNING}
        bar_html = "".join(
            f'<div style="margin-bottom:0.5rem;">'
            f'<div style="display:flex;justify-content:space-between;font-size:0.8rem;color:{TEXT_BODY};margin-bottom:0.18rem;">'
            f'<span>{ct}</span><span style="font-weight:600;">{pct}%</span></div>'
            f'<div style="background:{BORDER};border-radius:3px;height:7px;">'
            f'<div style="width:{pct}%;background:{bc.get(ct,MAERSK_BLUE)};border-radius:3px;height:100%;"></div>'
            f'</div></div>'
            for ct, pct in CONTAINER_INVENTORY.items()
        )
        st.markdown(f'<div class="ent-card">{bar_html}</div>', unsafe_allow_html=True)

        src_html = "".join(
            f'<div style="display:flex;align-items:center;gap:0.5rem;padding:0.4rem 0;border-bottom:1px solid {BORDER};">'
            f'<span>{"📡" if "Port" in s else "🛰️" if "AIS" in s else "🏢" if "SAP" in s else "🌤️" if "Weather" in s else "🌍"}</span>'
            f'<span style="font-size:0.82rem;color:{TEXT_BODY};flex:1;">{s}</span>'
            f'<span style="color:{SUCCESS};font-size:0.72rem;font-weight:700;">● Live</span></div>'
            for s in DATA_SOURCES
        )
        st.markdown(f'<div class="ent-card"><div class="sec-header">Data Sources</div>{src_html}</div>', unsafe_allow_html=True)

        bl = BASELINE_STATIC
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<span class="sec-header">Current Network Baseline</span>', unsafe_allow_html=True)
        bkpis = [
            ("Repositioning Cost/TEU", f"${bl['cost_per_teu']:,}", WARNING),
            ("SLA Compliance Rate",    f"{bl['sla_pct']}%",          DANGER),
            ("Manual Decision Time",   f"{bl['decision_hours']}+ hrs", WARNING),
            ("CO₂ Baseline",           f"{bl['co2_kilotons']:.3f} Kt",  INFO),
        ]
        for label, val, color in bkpis:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:0.4rem 0;border-bottom:1px solid {BORDER};">'
                f'<span style="font-size:0.8rem;color:{TEXT_MUTED};">{label}</span>'
                f'<span style="font-size:0.88rem;font-weight:700;color:{color};">{val}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if not st.session_state.approved_route:
            st.button("🚀 Trigger", key="overview_trigger", use_container_width=True, on_click=_show_demand_alert)
        else:
            if st.button("↩ New Optimization Cycle", key="overview_reset", use_container_width=True):
                st.session_state.console_phase = "setup"
                st.session_state.demand_result = None
                st.session_state.opt_result = None
                st.session_state.approved_route = None
                st.session_state.active_alert = None
                st.session_state["terminal_lines"] = []
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE — SETUP
# ══════════════════════════════════════════════════════════════════════════════
def _console_setup():
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{MAERSK_DARK} 0%,#003A5D 100%);'
        f'border-radius:10px;padding:1.2rem 1.5rem;margin-bottom:1rem;">'
        f'<div style="display:flex;align-items:center;gap:0.8rem;">'
        f'<span style="font-size:1.6rem;">🤖</span>'
        f'<div><div style="color:{TEXT_INV};font-size:1.1rem;font-weight:700;">Agent Execution Console</div>'
        f'<div style="color:{MAERSK_TEAL};font-size:0.78rem;">'
        f'Autonomous pipeline: Demand Intelligence → Inventory Discovery → Route Optimisation</div></div>'
        f'<div style="margin-left:auto;">'
        f'<span style="background:#22C55E22;color:{SUCCESS};padding:4px 12px;border-radius:12px;'
        f'font-size:0.75rem;font-weight:700;border:1px solid {SUCCESS}32;">● Standby</span></div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # Show alert context if triggered from Overview
    alert = st.session_state.get("active_alert")
    if alert:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#FEF3C7,#FDE68A);border:2px solid {WARNING};'
            f'border-radius:10px;padding:1rem 1.3rem;margin-bottom:1rem;">'
            f'<div style="font-size:0.95rem;font-weight:700;color:#92400E;margin-bottom:0.5rem;">'
            f'⚠️ Alert: {alert["port_name"]} — {alert["shortage_teu"]:,} TEU Shortage</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.5rem;">'
            f'<div><div style="font-size:0.65rem;color:{TEXT_MUTED};">Urgency</div>'
            f'<div style="font-weight:700;color:{DANGER};">{alert["urgency_level"]}</div></div>'
            f'<div><div style="font-size:0.65rem;color:{TEXT_MUTED};">Candidate Vessels</div>'
            f'<div style="font-weight:700;color:{TEXT_H};">{", ".join(v.replace("MV ","") for v in alert["candidate_vessels"])}</div></div>'
            f'<div><div style="font-size:0.65rem;color:{TEXT_MUTED};">Potential Savings</div>'
            f'<div style="font-weight:700;color:{SUCCESS};">${alert["potential_savings"]:,}</div></div>'
            f'</div>'
            f'<div style="font-size:0.78rem;color:#92400E;margin-top:0.5rem;">📍 {alert["description"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    steps = [
        ("1","🔍","Demand Intelligence",
         "Analyses the inbound demand signal from the shipper, classifies urgency tier, "
         "models SLA breach risk and financial exposure.",
         ["Demand classification","Urgency tiering","Penalty modelling","Source validation"]),
        ("2","🏭","Inventory Discovery",
         "Scans all 68 global depot locations for available empty containers. "
         "Ranks by proximity, inventory coverage, transit feasibility and cost.",
         ["Global depot scan","Distance scoring","Coverage analysis","Transit feasibility"]),
        ("3","🗺️","Route Optimisation",
         "Scores candidate routes using trained forecasting model plus weighted business priorities. "
         "Produces ranked recommendations with full reasoning.",
         ["Model-based scoring","Multi-criteria ranking","Cost vs carbon vs SLA","Explainable output"]),
    ]
    c1, c2, c3 = st.columns(3)
    for col, (num, icon, name, desc, features) in zip([c1, c2, c3], steps):
        color = [MAERSK_BLUE, MAERSK_TEAL, SUCCESS][int(num)-1]
        with col:
            feats = "".join(f'<div style="font-size:0.75rem;color:{TEXT_MUTED};padding:0.12rem 0;">'
                            f'<span style="color:{color};">▸</span> {f}</div>' for f in features)
            st.markdown(
                f'<div class="ent-card" style="border-top:3px solid {color};min-height:220px;">'
                f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.6rem;">'
                f'<span style="background:{color};color:#fff;border-radius:50%;width:26px;height:26px;'
                f'display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;">{num}</span>'
                f'<span style="font-size:1rem;font-weight:700;color:{TEXT_H};">{icon} {name}</span></div>'
                f'<div style="font-size:0.8rem;color:{TEXT_MUTED};line-height:1.45;margin-bottom:0.6rem;">{desc}</div>'
                f'{feats}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        # If alert is active, use its demand scenario, otherwise let user select
        alert = st.session_state.get("active_alert")
        if alert:
            # Auto-select scenario based on alert - find matching scenario
            matching_scenario = None
            for scenario_key, sc in DEMAND_SCENARIOS.items():
                if sc.get("port_id") == alert.get("demanding_port"):
                    matching_scenario = scenario_key
                    break
            
            if matching_scenario:
                st.session_state.scenario_key = matching_scenario
                sel = matching_scenario
                st.info(f"📍 Using alert-triggered demand: {alert['port_name']}")
            else:
                # Fallback: use first scenario
                sel = list(DEMAND_SCENARIOS.keys())[0]
                st.session_state.scenario_key = sel
                st.warning(f"⚠️ No matching scenario for {alert['port_name']}, using default scenario")
        else:
            # Normal scenario selection
            scenario_labels = {k: v["label"] for k, v in DEMAND_SCENARIOS.items()}
            sel = st.selectbox(
                "Select Demand Scenario",
                options=list(scenario_labels.keys()),
                format_func=lambda k: scenario_labels[k],
                index=list(scenario_labels.keys()).index(st.session_state.scenario_key),
                key="console_scenario_selector",
            )
            st.session_state.scenario_key = sel
        
        sc = DEMAND_SCENARIOS[sel]

        urgency_cls = "badge-critical" if sc["urgency"]=="CRITICAL" else "badge-high"
        dp = ATLAS_PORTS.get(sc["port_id"],{})
        st.markdown(
            f'<div class="ent-card" style="border-left:3px solid {MAERSK_BLUE};">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;">'
            f'<span style="font-size:0.95rem;font-weight:700;color:{TEXT_H};">{sc["shipper"]}</span>'
            f'<span class="{urgency_cls}">{sc["urgency"]}</span></div>'
            f'<div style="font-size:0.82rem;color:{TEXT_MUTED};line-height:1.4;margin-bottom:0.7rem;">{sc["description"]}</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.5rem;">'
            f'<div style="font-size:0.78rem;"><div style="color:{TEXT_MUTED};font-size:0.65rem;">Origin Port</div>'
            f'<div style="font-weight:700;color:{TEXT_H};">{sc["port_name"].split("(")[0].strip()}</div></div>'
            f'<div style="font-size:0.78rem;"><div style="color:{TEXT_MUTED};font-size:0.65rem;">Destination</div>'
            f'<div style="font-weight:700;color:{TEXT_H};">{sc["destination"].split(",")[0]}</div></div>'
            f'<div style="font-size:0.78rem;"><div style="color:{TEXT_MUTED};font-size:0.65rem;">Region</div>'
            f'<div style="font-weight:700;color:{TEXT_H};">{dp.get("region","—")}</div></div>'
            f'<div style="font-size:0.78rem;"><div style="color:{TEXT_MUTED};font-size:0.65rem;">TEU Required</div>'
            f'<div style="font-weight:700;color:{MAERSK_BLUE};font-size:1rem;">{sc["teu_required"]:,}</div></div>'
            f'<div style="font-size:0.78rem;"><div style="color:{TEXT_MUTED};font-size:0.65rem;">SLA Window</div>'
            f'<div style="font-weight:700;color:{WARNING};">{sc["sla_days"]} days</div></div>'
            f'<div style="font-size:0.78rem;"><div style="color:{TEXT_MUTED};font-size:0.65rem;">SLA Penalty</div>'
            f'<div style="font-weight:700;color:{DANGER};">${sc["penalty_per_day"]:,}/day</div></div>'
            f'</div>'
            f'<div style="margin-top:0.6rem;font-size:0.75rem;color:{TEXT_MUTED};">⚡ {sc["trigger"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(f'<span class="sec-header">Optimisation Priority</span>', unsafe_allow_html=True)
        profile = st.selectbox(
            "Business Priority Profile",
            options=list(WEIGHT_PROFILES.keys()),
            index=list(WEIGHT_PROFILES.keys()).index(st.session_state.weight_profile),
            key="console_profile",
        )
        st.session_state.weight_profile = profile
        w = WEIGHT_PROFILES[profile]
        weight_html = "".join(
            f'<div style="margin-bottom:0.45rem;">'
            f'<div style="display:flex;justify-content:space-between;font-size:0.78rem;color:{TEXT_BODY};margin-bottom:0.15rem;">'
            f'<span>{dim.capitalize()}</span><span style="font-weight:600;">{int(wt*100)}%</span></div>'
            f'<div style="background:{BORDER};border-radius:3px;height:6px;">'
            f'<div style="width:{int(wt*100)}%;background:{[MAERSK_BLUE,SUCCESS,INFO][i]};border-radius:3px;height:100%;"></div>'
            f'</div></div>'
            for i,(dim,wt) in enumerate(w.items())
        )
        st.markdown(f'<div class="ent-card" style="padding:0.9rem;">{weight_html}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<span class="sec-header">Baseline to Beat</span>', unsafe_allow_html=True)
        bl = BASELINE_STATIC
        for lbl, val, color in [
            ("Current Cost/TEU", f"${bl['cost_per_teu']:,}", DANGER),
            ("SLA Compliance",   f"{bl['sla_pct']}%",        DANGER),
            ("Decision Time",    f"{bl['decision_hours']}+ hours", WARNING),
        ]:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:0.35rem 0;'
                f'border-bottom:1px solid {BORDER};">'
                f'<span style="font-size:0.8rem;color:{TEXT_MUTED};">{lbl}</span>'
                f'<span style="font-size:0.85rem;font-weight:700;color:{color};">{val}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        # FIX 4: button text changed to "Run Agents"
        if st.button("🚀 Run Agents", key="console_launch_btn", use_container_width=True):
            st.session_state.console_phase = "running"
            st.session_state["terminal_lines"] = []  # clear old log on new run
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE — ANIMATED RUNNING
# ══════════════════════════════════════════════════════════════════════════════
def _console_running():
    sc = DEMAND_SCENARIOS[st.session_state.scenario_key]
    optimizer = _get_optimizer()

    st.markdown(
        f'<div style="background:{MAERSK_DARK};border-radius:10px;padding:0.85rem 1.4rem;'
        f'margin-bottom:0.8rem;display:flex;align-items:center;gap:0.8rem;">'
        f'<span style="font-size:1.3rem;">⚡</span>'
        f'<div><div style="color:{TEXT_INV};font-weight:700;font-size:0.95rem;">Pipeline Executing — {sc["label"]}</div>'
        f'<div style="color:{MAERSK_TEAL};font-size:0.74rem;">Agents processing in real time...</div></div>'
        f'<div style="margin-left:auto;">'
        f'<span style="background:{DANGER};color:#fff;padding:3px 10px;border-radius:12px;'
        f'font-size:0.7rem;font-weight:700;">● LIVE</span></div></div>',
        unsafe_allow_html=True,
    )

    col_term, col_status = st.columns([3, 2])
    with col_term:
        term_ph = st.empty()
    with col_status:
        status_ph = st.empty()

    st.markdown(f'<span class="sec-header" style="margin-top:0.5rem;">Agent Reports — Live</span>', unsafe_allow_html=True)
    demand_ph  = st.empty()
    supply_ph  = st.empty()
    opt_ph     = st.empty()

    # FIX 3: load any existing terminal lines from session state
    all_lines = list(st.session_state.get("terminal_lines", []))

    def _push(lines, delay=0.048):
        for l in lines:
            all_lines.append(l)
            st.session_state["terminal_lines"] = all_lines.copy()
            term_ph.markdown(_terminal_html(all_lines), unsafe_allow_html=True)
            time.sleep(delay)

    def _status(agent, pct, done):
        done_html = "".join(
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin:0.2rem 0;">'
            f'<span style="color:{SUCCESS};font-size:0.85rem;">✓</span>'
            f'<span style="font-size:0.82rem;color:{TEXT_BODY};">{a}</span></div>'
            for a in done
        )
        status_ph.markdown(
            f'<div class="ent-card">'
            f'<div class="sec-header">Agent Progress</div>'
            f'{done_html}'
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin:0.3rem 0;">'
            f'<span style="color:{MAERSK_BLUE};font-size:0.85rem;">⟳</span>'
            f'<span style="font-size:0.82rem;font-weight:600;color:{MAERSK_BLUE};">{agent}</span></div>'
            f'<div style="background:{BORDER};border-radius:4px;height:8px;margin-top:0.5rem;">'
            f'<div style="width:{pct}%;background:{MAERSK_BLUE};border-radius:4px;height:100%;'
            f'transition:width 0.3s;"></div></div>'
            f'<div style="font-size:0.72rem;color:{TEXT_MUTED};margin-top:0.25rem;">{pct}% complete</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    now = datetime.now().strftime("%H:%M:%S")
    _push([
        "═══════════════════════════════════════════════════════════",
        " TCS ATLAS — AUTONOMOUS AGENT PIPELINE",
        "═══════════════════════════════════════════════════════════",
        "",
        f"[{now}] System initialised — pipeline triggered",
        f"  Scenario  : {sc['label']}",
        f"  Shipper   : {sc['shipper']}",
        f"  Port      : {sc['port_name']}",
        f"  TEU Req.  : {sc['teu_required']:,} TEU",
        f"  Priority  : {sc['urgency']}",
        "",
        "Loading agent modules...",
        "  [OK] Demand Intelligence Agent",
        "  [OK] Inventory Discovery Agent",
        "  [OK] Route Optimisation Agent",
        "",
    ], delay=0.055)

    # ══ AGENT 1 ══
    _status("Demand Intelligence", 8, [])
    _push([
        "─────────────────────────────────────────────────",
        " STEP 1 / 3  —  DEMAND INTELLIGENCE AGENT",
        "─────────────────────────────────────────────────",
    ], delay=0.07)

    agent_a = DemandSensingAgent()
    demand  = agent_a.run(sc)
    _push(demand["stream_lines"], delay=0.052)
    _push(["", "  ✓ Demand Intelligence complete — passing to Inventory Discovery", ""], delay=0.06)
    time.sleep(0.35)

    dp = ATLAS_PORTS.get(demand["port_id"], {})
    urgency_cls = "badge-critical" if demand["urgency"]=="CRITICAL" else "badge-high"
    demand_ph.markdown(
        f'<div class="ent-card" style="border-top:3px solid {MAERSK_BLUE};">'
        f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.8rem;">'
        f'<span style="background:{MAERSK_BLUE};color:#fff;border-radius:6px;padding:3px 9px;font-size:0.72rem;font-weight:700;">✓ STEP 1</span>'
        f'<span style="font-size:0.95rem;font-weight:700;color:{TEXT_H};">🔍 Demand Intelligence Report</span>'
        f'<span class="{urgency_cls}" style="margin-left:auto;">{demand["urgency"]} · Tier {demand["tier"]}</span>'
        f'</div>'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.7rem;">'
        f'<div style="background:{BG_ALT};border-radius:7px;padding:0.65rem 0.7rem;text-align:center;">'
        f'<div style="font-size:0.62rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.05em;">Origin Port</div>'
        f'<div style="font-size:0.9rem;font-weight:700;color:{TEXT_H};">{dp.get("name","—").split("(")[0].strip()}</div>'
        f'<div style="font-size:0.68rem;color:{TEXT_MUTED};">{dp.get("country","—")}</div></div>'
        f'<div style="background:{BG_ALT};border-radius:7px;padding:0.65rem 0.7rem;text-align:center;">'
        f'<div style="font-size:0.62rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.05em;">TEU Required</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:{MAERSK_BLUE};">{demand["teu_required"]:,}</div>'
        f'<div style="font-size:0.68rem;color:{TEXT_MUTED};">{sc.get("container_mix","—")[:22]}</div></div>'
        f'<div style="background:{BG_ALT};border-radius:7px;padding:0.65rem 0.7rem;text-align:center;">'
        f'<div style="font-size:0.62rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.05em;">SLA Breach Risk</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:{DANGER};">{demand["breach_risk_pct"]}%</div>'
        f'<div style="font-size:0.68rem;color:{TEXT_MUTED};">Confidence {demand["confidence"]}%</div></div>'
        f'<div style="background:{BG_ALT};border-radius:7px;padding:0.65rem 0.7rem;text-align:center;">'
        f'<div style="font-size:0.62rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.05em;">Penalty Exposure</div>'
        f'<div style="font-size:1rem;font-weight:700;color:{DANGER};">${demand["total_penalty"]:,}</div>'
        f'<div style="font-size:0.68rem;color:{TEXT_MUTED};">${sc["penalty_per_day"]:,}/day × {sc["sla_days"]}d</div></div>'
        f'</div>'
        f'<div style="margin-top:0.7rem;display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">'
        + "".join(
            f'<div style="font-size:0.8rem;color:{TEXT_MUTED};padding:0.15rem 0;">'
            f'<span style="color:{MAERSK_BLUE};font-weight:600;">▸</span> {r}</div>'
            for r in demand["reasoning"]
        ) +
        f'</div></div>',
        unsafe_allow_html=True,
    )
    _status("Inventory Discovery", 35, ["Demand Intelligence"])

    # ══ AGENT 2 ══
    _push([
        "─────────────────────────────────────────────────",
        " STEP 2 / 3  —  INVENTORY DISCOVERY AGENT",
        "─────────────────────────────────────────────────",
        "",
        "[INVENTORY DISCOVERY] Scanning 68 global depot locations...",
        "[INVENTORY DISCOVERY] Filtering by SLA-feasible transit window...",
        "",
    ], delay=0.07)

    agent_b = SupplyFinderAgent()
    supply  = agent_b.run(demand)
    st.session_state.supply_result = supply

    for opt in supply[:4]:
        _push(opt.get("stream_lines", []), delay=0.044)
        time.sleep(0.08)

    _push(["", f"  ✓ {len([o for o in supply if o['feasible']])} feasible depots identified", ""], delay=0.06)
    time.sleep(0.35)

    depot_rows = "".join(
        f'<tr>'
        f'<td><strong>#{i+1}</strong></td>'
        f'<td>{o["port_name"]}</td>'
        f'<td>{o["country"]}</td>'
        f'<td style="color:{SUCCESS if o["feasible"] else DANGER};font-weight:600;">'
        f'{"✓ Feasible" if o["feasible"] else "✗ SLA risk"}</td>'
        f'<td>{o["available_teu"]:,}</td>'
        f'<td style="color:{SUCCESS if o["coverage_pct"]>=100 else WARNING};">{o["coverage_pct"]}%</td>'
        f'<td>{o["distance_km"]:,} km</td>'
        f'<td>{o["transit_days"]} d</td>'
        f'<td style="color:{MAERSK_BLUE};font-weight:600;">${o["cost_per_teu"]:,}</td>'
        f'<td style="color:{INFO};">{o["co2_kilotons"]:.4f} Kt</td>'
        f'</tr>'
        for i, o in enumerate(supply[:5])
    )
    supply_ph.markdown(
        f'<div class="ent-card" style="border-top:3px solid {MAERSK_TEAL};">'
        f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.8rem;">'
        f'<span style="background:{MAERSK_TEAL};color:#fff;border-radius:6px;padding:3px 9px;font-size:0.72rem;font-weight:700;">✓ STEP 2</span>'
        f'<span style="font-size:0.95rem;font-weight:700;color:{TEXT_H};">🏭 Inventory Discovery — Top {min(5,len(supply))} Depot Sources</span>'
        f'<span style="margin-left:auto;font-size:0.78rem;color:{TEXT_MUTED};">'
        f'{len([o for o in supply if o["feasible"]])} of {len(supply)} depots SLA-feasible</span>'
        f'</div>'
        f'<div style="overflow-x:auto;">'
        f'<table class="ent-table"><thead><tr>'
        f'<th>#</th><th>Depot Port</th><th>Country</th><th>SLA Status</th>'
        f'<th>Avail TEU</th><th>Coverage</th><th>Distance</th>'
        f'<th>Transit</th><th>Cost/TEU</th><th>CO₂</th>'
        f'</tr></thead><tbody>{depot_rows}</tbody></table></div>'
        f'<div style="margin-top:0.6rem;">'
        + "".join(
            f'<div style="font-size:0.78rem;color:{TEXT_MUTED};padding:0.12rem 0;">'
            f'<span style="color:{MAERSK_TEAL};font-weight:600;">▸</span> {opt.get("reasoning","")}</div>'
            for opt in supply[:3] if opt.get("reasoning")
        ) +
        f'</div></div>',
        unsafe_allow_html=True,
    )
    _status("Route Optimisation", 68, ["Demand Intelligence","Inventory Discovery"])

    # ══ AGENT 3 ══
    _push([
        "─────────────────────────────────────────────────",
        " STEP 3 / 3  —  ROUTE OPTIMISATION AGENT",
        "─────────────────────────────────────────────────",
    ], delay=0.07)

    opt_result = optimizer.run(
        routes=None,
        weight_profile=st.session_state.weight_profile,
        teu_needed=demand["teu_required"],
    )
    _push(opt_result["stream_lines"], delay=0.05)
    _push(["", "  ✓ Route Optimisation complete", ""], delay=0.06)
    time.sleep(0.35)

    ranked = opt_result["ranked_routes"]
    top    = opt_result["top_route"]
    w      = opt_result["weights"]
    opt_rows = "".join(
        f'<tr class="rank-{r["rank"]}">'
        f'<td><strong>#{r["rank"]}</strong></td>'
        f'<td>{r["from_port"]}</td>'
        f'<td>{r.get("vessel","—").replace("MV ","")}</td>'
        f'<td style="color:{MAERSK_BLUE};font-weight:600;">${r["cost_per_teu"]:,}</td>'
        f'<td style="color:{INFO};">{r.get("co2_kilotons",0):.3f} Kt</td>'
        f'<td style="color:{SUCCESS if r["sla_pct"]>=95 else WARNING};">{r["sla_pct"]}%</td>'
        f'<td style="font-weight:700;color:{"#16A34A" if r["_final"]>=85 else "#D97706" if r["_final"]>=70 else "#DC2626"};">'
        f'{r["_final"]:.1f}</td>'
        f'</tr>'
        for r in ranked
    )
    opt_ph.markdown(
        f'<div class="ent-card" style="border-top:3px solid {SUCCESS};">'
        f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.8rem;">'
        f'<span style="background:{SUCCESS};color:#fff;border-radius:6px;padding:3px 9px;font-size:0.72rem;font-weight:700;">✓ STEP 3</span>'
        f'<span style="font-size:0.95rem;font-weight:700;color:{TEXT_H};">🗺️ Route Optimisation — Ranked Recommendations</span>'
        f'<span style="margin-left:auto;font-size:0.78rem;color:{TEXT_MUTED};">'
        f'Profile: {st.session_state.weight_profile} · Cost {int(w["cost"]*100)}% / Carbon {int(w["carbon"]*100)}% / SLA {int(w["sla"]*100)}%'
        f'</span></div>'
        f'<table class="ent-table"><thead><tr>'
        f'<th>#</th><th>Origin Port</th><th>Vessel</th>'
        f'<th>Cost/TEU</th><th>CO₂</th><th>SLA%</th><th>Score</th>'
        f'</tr></thead><tbody>{opt_rows}</tbody></table>'
        f'<div style="margin-top:0.8rem;background:{BG_ALT};border-left:3px solid {SUCCESS};'
        f'padding:0.65rem 0.9rem;border-radius:0 6px 6px 0;">'
        f'<div style="font-size:0.8rem;font-weight:700;color:{SUCCESS};margin-bottom:0.3rem;">RECOMMENDATION: Route #{top["rank"]} — {top["from_port"]}</div>'
        + "".join(
            f'<div style="font-size:0.78rem;color:{TEXT_MUTED};padding:0.1rem 0;">'
            f'<span style="color:{SUCCESS};">▸</span> {r}</div>'
            for r in opt_result["reasoning"]
        ) +
        f'</div></div>',
        unsafe_allow_html=True,
    )

    _push([
        "",
        "═══════════════════════════════════════════════════════════",
        "  ALL 3 AGENTS COMPLETE — PIPELINE SUCCESSFUL",
        f"  Recommendation: Route #{top['rank']} ({top['from_port']})",
        f"  Score: {top['_final']:.1f}/100  ·  Cost: ${top['cost_per_teu']}/TEU  ·  SLA: {top['sla_pct']}%",
        "═══════════════════════════════════════════════════════════",
        "",
        "  Awaiting human approval to dispatch vessel...",
    ], delay=0.07)

    _status("Complete", 100, ["Demand Intelligence","Inventory Discovery","Route Optimisation"])

    st.session_state.demand_result = demand
    st.session_state.opt_result    = opt_result
    st.session_state.console_phase = "complete"
    time.sleep(0.4)
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE — COMPLETE
# ══════════════════════════════════════════════════════════════════════════════
def _console_complete():
    opt    = st.session_state.opt_result
    demand = st.session_state.demand_result
    sc     = DEMAND_SCENARIOS[st.session_state.scenario_key]
    if not opt or not demand:
        st.session_state.console_phase = "setup"
        st.rerun()
        return

    ranked = opt["ranked_routes"]
    top    = opt["top_route"]

    st.markdown(
        f'<div style="background:linear-gradient(90deg,{MAERSK_DARK},#003A5D);'
        f'border-radius:10px;padding:0.8rem 1.3rem;margin-bottom:1rem;'
        f'display:flex;align-items:center;gap:0.8rem;">'
        f'<span style="font-size:1.5rem;">✅</span>'
        f'<div><div style="color:{TEXT_INV};font-weight:700;font-size:0.95rem;">Pipeline Complete — 3/3 Agents Successful</div>'
        f'<div style="color:{MAERSK_TEAL};font-size:0.75rem;">'
        f'Recommendation ready · {sc["label"]}</div></div>'
        f'<div style="margin-left:auto;display:flex;gap:0.6rem;align-items:center;">'
        f'<span style="background:{SUCCESS};color:#fff;padding:3px 10px;border-radius:12px;'
        f'font-size:0.72rem;font-weight:700;">● Analysis Complete</span></div></div>',
        unsafe_allow_html=True,
    )

    co2_after = top.get("co2_kilotons", IMPACT["co2_ai_kilotons"])
    cost_save = BASELINE_STATIC["cost_per_teu"] - top["cost_per_teu"]
    for col, (label, val, color, sub) in zip(st.columns(4), [
        ("Top Route Score", f"{top['_final']:.1f}/100",           MAERSK_BLUE,  f"Via {top['from_port'].split(',')[0]}"),
        ("Cost Saving",     f"${cost_save:,}/TEU",                SUCCESS,       f"Total ${cost_save*top['teu']:,}"),
        ("SLA Confidence",  f"{top['sla_pct']}%",                 SUCCESS if top['sla_pct']>=95 else WARNING, ""),
        ("CO₂ Reduction",   f"{((IMPACT['co2_manual_kilotons']-co2_after)/IMPACT['co2_manual_kilotons']*100):.0f}%", INFO, f"{co2_after:.3f} Kt output"),
    ]):
        with col:
            st.markdown(
                f'<div class="kpi-tile" style="border-top:3px solid {color};">'
                f'<div style="font-size:0.68rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">{label}</div>'
                f'<div style="font-size:1.25rem;font-weight:700;color:{color};margin:0.2rem 0;">{val}</div>'
                f'<div style="font-size:0.7rem;color:{TEXT_MUTED};">{sub}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([5, 4])

    with left:
        st.markdown(f'<span class="sec-header">Ranked Routes — Final Comparison</span>', unsafe_allow_html=True)
        rows = "".join(
            f'<tr class="rank-{r["rank"]}">'
            f'<td><strong>#{r["rank"]}</strong></td><td>{r["from_port"]}</td>'
            f'<td>{r.get("vessel","—").replace("MV ","")}</td>'
            f'<td style="color:{MAERSK_BLUE};font-weight:600;">${r["cost_per_teu"]:,}</td>'
            f'<td style="color:{INFO};">{r.get("co2_kilotons",0):.3f} Kt</td>'
            f'<td style="color:{SUCCESS if r["sla_pct"]>=95 else WARNING};">{r["sla_pct"]}%</td>'
            f'<td style="font-weight:700;color:{"#16A34A" if r["_final"]>=85 else "#D97706"};">{r["_final"]:.1f}</td>'
            f'<td style="font-size:0.72rem;color:{TEXT_MUTED};">{r.get("recommendation","")[:30]}…</td>'
            f'</tr>'
            for r in ranked
        )
        st.markdown(
            f'<div style="overflow-x:auto;">'
            f'<table class="ent-table"><thead><tr>'
            f'<th>#</th><th>Origin</th><th>Vessel</th>'
            f'<th>$/TEU</th><th>CO₂</th><th>SLA%</th><th>Score</th><th>Notes</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        for r in opt["reasoning"]:
            st.markdown(f'<div class="reasoning-block">{r}</div>', unsafe_allow_html=True)

        # Re-rank
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([3,1])
        with c1:
            new_p = st.selectbox("Optimisation Profile", list(WEIGHT_PROFILES.keys()),
                                 index=list(WEIGHT_PROFILES.keys()).index(st.session_state.weight_profile),
                                 key="complete_profile")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Re-Rank →", key="complete_rerank"):
                st.session_state.weight_profile = new_p
                st.session_state.opt_result = _get_optimizer().run(
                    routes=None, weight_profile=new_p, teu_needed=demand["teu_required"])
                st.rerun()

        # FIX 3: Always show the agent execution log ──────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<span class="sec-header">Agent Execution Log</span>', unsafe_allow_html=True)
        saved_lines = st.session_state.get("terminal_lines", [])
        if saved_lines:
            st.markdown(_terminal_html(saved_lines), unsafe_allow_html=True)

    with right:
        st.markdown(f'<span class="sec-header">Route Map — Recommended Sea Lane</span>', unsafe_allow_html=True)
        fig = _build_map(demand["port_id"], ranked, show_demand=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown(
            f'<div class="ent-card" style="border-left:4px solid {SUCCESS};background:{BG_ALT};">'
            f'<div style="font-weight:700;color:{TEXT_H};margin-bottom:0.2rem;">'
            f'✅ Recommendation: Route #{top["rank"]} — {top["from_port"]}</div>'
            f'<div style="font-size:0.82rem;color:{TEXT_MUTED};">'
            f'Score {top["_final"]:.1f}/100 · ${top["cost_per_teu"]}/TEU · '
            f'{top["sla_pct"]}% SLA · {top.get("co2_kilotons",0):.3f} Kt CO₂</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button("✅ Approve & Dispatch Route #1", key="final_approve_btn", use_container_width=True):
            st.session_state.approved_route = top
            st.session_state.console_phase = "approved"
            st.rerun()
        if st.button("↩ Start New Scenario", key="final_reset_btn", use_container_width=True):
            st.session_state.console_phase = "setup"
            st.session_state.demand_result = None
            st.session_state.opt_result = None
            st.session_state.approved_route = None
            st.session_state["terminal_lines"] = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE — APPROVED
# ══════════════════════════════════════════════════════════════════════════════
def _console_approved():
    approved = st.session_state.approved_route
    demand   = st.session_state.demand_result
    opt      = st.session_state.opt_result
    sc       = DEMAND_SCENARIOS[st.session_state.scenario_key]
    if not approved:
        st.session_state.console_phase = "setup"
        st.rerun()
        return

    baseline = BASELINE_STATIC
    co2_after = approved.get("co2_kilotons", IMPACT["co2_ai_kilotons"])
    cost_save = baseline["cost_per_teu"] - approved["cost_per_teu"]
    teu_vol   = approved.get("teu", demand["teu_required"])

    st.markdown(
        f'<div style="background:linear-gradient(90deg,{SUCCESS},#15803D);border-radius:10px;'
        f'padding:1rem 1.5rem;margin-bottom:1rem;display:flex;align-items:center;gap:1rem;">'
        f'<span style="font-size:1.8rem;">✅</span>'
        f'<div><div style="color:#fff;font-weight:700;font-size:1rem;">Vessel Dispatched — Route Approved</div>'
        f'<div style="color:#BBF7D0;font-size:0.8rem;">'
        f'{approved["from_port"]} → {sc["port_name"]} · {teu_vol:,} TEU · '
        f'{approved.get("vessel","—")} · ETA {approved.get("transit_days",2)} days</div></div>'
        f'<div style="margin-left:auto;text-align:right;">'
        f'<div style="color:#fff;font-size:1.1rem;font-weight:700;">{datetime.now().strftime("%H:%M UTC")}</div>'
        f'<div style="color:#BBF7D0;font-size:0.72rem;">{datetime.now().strftime("%d %b %Y")}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<span class="sec-header">Before vs After — Business Impact</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    penalty_avoided = sc["penalty_per_day"] * sc["sla_days"]
    annual_saving   = cost_save * 12 * teu_vol
    co2_saved_t     = (baseline["co2_kilotons"] - co2_after) * 1000

    comparisons = [
        ("Cost per TEU",    f"${baseline['cost_per_teu']:,}",  f"${approved['cost_per_teu']:,}", f"−${cost_save:,}/TEU",  SUCCESS, f"Saves ${cost_save*teu_vol:,} this shipment"),
        ("SLA Compliance",  f"{baseline['sla_pct']}%",          f"{approved['sla_pct']}%",        f"+{approved['sla_pct']-baseline['sla_pct']:.1f}pp", SUCCESS, "Customer commitments secured"),
        ("Decision Speed",  f"{baseline['decision_hours']}+ hrs","~8 minutes",                   "−98% faster",           SUCCESS, "Autonomous vs manual"),
        ("CO₂ Emissions",   f"{baseline['co2_kilotons']:.3f} Kt",f"{co2_after:.3f} Kt",          f"−{co2_saved_t:.0f} t", SUCCESS, "Kilotons CO₂ reduction"),
    ]
    for col, (label, before, after, delta, color, note) in zip(st.columns(4), comparisons):
        with col:
            st.markdown(
                f'<div class="ent-card" style="text-align:center;padding:0.9rem 0.7rem;">'
                f'<div style="font-size:0.68rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">{label}</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.35rem;margin-bottom:0.4rem;">'
                f'<div class="before-tile"><div style="font-size:0.58rem;color:{WARNING};font-weight:700;margin-bottom:0.15rem;">BEFORE</div>'
                f'<div style="font-size:0.85rem;font-weight:700;color:#92400E;">{before}</div></div>'
                f'<div class="after-tile"><div style="font-size:0.58rem;color:{SUCCESS};font-weight:700;margin-bottom:0.15rem;">AFTER</div>'
                f'<div style="font-size:0.85rem;font-weight:700;color:#14532D;">{after}</div></div>'
                f'</div>'
                f'<div style="font-size:1.05rem;font-weight:700;color:{color};">{delta}</div>'
                f'<div style="font-size:0.7rem;color:{TEXT_MUTED};">{note}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Financial & Sustainability Impact</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    for col, (icon, val, label, sub) in zip(st.columns(5), [
        ("💰", f"${cost_save*teu_vol:,}",    "Immediate Savings",       "This shipment"),
        ("📅", f"${penalty_avoided:,}",       "Penalty Avoided",         f"${sc['penalty_per_day']:,}/day × {sc['sla_days']}d"),
        ("📈", f"${annual_saving:,.0f}",      "Est. Annual Saving",      "At deployment scale"),
        ("🌱", f"{co2_saved_t:.0f} tonnes",  "CO₂ Saved",              "vs manual routing"),
        ("⏱️", f"{approved.get('transit_days',2)} days", "Transit ETA", "Port-to-port"),
    ]):
        with col:
            st.markdown(
                f'<div class="kpi-tile"><div style="font-size:1.2rem;">{icon}</div>'
                f'<div style="font-size:1.05rem;font-weight:700;color:{MAERSK_DARK};">{val}</div>'
                f'<div style="font-size:0.72rem;font-weight:600;color:{TEXT_H};">{label}</div>'
                f'<div style="font-size:0.65rem;color:{TEXT_MUTED};">{sub}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 4])

    with left:
        fig2 = go.Figure()
        cats  = ["Cost/TEU ($)", "SLA (%)", "CO₂ (×1000 Kt)"]
        bvals = [baseline["cost_per_teu"], baseline["sla_pct"], baseline["co2_kilotons"]*1000]
        avals = [approved["cost_per_teu"],  approved["sla_pct"],  co2_after*1000]
        fig2.add_trace(go.Bar(name="Before",x=cats,y=bvals,marker_color=WARNING,opacity=0.85))
        fig2.add_trace(go.Bar(name="After (AI)",x=cats,y=avals,marker_color=MAERSK_BLUE,opacity=0.9))
        fig2.update_layout(barmode="group",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            height=250,margin=dict(l=5,r=5,t=20,b=5),
            legend=dict(font=dict(color=TEXT_BODY,size=11)),
            xaxis=dict(gridcolor=BORDER,tickfont=dict(color=TEXT_BODY,size=11)),
            yaxis=dict(gridcolor=BORDER,tickfont=dict(color=TEXT_BODY,size=11)),
            font=dict(family="Segoe UI",color=TEXT_BODY))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        if opt:
            st.markdown(f'<span class="sec-header">Decision Rationale</span>', unsafe_allow_html=True)
            for r in opt["reasoning"]:
                st.markdown(f'<div class="reasoning-block">{r}</div>', unsafe_allow_html=True)

    with right:
        st.markdown(f'<span class="sec-header">Approved Route Map</span>', unsafe_allow_html=True)
        fig = _build_map(demand["port_id"], [approved], show_demand=True, height=450)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↩ New Scenario", key="approved_reset"):
        st.session_state.console_phase = "setup"
        st.session_state.demand_result = None
        st.session_state.opt_result    = None
        st.session_state.approved_route = None
        st.session_state["terminal_lines"] = []
        st.rerun()


def _console_whatif_section():
    st.markdown(f'<span class="sec-header">Scenario Comparison</span>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:0.85rem;color:{TEXT_MUTED};margin-bottom:1rem;">'
        f'Explore how external disruptions affect route recommendations across different scenarios.</div>',
        unsafe_allow_html=True,
    )
    for wi_key, wi in WHATIF_SCENARIOS.items():
        with st.expander(f"⚡ {wi['label']}", expanded=(wi_key=="typhoon")):
            st.markdown(
                f'<div style="font-size:0.85rem;color:#334155;margin-bottom:0.8rem;">{wi["description"]}</div>',
                unsafe_allow_html=True,
            )
            rows = "".join(
                f'<tr class="rank-{r["rank"]}">'
                f'<td>#{r["rank"]}</td><td>{r["from_port"]}</td>'
                f'<td>${r["cost_per_teu"]:,}</td><td>{r.get("co2_kilotons",0):.3f} Kt</td>'
                f'<td>{r["sla_pct"]}%</td><td>{r["xgb_score"]}</td>'
                f'<td style="font-size:0.75rem;color:#334155;">{r["recommendation"][:45]}</td>'
                f'</tr>'
                for r in wi["routes"]
            )
            st.markdown(
                f'<table class="ent-table"><thead><tr>'
                f'<th>#</th><th>Origin</th><th>Cost/TEU</th><th>CO₂</th><th>SLA%</th><th>Score</th><th>Notes</th>'
                f'</tr></thead><tbody>{rows}</tbody></table>',
                unsafe_allow_html=True,
            )


def _console_performance_section():
    """Comprehensive performance metrics with multiple visualizations.
    
    Shows:
    - Key performance indicators (cost, SLA, CO2, time)
    - Before/after comparison charts
    - Detailed route metrics table
    - Cost-benefit analysis
    - Route utilization and efficiency metrics
    """
    st.markdown(f'<span class="sec-header">Key Performance Indicators</span>', unsafe_allow_html=True)
    opt = st.session_state.opt_result
    baseline = BASELINE_STATIC
    demand = st.session_state.demand_result
    
    if not opt:
        st.info("ℹ️ Run agent optimization first to see comprehensive performance metrics.")
        return
    
    top = opt.get("top_route", {})
    alternatives = opt.get("alternatives", [])
    
    # ── Calculate metrics ──────────────────────────────────────────────────────
    cost_baseline = baseline["cost_per_teu"]
    cost_optimized = top.get("cost_per_teu", cost_baseline)
    cost_saved = cost_baseline - cost_optimized
    cost_pct = (cost_saved / cost_baseline * 100) if cost_baseline > 0 else 0
    
    sla_baseline = baseline["sla_pct"]
    sla_optimized = top.get("sla_pct", sla_baseline)
    sla_gain = sla_optimized - sla_baseline
    
    co2_baseline = baseline["co2_kilotons"]
    co2_optimized = top.get("co2_kilotons", co2_baseline)
    co2_saved = co2_baseline - co2_optimized
    
    decision_baseline = baseline["decision_hours"]
    decision_optimized = 8 / 60  # ~8 minutes
    time_saved = decision_baseline - decision_optimized
    
    # ── Total savings for demand ──────────────────────────────────────────────
    teu_volume = demand.get("teu_required", 2000) if demand else 2000
    total_cost_saved = cost_saved * teu_volume
    total_co2_saved = co2_saved * teu_volume / 1000  # convert to metric tons
    
    # ── KPI Tiles ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(
            f'<div class="kpi-tile" style="border-top:4px solid {SUCCESS};">'
            f'<div style="font-size:0.65rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">💰 Cost per TEU</div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:{SUCCESS};">−${cost_saved:,}</div>'
            f'<div style="font-size:0.75rem;color:{TEXT_MUTED};line-height:1.3;">'
            f'<span style="color:{SUCCESS};font-weight:700;">${cost_optimized:,}</span> vs '
            f'<span style="color:{DANGER};">${cost_baseline:,}</span><br>'
            f'<span style="color:{WARNING};">{cost_pct:.1f}% reduction</span></div></div>',
            unsafe_allow_html=True,
        )
    
    with c2:
        st.markdown(
            f'<div class="kpi-tile" style="border-top:4px solid {SUCCESS};">'
            f'<div style="font-size:0.65rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">📊 SLA Compliance</div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:{SUCCESS};">+{sla_gain:.1f}%</div>'
            f'<div style="font-size:0.75rem;color:{TEXT_MUTED};line-height:1.3;">'
            f'<span style="color:{SUCCESS};font-weight:700;">{sla_optimized:.1f}%</span> vs '
            f'<span style="color:{DANGER};">{sla_baseline:.1f}%</span><br>'
            f'<span style="color:{INFO};">Reliability improved</span></div></div>',
            unsafe_allow_html=True,
        )
    
    with c3:
        st.markdown(
            f'<div class="kpi-tile" style="border-top:4px solid {INFO};">'
            f'<div style="font-size:0.65rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">🌱 CO₂ Reduction</div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:{INFO};">−{co2_saved:.3f} Kt</div>'
            f'<div style="font-size:0.75rem;color:{TEXT_MUTED};line-height:1.3;">'
            f'<span style="color:{INFO};font-weight:700;">{co2_optimized:.3f}</span> vs '
            f'<span style="color:{DANGER};">{co2_baseline:.3f}</span> Kt<br>'
            f'<span style="color:{SUCCESS};">{total_co2_saved:,.0f} metric tons</span></div></div>',
            unsafe_allow_html=True,
        )
    
    with c4:
        st.markdown(
            f'<div class="kpi-tile" style="border-top:4px solid {MAERSK_BLUE};">'
            f'<div style="font-size:0.65rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">⚡ Decision Time</div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:{MAERSK_BLUE};">−{time_saved:.1f}h</div>'
            f'<div style="font-size:0.75rem;color:{TEXT_MUTED};line-height:1.3;">'
            f'<span style="color:{SUCCESS};font-weight:700;">8 min</span> vs '
            f'<span style="color:{DANGER};">{decision_baseline}+ hrs</span><br>'
            f'<span style="color:{WARNING};">{time_saved/decision_baseline*100:.0f}% faster</span></div></div>',
            unsafe_allow_html=True,
        )
    
    # ── Total Business Impact ──────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Total Business Impact (This Shipment)</span>', unsafe_allow_html=True)
    
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.metric(
            "Total Cost Savings",
            f"${total_cost_saved:,.0f}",
            f"{cost_pct:.1f}% vs manual",
            delta_color="inverse"
        )
    with ic2:
        st.metric(
            "TEU Volume",
            f"{teu_volume:,}",
            "containers repositioned"
        )
    with ic3:
        st.metric(
            "CO₂ Avoided",
            f"{total_co2_saved:,.0f} t",
            f"{total_co2_saved/total_cost_saved*1000 if total_cost_saved > 0 else 0:.2f} t/$1k saved"
        )
    
    # ── Before/After Comparison Chart ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Metric Comparison: Baseline vs Optimized</span>', unsafe_allow_html=True)
    
    cats = ["Cost/TEU\n($)", "SLA\n(% compliance)", "CO₂\n(Kilotons)", "Time\n(minutes)"]
    baseline_vals = [cost_baseline, sla_baseline, co2_baseline * 1000, decision_baseline * 60]
    optimized_vals = [cost_optimized, sla_optimized, co2_optimized * 1000, decision_optimized * 60]
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Baseline",
        x=cats,
        y=baseline_vals,
        marker_color=WARNING,
        opacity=0.75,
        hovertemplate='<b>Baseline</b><br>%{x}<br>Value: %{y:.2f}<extra></extra>'
    ))
    fig_comp.add_trace(go.Bar(
        name="AI Optimised",
        x=cats,
        y=optimized_vals,
        marker_color=SUCCESS,
        opacity=0.9,
        hovertemplate='<b>Optimised</b><br>%{x}<br>Value: %{y:.2f}<extra></extra>'
    ))
    
    fig_comp.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=50, r=20, t=30, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=TEXT_BODY)
        ),
        xaxis=dict(
            gridcolor=BORDER,
            tickfont=dict(color=TEXT_BODY, size=10),
            showgrid=False
        ),
        yaxis=dict(
            gridcolor=BORDER,
            tickfont=dict(color=TEXT_BODY, size=10),
            gridwidth=1
        ),
        font=dict(family="Segoe UI", color=TEXT_BODY)
    )
    
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
    
    # ── Route Ranking Table ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Top Route Options Analyzed</span>', unsafe_allow_html=True)
    
    route_data = []
    for i, route in enumerate([top] + alternatives[:2], 1):
        if route:
            route_data.append({
                "Rank": f"#{i}",
                "Route": f"{route.get('from_port', '—')} → {route.get('to_port', 'DEST')}",
                "Cost/TEU": f"${route.get('cost_per_teu', 0):,}",
                "SLA %": f"{route.get('sla_pct', 0):.1f}%",
                "CO₂ (Kt)": f"{route.get('co2_kilotons', 0):.3f}",
                "Score": f"{route.get('xgb_score', 0):.2f}",
                "Status": "✅ SELECTED" if i == 1 else "—"
            })
    
    if route_data:
        routes_df = pd.DataFrame(route_data)
        st.dataframe(
            routes_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.TextColumn(width="small"),
                "Route": st.column_config.TextColumn(width="large"),
                "Cost/TEU": st.column_config.TextColumn(width="medium"),
                "SLA %": st.column_config.TextColumn(width="small"),
                "CO₂ (Kt)": st.column_config.TextColumn(width="small"),
                "Score": st.column_config.TextColumn(width="small"),
                "Status": st.column_config.TextColumn(width="medium"),
            }
        )
    
    # ── Savings Breakdown ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Value Breakdown</span>', unsafe_allow_html=True)
    
    c_val1, c_val2 = st.columns(2)
    with c_val1:
        st.markdown(
            f'<div class="ent-card">'
            f'<div style="font-size:0.8rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;margin-bottom:0.8rem;">💸 Financial Impact</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.85rem;">'
            f'<div><span style="color:{TEXT_MUTED};">Cost Reduction:</span><br><span style="color:{SUCCESS};font-weight:700;font-size:1.1rem;">${total_cost_saved:,.0f}</span></div>'
            f'<div><span style="color:{TEXT_MUTED};">Per TEU:</span><br><span style="color:{SUCCESS};font-weight:700;font-size:1rem;">−${cost_saved:,}</span></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    with c_val2:
        st.markdown(
            f'<div class="ent-card">'
            f'<div style="font-size:0.8rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;margin-bottom:0.8rem;">♻️ Environmental Impact</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.85rem;">'
            f'<div><span style="color:{TEXT_MUTED};">Total CO₂:</span><br><span style="color:{INFO};font-weight:700;font-size:1.1rem;">−{total_co2_saved:,.0f} t</span></div>'
            f'<div><span style="color:{TEXT_MUTED};">Per Shipment:</span><br><span style="color:{INFO};font-weight:700;font-size:1rem;">−{co2_saved:.3f} Kt</span></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def _sc_console():
    phase = st.session_state.console_phase
    if phase == "setup":       _console_setup()
    elif phase == "running":   _console_running()
    elif phase == "complete":  _console_complete()
    elif phase == "approved":  _console_approved()
    else:
        st.session_state.console_phase = "setup"
        st.rerun()

    # Expandable sections always present after running
    if phase in ("complete", "approved"):
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 What-If Analysis", expanded=False):
            _console_whatif_section()
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📈 Performance Metrics", expanded=False):
            _console_performance_section()


# ══════════════════════════════════════════════════════════════════════════════
#  FLEET MAP TAB
# ══════════════════════════════════════════════════════════════════════════════
def _sc_map():
    st.markdown(f'<span class="sec-header">Live Fleet & Port Network Map</span>', unsafe_allow_html=True)
    fig = go.Figure()
    for pid, p in ATLAS_PORTS.items():
        c = DANGER if p["inv_status"]=="Shortage" else (SUCCESS if p["inv_status"]=="Surplus" else WARNING)
        sym = "triangle-down" if p["inv_status"]=="Shortage" else ("triangle-up" if p["inv_status"]=="Surplus" else "circle")
        fig.add_trace(go.Scattergeo(lat=[p["lat"]],lon=[p["lon"]],mode="markers+text",
            marker=dict(size=10,color=c,symbol=sym,line=dict(width=1,color="white")),
            text=[p["name"].split("(")[0].strip()],textposition="top center",
            textfont=dict(size=8,color=TEXT_BODY),
            hovertext=f"{p['name']}<br>{p['inv_status']}: {p['surplus_teu']:+,} TEU",
            hoverinfo="text",name=p["inv_status"],showlegend=False))
    for v in FLEET_VESSELS:
        fp = ATLAS_PORTS.get(v["from_port"],{})
        tp = ATLAS_PORTS.get(v["to_port"],{})
        if fp and tp:
            mid_lat = (fp["lat"]+tp["lat"])/2
            mid_lon = (fp["lon"]+tp["lon"])/2
            fig.add_trace(go.Scattergeo(
                lat=[fp["lat"],mid_lat,tp["lat"]],lon=[fp["lon"],mid_lon,tp["lon"]],
                mode="lines",line=dict(width=1.5,color=MAERSK_BLUE,dash="dot"),
                opacity=0.5,hoverinfo="skip",showlegend=False))
            fig.add_trace(go.Scattergeo(lat=[mid_lat],lon=[mid_lon],mode="markers",
                marker=dict(size=10,color=MAERSK_BLUE,symbol="diamond",line=dict(width=1,color="white")),
                hovertext=f"{v['vessel']}<br>Route: {v['from_port']}→{v['to_port']}<br>Empty: {v['empty_teu']:,} TEU",
                hoverinfo="text",showlegend=False))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=0,b=0),height=560,
        geo=dict(projection_type="natural earth",showland=True,landcolor="#E8EDF3",
                 showocean=True,oceancolor="#D4E8F7",showcoastlines=True,
                 coastlinecolor="#B0BEC5",showcountries=True,countrycolor="#CBD5E1",
                 showlakes=True,lakecolor="#D4E8F7",bgcolor="rgba(0,0,0,0)"),
        font=dict(family="Segoe UI",color=TEXT_BODY))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})
    c1,c2,c3 = st.columns(3)
    for col,(color,sym,label) in zip([c1,c2,c3],[
        (DANGER,"▼","Shortage Port"),(SUCCESS,"▲","Surplus Port"),(MAERSK_BLUE,"◆","Active Vessel")]):
        with col:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;font-size:0.82rem;color:{TEXT_MUTED};">'
                f'<span style="color:{color};font-size:1rem;">{sym}</span><span>{label}</span></div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  WHAT-IF TAB
# ══════════════════════════════════════════════════════════════════════════════
def _sc_whatif():
    st.markdown(f'<span class="sec-header">What-If Scenario Analysis</span>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:0.85rem;color:{TEXT_MUTED};margin-bottom:1rem;">'
        f'Explore how external disruptions affect route recommendations — compare outcomes across disruption types.</div>',
        unsafe_allow_html=True,
    )
    for wi_key, wi in WHATIF_SCENARIOS.items():
        with st.expander(f"⚡ {wi['label']}", expanded=(wi_key=="typhoon")):
            st.markdown(
                f'<div style="font-size:0.85rem;color:#334155;margin-bottom:0.8rem;">{wi["description"]}</div>',
                unsafe_allow_html=True,
            )
            rows = "".join(
                f'<tr class="rank-{r["rank"]}">'
                f'<td>#{r["rank"]}</td><td>{r["from_port"]}</td>'
                f'<td>${r["cost_per_teu"]:,}</td><td>{r.get("co2_kilotons",0):.3f} Kt</td>'
                f'<td>{r["sla_pct"]}%</td><td>{r["xgb_score"]}</td>'
                f'<td style="font-size:0.75rem;color:#334155;">{r["recommendation"][:45]}</td>'
                f'</tr>'
                for r in wi["routes"]
            )
            st.markdown(
                f'<table class="ent-table"><thead><tr>'
                f'<th>#</th><th>Origin</th><th>Cost/TEU</th><th>CO₂</th><th>SLA%</th><th>Score</th><th>Notes</th>'
                f'</tr></thead><tbody>{rows}</tbody></table>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
#  PERFORMANCE TAB  — FIX 6: replaced radar with useful charts
# ══════════════════════════════════════════════════════════════════════════════
def _sc_performance():
    st.markdown(f'<span class="sec-header">Performance Analytics</span>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    kpis = [
        ("Cost Reduction", "28%", SUCCESS, f"vs ${BASELINE_STATIC['cost_per_teu']}/TEU baseline"),
        ("SLA Compliance", "97.8%", SUCCESS, f"up from {BASELINE_STATIC['sla_pct']}%"),
        ("Decision Speed", "8 min", MAERSK_BLUE, f"vs {BASELINE_STATIC['decision_hours']}+ hours manual"),
        ("CO₂ Saved",     "53.4%", INFO,  f"{IMPACT['co2_ai_kilotons']:.3f} Kt vs {IMPACT['co2_manual_kilotons']:.3f} Kt"),
    ]
    for col,(label,val,color,sub) in zip([c1,c2,c3,c4],kpis):
        with col:
            st.markdown(
                f'<div class="kpi-tile" style="border-top:3px solid {color};">'
                f'<div style="font-size:0.68rem;color:{TEXT_MUTED};font-weight:700;text-transform:uppercase;">{label}</div>'
                f'<div style="font-size:1.7rem;font-weight:700;color:{color};">{val}</div>'
                f'<div style="font-size:0.72rem;color:{TEXT_MUTED};">{sub}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    np.random.seed(42)
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    left, right = st.columns(2)

    with left:
        # SLA compliance trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=np.random.uniform(72,88,12).round(1),
            name="Manual Baseline", line=dict(color=WARNING,width=2,dash="dash"),
            mode="lines+markers", marker=dict(size=5)))
        fig.add_trace(go.Scatter(x=months, y=np.random.uniform(92,99,12).round(1),
            name="AI Optimised", line=dict(color=SUCCESS,width=2.5),
            mode="lines+markers", marker=dict(size=5),
            fill="tonexty", fillcolor="rgba(22,163,74,0.08)"))
        fig.update_layout(title="SLA Compliance Rate (%)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=260, margin=dict(l=5,r=5,t=35,b=5),
            legend=dict(font=dict(color=TEXT_BODY,size=11)),
            xaxis=dict(gridcolor=BORDER,tickfont=dict(color=TEXT_BODY,size=10)),
            yaxis=dict(gridcolor=BORDER,tickfont=dict(color=TEXT_BODY,size=10),range=[60,102]),
            font=dict(family="Segoe UI",color=TEXT_BODY))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        # Manual vs AI — grouped bar across key metrics
        kpi_cats  = ["Cost/TEU ($/10)", "SLA (%)", "Decision (min)", "CO₂ (×10 Kt)"]
        before_v  = [
            round(BASELINE_STATIC["cost_per_teu"] / 10, 1),
            BASELINE_STATIC["sla_pct"],
            BASELINE_STATIC["decision_hours"] * 60,
            round(IMPACT["co2_manual_kilotons"] * 10, 2),
        ]
        after_v   = [
            round(BASELINE_STATIC["cost_per_teu"] * 0.72 / 10, 1),
            97.8,
            8,
            round(IMPACT["co2_ai_kilotons"] * 10, 2),
        ]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Manual", x=kpi_cats, y=before_v,
            marker_color=WARNING, opacity=0.9,
            text=[f"{v:.0f}" for v in before_v], textposition="outside",
            textfont=dict(color=TEXT_BODY, size=10)))
        fig2.add_trace(go.Bar(name="AI Optimised", x=kpi_cats, y=after_v,
            marker_color=MAERSK_BLUE, opacity=0.9,
            text=[f"{v:.0f}" for v in after_v], textposition="outside",
            textfont=dict(color=TEXT_BODY, size=10)))
        fig2.update_layout(
            barmode="group",
            title="Manual vs AI — Key Metrics (normalised)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=260, margin=dict(l=5,r=5,t=38,b=5),
            legend=dict(font=dict(color=TEXT_BODY,size=11)),
            xaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
            yaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
            font=dict(family="Segoe UI",color=TEXT_BODY))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ── Row 2: cost trend + CO₂ quarterly ──────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    left2, right2 = st.columns(2)
    np.random.seed(7)

    with left2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=months, y=np.random.uniform(780,900,12).round(0),
            name="Manual Routing", line=dict(color=WARNING,width=2,dash="dash"),
            mode="lines+markers", marker=dict(size=5)))
        fig3.add_trace(go.Scatter(x=months, y=np.random.uniform(560,650,12).round(0),
            name="AI Optimised", line=dict(color=MAERSK_BLUE,width=2.5),
            mode="lines+markers", marker=dict(size=5),
            fill="tonexty", fillcolor="rgba(0,119,182,0.07)"))
        fig3.update_layout(title="Cost per TEU Trend ($)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=255, margin=dict(l=5,r=5,t=35,b=5),
            legend=dict(font=dict(color=TEXT_BODY,size=11)),
            xaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
            yaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
            font=dict(family="Segoe UI",color=TEXT_BODY))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with right2:
        quarters  = ["Q1","Q2","Q3","Q4"]
        co2_man   = [round(x,3) for x in np.random.uniform(0.018,0.024,4)]
        co2_ai    = [round(x,3) for x in np.random.uniform(0.008,0.012,4)]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Manual CO₂ (Kt)", x=quarters, y=co2_man,
            marker_color=DANGER, opacity=0.85,
            text=[f"{v:.3f}" for v in co2_man], textposition="outside",
            textfont=dict(color=TEXT_BODY,size=10)))
        fig4.add_trace(go.Bar(name="AI CO₂ (Kt)", x=quarters, y=co2_ai,
            marker_color=MAERSK_TEAL, opacity=0.9,
            text=[f"{v:.3f}" for v in co2_ai], textposition="outside",
            textfont=dict(color=TEXT_BODY,size=10)))
        fig4.update_layout(title="CO₂ Emissions by Quarter (Kt)",
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=255, margin=dict(l=5,r=5,t=35,b=5),
            legend=dict(font=dict(color=TEXT_BODY,size=11)),
            xaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
            yaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
            font=dict(family="Segoe UI",color=TEXT_BODY))
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    # ── Row 3: depot utilisation stacked bars ───────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Depot Utilisation by Region</span>', unsafe_allow_html=True)
    np.random.seed(99)
    regions = ["Asia Pacific","South Asia","Middle East","Europe","Americas"]
    fig5 = go.Figure()
    for label, color, vals in [
        ("Full (≥90%)",  SUCCESS,    np.random.randint(30, 55, 5)),
        ("Medium (50-90%)", WARNING, np.random.randint(20, 35, 5)),
        ("Low (<50%)",   DANGER,     np.random.randint(5,  20, 5)),
    ]:
        fig5.add_trace(go.Bar(name=label, x=regions, y=vals,
            marker_color=color, opacity=0.9))
    fig5.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=240, margin=dict(l=5,r=5,t=15,b=5),
        legend=dict(font=dict(color=TEXT_BODY,size=11), orientation="h", y=1.1),
        xaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10)),
        yaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT_BODY,size=10), title="Depots"),
        font=dict(family="Segoe UI",color=TEXT_BODY))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS TAB
# ══════════════════════════════════════════════════════════════════════════════
def _sc_settings():
    st.markdown(f'<span class="sec-header">Demand Scenario Selection</span>', unsafe_allow_html=True)
    
    st.markdown(f"""
<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;padding:1.2rem;margin-bottom:1.5rem;">
    <div style="font-size:0.95rem;color:{TEXT_BODY};line-height:1.6;">
        Select a demand scenario to trigger. When you click the <strong>"Trigger"</strong> button on the Overview page, 
        the selected scenario will be used to generate the alert and proceed to the Agent Console for optimization.
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Get all demand scenarios
    scenario_keys = list(DEMAND_SCENARIOS.keys())
    scenario_labels = {k: DEMAND_SCENARIOS[k].get("label", k) for k in scenario_keys}
    
    # Create display list with scenario details
    scenario_options = []
    for key in scenario_keys:
        sc = DEMAND_SCENARIOS[key]
        label = f"{sc.get('label', key)} — {sc.get('port_name', 'Unknown')} ({sc.get('teu_required', 0):,} TEUs)"
        scenario_options.append((key, label))
    
    # Display current selection
    st.markdown(f'<span class="sec-header">Currently Selected</span>', unsafe_allow_html=True)
    current_scenario = st.session_state.scenario_key
    current_sc_data = DEMAND_SCENARIOS.get(current_scenario, {})
    
    st.markdown(f"""
<div class="ent-card" style="border-left:3px solid {MAERSK_BLUE};">
    <div style="font-size:1rem;font-weight:700;color:{TEXT_H};margin-bottom:0.5rem;">
        {current_sc_data.get('label', current_scenario)}
    </div>
    <div style="font-size:0.9rem;color:{TEXT_BODY};margin-bottom:0.8rem;line-height:1.5;">
        {current_sc_data.get('description', 'No description available')}
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;font-size:0.85rem;">
        <div>
            <div style="color:{TEXT_MUTED};font-size:0.75rem;margin-bottom:0.3rem;">Port</div>
            <div style="font-weight:600;color:{TEXT_H};">{current_sc_data.get('port_name', '—').split('(')[0].strip()}</div>
        </div>
        <div>
            <div style="color:{TEXT_MUTED};font-size:0.75rem;margin-bottom:0.3rem;">TEU Required</div>
            <div style="font-weight:600;color:{MAERSK_BLUE};">{current_sc_data.get('teu_required', 0):,}</div>
        </div>
        <div>
            <div style="color:{TEXT_MUTED};font-size:0.75rem;margin-bottom:0.3rem;">Urgency</div>
            <div style="font-weight:600;color:{DANGER};">{current_sc_data.get('urgency', '—')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="sec-header">Change Scenario</span>', unsafe_allow_html=True)
    
    # Scenario selector
    selected_key = st.selectbox(
        "Available Demand Scenarios",
        options=[opt[0] for opt in scenario_options],
        format_func=lambda k: scenario_options[[opt[0] for opt in scenario_options].index(k)][1],
        index=[opt[0] for opt in scenario_options].index(current_scenario),
        key="settings_scenario_selector",
    )
    
    if selected_key != current_scenario:
        st.session_state.scenario_key = selected_key
        st.success(f"✅ Scenario changed to: {DEMAND_SCENARIOS[selected_key].get('label', selected_key)}")
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 You can now go to the Overview page and click **Trigger** to generate an alert based on the selected demand scenario.")


# ══════════════════════════════════════════════════════════════════════════════
#  CONTAINER SC PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def page_container_sc():
    """Container SC page with state-based tab routing (no st.radio).
    
    Tab switching is handled purely through st.session_state.sc_tab.
    Buttons update this state and trigger st.rerun() for clean UI sync.
    """
    # Initialize sc_tab if not set
    if "sc_tab" not in st.session_state:
        st.session_state.sc_tab = "overview"
    
    # Render tab buttons at the top
    _render_sc_tabs_buttons()
    
    st.markdown("<br>", unsafe_allow_html=True)
    tab = st.session_state.sc_tab
    
    # ── Demand Alert Card (Only on Overview) ─────────────────────────────────
    alert = st.session_state.get("active_alert")
    if tab == "overview" and alert and st.session_state.get("alert_visible", False):
        st.markdown(f'''
<div style="
    background:{DANGER};
    border-radius:10px;padding:1.2rem;
    border:2px solid {WARNING};box-shadow:0 4px 15px rgba(220,38,38,0.3);
    margin-bottom:1rem;
">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="display:flex;align-items:center;gap:1rem;flex:1;">
            <span style="font-size:2rem;">⚠️</span>
            <div style="color:#fff;">
                <div style="font-size:1.05rem;font-weight:700;">{alert["port_name"]}</div>
                <div style="font-size:0.9rem;color:#FCA5A5;margin-top:0.3rem;font-weight:600;">{alert["shortage_teu"]:,} TEU shortage</div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="padding:0.4rem 1rem;background:rgba(255,255,255,0.2);border-radius:6px;color:#fff;font-weight:700;margin-bottom:0.5rem;">
                {alert["urgency_level"]}
            </div>
        </div>
    </div>
</div>''', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("❌ Dismiss", use_container_width=True, key="dismiss_alert_btn"):
                st.session_state.alert_visible = False
                st.rerun()
        with col2:
            if st.button("🚀 Go to Console", use_container_width=True, key="go_console_btn"):
                # Direct state update — no flag needed with button-based nav
                st.session_state.sc_tab = "console"
                st.session_state.console_phase = "setup"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Route to appropriate page based on current tab ──────────────────────────
    if tab == "overview":
        _sc_overview()
    elif tab == "console":
        _sc_console()
    elif tab == "settings":
        _sc_settings()
    else:
        # Safety fallback
        st.session_state.sc_tab = "overview"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    _init_state()
    _render_topnav()
    page = st.session_state.page
    if page == "home":
        page_home()
    elif page == "container_sc":
        page_container_sc()
    else:
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    main()