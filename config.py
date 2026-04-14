# ============================================================
# config.py — TCS ATLAS v3.0  |  Maersk Enterprise Portal
# TCS Crystallus × A.P. Moller-Maersk
# ============================================================

ATLAS_VERSION  = "3.0"
SYSTEM_NAME    = "TCS ATLAS"
CLIENT_NAME    = "A.P. Moller-Maersk"
PLATFORM_NAME  = "TCS Crystallus"
SYSTEM_FULL    = "Autonomous Transport Logistics Agent System"

# ── Network Scale ──────────────────────────────────────────
NETWORK_PORTS      = 524
NETWORK_COUNTRIES  = 130
TOTAL_VESSELS      = 737
DEPOT_LOCATIONS    = 68
GLOBAL_EMPTY_TEUS  = 1_247_000

# ══════════════════════════════════════════════════════════
#  MAERSK ENTERPRISE LIGHT THEME
# ══════════════════════════════════════════════════════════
MAERSK_DARK    = "#00243D"   # header / brand dark
MAERSK_BLUE    = "#0077B6"   # primary CTA / active
MAERSK_LIGHT   = "#42B4E6"   # hover / secondary accent
MAERSK_TEAL    = "#00B4D8"   # live indicators / progress

BG_PAGE        = "#F5F7FA"
BG_CARD        = "#FFFFFF"
BG_SIDEBAR     = "#FFFFFF"
BG_ALT         = "#EEF4FA"
BG_DARK_CARD   = "#00243D"

TEXT_H         = "#00243D"
TEXT_BODY      = "#1E293B"
TEXT_MUTED     = "#64748B"
TEXT_CAPTION   = "#94A3B8"
TEXT_INV       = "#FFFFFF"

BORDER         = "#E2E8F0"
BORDER_STRONG  = "#CBD5E1"

SUCCESS        = "#16A34A"
WARNING        = "#D97706"
DANGER         = "#DC2626"
INFO           = "#0077B6"

# ══════════════════════════════════════════════════════════
#  5 USE CASE DEFINITIONS  (no internal IDs on the UI)
# ══════════════════════════════════════════════════════════
USE_CASES = [
    {
        "id": "control_tower",
        "title": "Control Tower",
        "domain": "Supply Chain & Logistics",
        "short": "Real-time global visibility & autonomous disruption management",
        "description": (
            "Provides end-to-end real-time visibility across Maersk's global network. "
            "Autonomous disruption detection, multi-tier SLA monitoring, and intelligent "
            "alerting across 524 ports and 47 tracked vessels."
        ),
        "annual_value": "$180M+",
        "icon": "🗼",
        "active": False,
        "status": "Preview",
        "color": "#00B4D8",
        "features": [
            "Real-time vessel positioning across 524 ports",
            "Autonomous disruption detection & multi-tier alerting",
            "Predictive SLA breach risk scoring",
            "Integrated weather, geopolitical & congestion feeds",
        ],
        "kpis": [("Vessels Tracked", "47"), ("Alert Response", "< 5 min"), ("Uptime", "99.1%")],
    },
    {
        "id": "aiops",
        "title": "AIOps",
        "domain": "IT & Infrastructure Operations",
        "short": "Auto root cause analysis & self-healing system management",
        "description": (
            "Auto root cause analysis and self-healing workflows reducing mean time "
            "to resolution by 70% across Maersk's global IT estate of 300+ monitored systems."
        ),
        "annual_value": "$100M+",
        "icon": "🔧",
        "active": False,
        "status": "Preview",
        "color": "#8B5CF6",
        "features": [
            "Automated root cause analysis across 300+ systems",
            "Self-healing remediation workflows",
            "Predictive capacity forecasting",
            "Intelligent incident triage & escalation",
        ],
        "kpis": [("MTTR Reduction", "70%"), ("Systems Monitored", "300+"), ("Auto-Resolved", "68%")],
    },
    {
        "id": "container_sc",
        "title": "Container Supply Chain",
        "domain": "Container & Supply Chain",
        "short": "Autonomous empty container repositioning & demand fulfilment",
        "description": (
            "Generative disruption simulation and autonomous repositioning of empty containers "
            "across the global Maersk network. Multi-agent decision intelligence reduces "
            "cost per TEU by 28% and SLA compliance from 62% to 97.8%."
        ),
        "annual_value": "$250M+",
        "icon": "📦",
        "active": True,
        "status": "Live",
        "color": "#0077B6",
        "features": [
            "Demand forecasting with scenario simulation",
            "Autonomous depot selection & route optimisation",
            "Multi-agent processing with explainable decisions",
            "Before/after route performance comparison",
        ],
        "kpis": [("Cost Reduction", "28%"), ("SLA Compliance", "97.8%"), ("Decision Time", "8 min")],
    },
    {
        "id": "fuel_opt",
        "title": "Fuel Optimisation",
        "domain": "Global Fleet Management",
        "short": "Voyage intelligence & autonomous bunkering decisions",
        "description": (
            "Graph Neural Network-powered voyage intelligence and autonomous bunkering "
            "decisions reducing fuel spend and carbon emissions across 737 vessels. "
            "Integrates weather routing, port schedules, and live fuel price feeds."
        ),
        "annual_value": "$300M+",
        "icon": "⛽",
        "active": False,
        "status": "Preview",
        "color": "#16A34A",
        "features": [
            "GNN-powered voyage optimisation",
            "Autonomous bunkering port selection",
            "Weather-integrated dynamic routing",
            "Fleet-wide carbon footprint tracking",
        ],
        "kpis": [("Fuel Reduction", "12%"), ("CO₂ Savings", "53%"), ("Fleet Coverage", "737 vessels")],
    },
    {
        "id": "pricing_ai",
        "title": "Pricing Intelligence",
        "domain": "Commercial Operations",
        "short": "Contract intelligence & real-time surcharge automation",
        "description": (
            "Agentic contract intelligence and real-time surcharge automation compressing "
            "multi-week manual BAF/FFF processes into same-day execution across 1,200+ "
            "active contracts, recovering significant previously lost revenue."
        ),
        "annual_value": "$2.78B+",
        "icon": "💹",
        "active": False,
        "status": "Preview",
        "color": "#D97706",
        "features": [
            "AI contract clause analysis at scale",
            "Real-time BAF/FFF surcharge automation",
            "Rate benchmarking & revenue recovery",
            "Same-day multi-contract execution",
        ],
        "kpis": [("Revenue Impact", "$2.78B"), ("Contracts", "1,200+"), ("Cycle Time", "Same-day")],
    },
]

# ══════════════════════════════════════════════════════════
#  GLOBAL PORT NETWORK  (25 ports)
# ══════════════════════════════════════════════════════════
ATLAS_PORTS = {
    "SGP":   {"name": "Singapore (PSA)",            "country": "Singapore",     "lat":  1.26, "lon": 103.82, "region": "SE Asia",      "berths": 12, "surplus_teu": -3000, "inv_status": "Shortage",  "depot": True},
    "PKG":   {"name": "Port Klang",                 "country": "Malaysia",      "lat":  3.00, "lon": 101.40, "region": "SE Asia",      "berths":  6, "surplus_teu":  1200, "inv_status": "Surplus",   "depot": True},
    "HKG":   {"name": "Hong Kong",                  "country": "China",         "lat": 22.30, "lon": 114.17, "region": "E Asia",       "berths":  8, "surplus_teu":   890, "inv_status": "Surplus",   "depot": True},
    "GZO":   {"name": "Guangzhou (Nansha)",          "country": "China",         "lat": 22.72, "lon": 113.52, "region": "E Asia",       "berths": 10, "surplus_teu":   450, "inv_status": "Balanced",  "depot": True},
    "KHH":   {"name": "Kaohsiung",                  "country": "Taiwan",        "lat": 22.56, "lon": 120.35, "region": "E Asia",       "berths":  7, "surplus_teu":   320, "inv_status": "Surplus",   "depot": True},
    "SHA":   {"name": "Shanghai",                   "country": "China",         "lat": 31.35, "lon": 121.68, "region": "E Asia",       "berths": 14, "surplus_teu": -1000, "inv_status": "Shortage",  "depot": True},
    "PUS":   {"name": "Busan",                      "country": "South Korea",   "lat": 35.10, "lon": 129.04, "region": "E Asia",       "berths":  8, "surplus_teu":   980, "inv_status": "Surplus",   "depot": True},
    "TYO":   {"name": "Tokyo (Tokyo Bay)",           "country": "Japan",         "lat": 35.45, "lon": 139.78, "region": "E Asia",       "berths":  6, "surplus_teu":   210, "inv_status": "Balanced",  "depot": True},
    "CMB":   {"name": "Colombo",                    "country": "Sri Lanka",     "lat":  6.94, "lon":  79.85, "region": "South Asia",   "berths":  5, "surplus_teu":   340, "inv_status": "Surplus",   "depot": True},
    "MUM":   {"name": "Mumbai (JNPT)",              "country": "India",         "lat": 18.93, "lon":  72.84, "region": "South Asia",   "berths":  7, "surplus_teu":   380, "inv_status": "Surplus",   "depot": True},
    "CHT":   {"name": "Chittagong",                 "country": "Bangladesh",    "lat": 22.33, "lon":  91.82, "region": "South Asia",   "berths":  4, "surplus_teu":  -800, "inv_status": "Shortage",  "depot": False},
    "DXB":   {"name": "Dubai (Jebel Ali)",          "country": "UAE",           "lat": 24.99, "lon":  55.06, "region": "Middle East",  "berths":  8, "surplus_teu":  4000, "inv_status": "Surplus",   "depot": True},
    "DJI":   {"name": "Djibouti",                   "country": "Djibouti",      "lat": 11.59, "lon":  43.14, "region": "East Africa",  "berths":  3, "surplus_teu":   150, "inv_status": "Balanced",  "depot": False},
    "MOM":   {"name": "Mombasa",                    "country": "Kenya",         "lat": -4.04, "lon":  39.67, "region": "E Africa",     "berths":  4, "surplus_teu":  -200, "inv_status": "Shortage",  "depot": False},
    "CPT":   {"name": "Cape Town",                  "country": "South Africa",  "lat":-33.93, "lon":  18.42, "region": "S Africa",     "berths":  5, "surplus_teu":   420, "inv_status": "Surplus",   "depot": True},
    "RTM":   {"name": "Rotterdam",                  "country": "Netherlands",   "lat": 51.90, "lon":   4.48, "region": "Europe",       "berths": 10, "surplus_teu":  1000, "inv_status": "Surplus",   "depot": True},
    "HH":    {"name": "Hamburg",                    "country": "Germany",       "lat": 53.53, "lon":   9.97, "region": "Europe",       "berths":  8, "surplus_teu":   760, "inv_status": "Surplus",   "depot": True},
    "ANT":   {"name": "Antwerp",                    "country": "Belgium",       "lat": 51.23, "lon":   4.40, "region": "Europe",       "berths":  7, "surplus_teu":   580, "inv_status": "Surplus",   "depot": False},
    "GIB":   {"name": "Algeciras (Gibraltar)",       "country": "Spain",         "lat": 36.13, "lon":  -5.45, "region": "Europe",       "berths":  5, "surplus_teu":   220, "inv_status": "Balanced",  "depot": False},
    "PSE":   {"name": "Port Said East",             "country": "Egypt",         "lat": 31.26, "lon":  32.32, "region": "Middle East",  "berths":  6, "surplus_teu":  -500, "inv_status": "Shortage",  "depot": False},
    "LAX":   {"name": "Los Angeles",                "country": "USA",           "lat": 33.74, "lon":-118.27, "region": "Americas",     "berths":  8, "surplus_teu":   500, "inv_status": "Surplus",   "depot": True},
    "NYK":   {"name": "New York / New Jersey",       "country": "USA",           "lat": 40.66, "lon": -74.07, "region": "Americas",     "berths":  6, "surplus_teu":   310, "inv_status": "Surplus",   "depot": False},
    "STO":   {"name": "Santos",                     "country": "Brazil",        "lat":-23.96, "lon": -46.32, "region": "Americas",     "berths":  5, "surplus_teu":   280, "inv_status": "Surplus",   "depot": True},
    "VNCMT": {"name": "Ho Chi Minh City (Cai Mep)", "country": "Vietnam",       "lat": 10.60, "lon": 107.00, "region": "SE Asia",      "berths":  4, "surplus_teu": -3500, "inv_status": "Shortage",  "depot": False},
    "MNL":   {"name": "Manila",                     "country": "Philippines",   "lat": 14.52, "lon": 120.97, "region": "SE Asia",      "berths":  4, "surplus_teu":   180, "inv_status": "Balanced",  "depot": False},
}

# ── Depot Inventory ────────────────────────────────────────
DEPOT_INVENTORY = {
    "SGP":  {"vessel": "MV Stellaris Maersk",  "type": "Container Ship", "capacity_teu": 18_000, "available_teu": 1_240, "idle_days": 2},
    "PKG":  {"vessel": "MV Gunhilde Maersk",   "type": "Container Ship", "capacity_teu": 15_500, "available_teu":   620, "idle_days": 0},
    "HKG":  {"vessel": "MV Ane Maersk",        "type": "Container Ship", "capacity_teu": 20_000, "available_teu":   890, "idle_days": 1},
    "GZO":  {"vessel": "MV Edith Maersk",      "type": "Container Ship", "capacity_teu": 15_000, "available_teu":   450, "idle_days": 3},
    "PUS":  {"vessel": "MV Marie Maersk",      "type": "Feeder",         "capacity_teu":  8_500, "available_teu":   980, "idle_days": 1},
    "CMB":  {"vessel": "MV Laura Maersk",      "type": "Container Ship", "capacity_teu": 16_000, "available_teu":   340, "idle_days": 0},
    "SHA":  {"vessel": "MV Evelyn Maersk",     "type": "ULCV",           "capacity_teu": 24_000, "available_teu": 1_100, "idle_days": 2},
    "MUM":  {"vessel": "MV Munkebo Maersk",    "type": "Container Ship", "capacity_teu": 14_000, "available_teu":   380, "idle_days": 4},
    "DXB":  {"vessel": "MV Svend Maersk",      "type": "Container Ship", "capacity_teu": 13_500, "available_teu":   710, "idle_days": 1},
    "RTM":  {"vessel": "MV Gunde Maersk",      "type": "Container Ship", "capacity_teu": 17_000, "available_teu":   560, "idle_days": 0},
    "HH":   {"vessel": "MV Sovereign Maersk",  "type": "Container Ship", "capacity_teu": 16_000, "available_teu":   490, "idle_days": 2},
    "LAX":  {"vessel": "MV Cornelia Maersk",   "type": "Feeder",         "capacity_teu":  9_000, "available_teu":   320, "idle_days": 3},
    "CPT":  {"vessel": "MV Safmarine Kuramo",  "type": "Feeder",         "capacity_teu":  5_500, "available_teu":   180, "idle_days": 1},
}

# ── Fleet Vessels ──────────────────────────────────────────
FLEET_VESSELS = [
    {"id": "V001", "vessel": "MV Gunhilde Maersk",   "type": "Container Ship", "from_port": "PKG",  "to_port": "VNCMT", "cargo_pct": 0.72, "empty_teu": 434,  "total_capacity": 15_500, "original_route": ["PKG","SGP","VNCMT"], "original_eta_days": 2.1, "status": "In Transit", "planned_route": {"from_port": "PKG", "to_port": "VNCMT", "cost_per_teu": 485, "total_cost": 210490, "teu_count": 434, "days_to_arrival": 2}},
    {"id": "V002", "vessel": "MV Stellaris Maersk",  "type": "Container Ship", "from_port": "SGP",  "to_port": "HKG",   "cargo_pct": 0.58, "empty_teu": 756,  "total_capacity": 18_000, "original_route": ["SGP","MNL","HKG"],   "original_eta_days": 3.4, "status": "In Transit", "planned_route": {"from_port": "SGP", "to_port": "HKG", "cost_per_teu": 520, "total_cost": 393120, "teu_count": 756, "days_to_arrival": 3}},
    {"id": "V003", "vessel": "MV Ane Maersk",        "type": "Container Ship", "from_port": "HKG",  "to_port": "SHA",   "cargo_pct": 0.81, "empty_teu": 380,  "total_capacity": 20_000, "original_route": ["HKG","GZO","SHA"],   "original_eta_days": 1.8, "status": "In Transit", "planned_route": {"from_port": "HKG", "to_port": "SHA", "cost_per_teu": 340, "total_cost": 129200, "teu_count": 380, "days_to_arrival": 2}},
    {"id": "V004", "vessel": "MV Marie Maersk",      "type": "Feeder",         "from_port": "PUS",  "to_port": "SHA",   "cargo_pct": 0.44, "empty_teu": 476,  "total_capacity":  8_500, "original_route": ["PUS","SHA"],         "original_eta_days": 2.2, "status": "Idle at Port", "planned_route": {"from_port": "PUS", "to_port": "SHA", "cost_per_teu": 290, "total_cost": 138040, "teu_count": 476, "days_to_arrival": 2}},
    {"id": "V005", "vessel": "MV Evelyn Maersk",     "type": "ULCV",           "from_port": "SHA",  "to_port": "RTM",   "cargo_pct": 0.93, "empty_teu": 168,  "total_capacity": 24_000, "original_route": ["SHA","SGP","CMB","RTM"], "original_eta_days": 22.0, "status": "In Transit", "planned_route": {"from_port": "SHA", "to_port": "RTM", "cost_per_teu": 680, "total_cost": 114240, "teu_count": 168, "days_to_arrival": 22}},
    {"id": "V006", "vessel": "MV Laura Maersk",      "type": "Container Ship", "from_port": "CMB",  "to_port": "DXB",   "cargo_pct": 0.66, "empty_teu": 544,  "total_capacity": 16_000, "original_route": ["CMB","MUM","DXB"],   "original_eta_days": 4.5, "status": "In Transit", "planned_route": {"from_port": "CMB", "to_port": "DXB", "cost_per_teu": 310, "total_cost": 168640, "teu_count": 544, "days_to_arrival": 4}},
]

# ── Customer List ──────────────────────────────────────────
CUSTOMERS = [
    "Vinamilk Vietnam Co., Ltd.",
    "BGMEA Logistics (Bangladesh)",
    "Reliance Industries Ltd.",
    "Samsung Heavy Industries",
    "Suez Canal Authority Partners",
    "COSCO Logistics",
    "Alibaba International Supply Chain",
    "Procter & Gamble Asia Pacific",
    "Unilever Supply Chain",
    "Toyota Logistics Services",
    "Ikea Supply AG",
    "Custom / Enter manually",
]

# ══════════════════════════════════════════════════════════
#  5 DEMAND SCENARIOS
# ══════════════════════════════════════════════════════════
DEMAND_SCENARIOS = {
    "vietnam_surge": {
        "label": "Vietnam Export Surge — Red Sea Disruption",
        "shipper": "Vinamilk Vietnam Co., Ltd.",
        "port_id": "VNCMT",
        "port_name": "Ho Chi Minh City (Cai Mep Terminal)",
        "destination": "Rotterdam, Netherlands",
        "destination_port": "RTM",
        "teu_required": 847,
        "container_mix": "580 × 40' Dry  +  267 × 40' Reefer",
        "cargo": "Dairy products — temperature-controlled export",
        "sla_days": 5,
        "penalty_per_day": 42_000,
        "trigger": "Red Sea Disruption — Regional depot depletion surge",
        "urgency": "CRITICAL",
        "description": (
            "Vinamilk requires urgent container pickup following Red Sea disruptions that "
            "depleted regional depot stock. 847 TEUs needed within 5 days or a $42,000/day "
            "SLA penalty applies."
        ),
    },
    "bangladesh_crisis": {
        "label": "Bangladesh Garment — Cyclone Emergency",
        "shipper": "BGMEA Logistics (Bangladesh)",
        "port_id": "CHT",
        "port_name": "Chittagong Port",
        "destination": "Hamburg, Germany",
        "destination_port": "HH",
        "teu_required": 620,
        "container_mix": "420 × 40' Dry  +  200 × 20' Dry",
        "cargo": "Ready-made garments — export consignment",
        "sla_days": 7,
        "penalty_per_day": 28_000,
        "trigger": "Cyclone Mocha — Bay of Bengal route disruption",
        "urgency": "HIGH",
        "description": (
            "Post-cyclone recovery shipment. 620 TEU garment exports held at Chittagong "
            "pending container availability. 7-day departure window before consignment "
            "penalty applies."
        ),
    },
    "india_shortage": {
        "label": "India West Coast — Port Strike Backlog",
        "shipper": "Reliance Industries Ltd.",
        "port_id": "MUM",
        "port_name": "Mumbai (JNPT — Nhava Sheva)",
        "destination": "Los Angeles, USA",
        "destination_port": "LAX",
        "teu_required": 720,
        "container_mix": "490 × 40' Dry  +  230 × 40' High Cube",
        "cargo": "Petrochemical products & textiles",
        "sla_days": 6,
        "penalty_per_day": 35_000,
        "trigger": "Nhava Sheva port workers strike — container backlog at terminal",
        "urgency": "HIGH",
        "description": (
            "India west coast container deficit following port strike. 720 TEUs urgently "
            "required. Alternative depot sourcing needed to bypass the strike-affected terminal."
        ),
    },
    "korea_electronics": {
        "label": "Korea Electronics — Q4 Holiday Rush",
        "shipper": "Samsung Heavy Industries",
        "port_id": "PUS",
        "port_name": "Busan (Gamcheon Terminal)",
        "destination": "Los Angeles, USA",
        "destination_port": "LAX",
        "teu_required": 550,
        "container_mix": "550 × 40' High Cube",
        "cargo": "Consumer electronics — Q4 holiday shipment",
        "sla_days": 4,
        "penalty_per_day": 55_000,
        "trigger": "Q4 factory production surge — container inventory depleted at Busan",
        "urgency": "CRITICAL",
        "description": (
            "Samsung Q4 holiday shipment. 550 TEU high-cube containers needed at Busan "
            "within 4 days. Strict SLA with $55,000/day penalty for a missed Christmas window."
        ),
    },
    "egypt_suez": {
        "label": "Egypt / Suez Corridor — Canal Restoration",
        "shipper": "Suez Canal Authority Partners",
        "port_id": "PSE",
        "port_name": "Port Said East (Suez Canal Gateway)",
        "destination": "Singapore (PSA)",
        "destination_port": "SGP",
        "teu_required": 900,
        "container_mix": "600 × 40' Dry  +  300 × 40' Reefer",
        "cargo": "Mixed transit containers",
        "sla_days": 8,
        "penalty_per_day": 38_000,
        "trigger": "Suez Canal capacity restoration — northbound congestion clearance needed",
        "urgency": "HIGH",
        "description": (
            "Post-blockage corridor restoration. 900 TEU transit containers required at Port Said "
            "East for onward Asia routing. 8-day window aligned with canal scheduling authority."
        ),
    },
}

# ══════════════════════════════════════════════════════════
#  STATIC BASELINE — FROZEN (never changes after disruption)
# ══════════════════════════════════════════════════════════
BASELINE_STATIC = {
    "repositioning_cost_B": 1.5,
    "sla_pct": 82,
    "decision_time_days": 4.2,
    "active_alerts": 0,
    "cost_per_teu": 412,
    "co2_kilotons": 0.187,      # 187 tonnes = 0.187 Kilotons
    "decision_hours": 72,
    "routes": [
        {
            "rank": 1, "from_port": "Port Klang, Malaysia",
            "vessel": "MV Gunhilde Maersk", "port_id": "PKG",
            "teu": 847, "transit_days": 2.8,
            "cost_per_teu": 412, "total_cost": 348_764,
            "co2_kilotons": 0.187, "sla_pct": 82.3, "score": 71.2,
            "lat_from": 3.00, "lon_from": 101.40,
            "recommendation": "Manual selection — no optimisation applied",
        },
        {
            "rank": 2, "from_port": "Singapore (PSA)",
            "vessel": "MV Stellaris Maersk", "port_id": "SGP",
            "teu": 847, "transit_days": 3.2,
            "cost_per_teu": 485, "total_cost": 410_695,
            "co2_kilotons": 0.213, "sla_pct": 71.4, "score": 62.8,
            "lat_from": 1.26, "lon_from": 103.82,
            "recommendation": "Second option — higher cost, lower SLA",
        },
        {
            "rank": 3, "from_port": "Hong Kong",
            "vessel": "MV Ane Maersk", "port_id": "HKG",
            "teu": 847, "transit_days": 4.1,
            "cost_per_teu": 532, "total_cost": 450_604,
            "co2_kilotons": 0.242, "sla_pct": 58.2, "score": 51.4,
            "lat_from": 22.30, "lon_from": 114.17,
            "recommendation": "Third option — longest transit, SLA at risk",
        },
    ],
}

# ── Pre-computed Optimised Route Options (Vietnam scenario) ──
ROUTE_OPTIONS_BASE = [
    {
        "rank": 1, "port_id": "PKG",
        "vessel": "MV Gunhilde Maersk",
        "from_port": "Port Klang, Malaysia",
        "teu": 847, "distance_km": 1_050, "transit_days": 1.5,
        "cost_per_teu": 298, "total_cost": 252_206,
        "co2_kilotons": 0.087, "sla_pct": 97.8, "xgb_score": 94.2,
        "lat_from": 3.00, "lon_from": 101.40,
        "recommendation": "Optimal — fastest transit, lowest carbon, highest SLA",
    },
    {
        "rank": 2, "port_id": "SGP",
        "vessel": "MV Stellaris Maersk",
        "from_port": "Singapore (PSA)",
        "teu": 847, "distance_km": 1_183, "transit_days": 1.8,
        "cost_per_teu": 312, "total_cost": 264_264,
        "co2_kilotons": 0.098, "sla_pct": 96.1, "xgb_score": 91.8,
        "lat_from": 1.26, "lon_from": 103.82,
        "recommendation": "Strong — high confidence, ample inventory buffer",
    },
    {
        "rank": 3, "port_id": "HKG",
        "vessel": "MV Ane Maersk",
        "from_port": "Hong Kong",
        "teu": 847, "distance_km": 1_685, "transit_days": 2.8,
        "cost_per_teu": 365, "total_cost": 309_055,
        "co2_kilotons": 0.143, "sla_pct": 87.3, "xgb_score": 79.4,
        "lat_from": 22.30, "lon_from": 114.17,
        "recommendation": "Fallback — meets SLA minimum; higher cost & carbon",
    },
]

# ── What-If Scenarios ──────────────────────────────────────
WHATIF_SCENARIOS = {
    "typhoon": {
        "label": "Typhoon — South China Sea",
        "description": "Typhoon Haikui disrupts Port Klang & Singapore. Routes recalculated via alternative depots.",
        "routes": [
            {"rank": 1, "port_id": "HKG", "vessel": "MV Ane Maersk",     "from_port": "Hong Kong",     "teu": 847, "distance_km": 1685, "transit_days": 2.8, "cost_per_teu": 365, "total_cost": 308_955, "co2_kilotons": 0.143, "sla_pct": 92.1, "xgb_score": 86.3, "lat_from": 22.30, "lon_from": 114.17, "recommendation": "Best available under typhoon conditions"},
            {"rank": 2, "port_id": "CMB", "vessel": "MV Laura Maersk",   "from_port": "Colombo",       "teu": 340, "distance_km": 2247, "transit_days": 3.5, "cost_per_teu": 287, "total_cost": 244_969, "co2_kilotons": 0.163, "sla_pct": 87.4, "xgb_score": 79.1, "lat_from": 6.94,  "lon_from":  79.85, "recommendation": "Partial — 340 TEU; supplementary vessel needed"},
            {"rank": 3, "port_id": "MUM", "vessel": "MV Munkebo Maersk", "from_port": "Mumbai (JNPT)", "teu": 380, "distance_km": 3120, "transit_days": 4.2, "cost_per_teu": 263, "total_cost": 222_561, "co2_kilotons": 0.187, "sla_pct": 82.1, "xgb_score": 71.2, "lat_from": 18.93, "lon_from":  72.84, "recommendation": "Risk — tight SLA window; expedite loading"},
        ],
    },
    "vessel_delay": {
        "label": "Vessel Delay — MV Gunhilde Maersk",
        "description": "MV Gunhilde Maersk (Port Klang) delayed 3 days due to engine maintenance.",
        "routes": [
            {"rank": 1, "port_id": "SGP", "vessel": "MV Stellaris Maersk", "from_port": "Singapore (PSA)", "teu": 847, "distance_km": 1183, "transit_days": 1.8, "cost_per_teu": 312, "total_cost": 264_264, "co2_kilotons": 0.098, "sla_pct": 96.1, "xgb_score": 91.8, "lat_from": 1.26,  "lon_from": 103.82, "recommendation": "Promoted — Port Klang delayed; Singapore next best"},
            {"rank": 2, "port_id": "GZO", "vessel": "MV Edith Maersk",    "from_port": "Guangzhou",       "teu": 450, "distance_km": 1580, "transit_days": 2.5, "cost_per_teu": 342, "total_cost": 289_530, "co2_kilotons": 0.129, "sla_pct": 89.2, "xgb_score": 83.5, "lat_from": 22.72, "lon_from": 113.52, "recommendation": "Partial — 450 TEU; combine with another depot"},
            {"rank": 3, "port_id": "HKG", "vessel": "MV Ane Maersk",      "from_port": "Hong Kong",       "teu": 847, "distance_km": 1685, "transit_days": 2.8, "cost_per_teu": 365, "total_cost": 309_055, "co2_kilotons": 0.143, "sla_pct": 87.3, "xgb_score": 79.4, "lat_from": 22.30, "lon_from": 114.17, "recommendation": "Fallback — full capacity; higher cost"},
        ],
    },
    "surge_demand": {
        "label": "Surge Demand — +540 TEU Additional Booking",
        "description": "Masan Industries (Vietnam) adds 540 TEU. Total 1,387 TEU. Multi-vessel solution triggered.",
        "routes": [
            {"rank": 1, "port_id": "PKG+SGP", "vessel": "MV Gunhilde + MV Stellaris", "from_port": "Port Klang + Singapore", "teu": 1387, "distance_km": 1120, "transit_days": 1.8, "cost_per_teu": 304, "total_cost": 421_648, "co2_kilotons": 0.131, "sla_pct": 95.4, "xgb_score": 93.1, "lat_from": 3.00,  "lon_from": 101.40, "recommendation": "Multi-vessel — combined PKG(847)+SGP(540); optimal split"},
            {"rank": 2, "port_id": "SGP+GZO", "vessel": "MV Stellaris + MV Edith",   "from_port": "Singapore + Guangzhou",  "teu": 1387, "distance_km": 1380, "transit_days": 2.2, "cost_per_teu": 318, "total_cost": 440_946, "co2_kilotons": 0.158, "sla_pct": 91.8, "xgb_score": 87.4, "lat_from": 1.26,  "lon_from": 103.82, "recommendation": "Alternative — both ports clear of disruption"},
            {"rank": 3, "port_id": "HKG+CMB", "vessel": "MV Ane + MV Laura",         "from_port": "Hong Kong + Colombo",    "teu": 1230, "distance_km": 1970, "transit_days": 3.2, "cost_per_teu": 331, "total_cost": 407_130, "co2_kilotons": 0.215, "sla_pct": 85.6, "xgb_score": 74.8, "lat_from": 22.30, "lon_from": 114.17, "recommendation": "Risk — 157 TEU shortfall; partial delivery"},
        ],
    },
}

# ── Optimisation Weight Profiles ───────────────────────────
WEIGHT_PROFILES = {
    "Balanced":          {"cost": 0.40, "carbon": 0.30, "sla": 0.30},
    "Cost Focus":        {"cost": 0.70, "carbon": 0.15, "sla": 0.15},
    "Carbon Reduction":  {"cost": 0.15, "carbon": 0.70, "sla": 0.15},
    "SLA Priority":      {"cost": 0.15, "carbon": 0.15, "sla": 0.70},
}

# ── Business Impact ────────────────────────────────────────
IMPACT = {
    "annual_value_usd":         250_000_000,
    "response_time_manual":     "72 hours",
    "response_time_ai":         "8 minutes",
    "cost_per_teu_manual":      412,
    "cost_per_teu_ai":          298,
    "co2_manual_kilotons":      0.187,
    "co2_ai_kilotons":          0.087,
    "sla_manual_pct":           62.3,
    "sla_ai_pct":               97.8,
    "carbon_reduction_pct":     53.4,
}

# ── Port Berth Capacity ────────────────────────────────────
PORT_BERTHS = {p: v["berths"] for p, v in ATLAS_PORTS.items() if "berths" in v}

# ── Control Tower Monitor Data ─────────────────────────────
MONITOR_PORTS = ["SGP", "DXB", "RTM", "SHA", "LAX"]

CONTAINER_INVENTORY = {
    "Dry (20ft)":  72,
    "Dry (40ft)":  58,
    "Reefer":      41,
    "In Transit":  65,
}

DATA_SOURCES = [
    "PortSight",
    "AIS Vessel Feed",
    "SAP TM Inventory",
    "Weather Feed",
    "Geopolitical API",
]

# ── Rotating News Items ────────────────────────────────────
NEWS_ITEMS = [
    "Red Sea shipping volumes down 18% — Suez Canal diversions increasing transit costs.",
    "Typhoon Haikui: South China Sea advisory issued for Luzon Strait shipping lanes.",
    "Port Klang berth utilisation at 94% — priority booking strongly recommended.",
    "Maersk Q3: repositioning efficiency up 28% year-on-year vs prior period.",
    "Singapore MPA: new port congestion surcharge effective 1 Nov across all terminals.",
    "Rotterdam strikes called off — normal terminal operations fully resumed.",
    "Shanghai port cleared after delays — 3-day container backlog now processed.",
    "IMO 2025 sulphur cap enforcement: 87% of Maersk fleet now in compliance.",
    "Baltic Dry Index rises 6.2% — bulk carrier demand increasing ahead of Q4.",
    "Container spot rates on Asia-Europe corridor up $220/TEU week-on-week.",
    "Djibouti transshipment hub reporting 12% volume increase — Gulf demand rising.",
    "AIS data: 47 Maersk vessels in active transit; 3 flagged for schedule review.",
]

# ── Demand Alerts ──────────────────────────────────────────
DEMAND_ALERTS = {
    "port_shortage_sgp": {
        "demanding_port": "SGP",
        "port_name": "Singapore (Tuas Port)",
        "shortage_teu": 2400,
        "urgency_level": "HIGH",
        "description": "Peak season surge in import demand; local empty container shortage",
        "candidate_vessels": ["MV Gunhilde Maersk", "MV Stellaris Maersk"],
        "potential_savings": 85000,
        "estimated_lead_time": "8-12 hours",
        "supply_ports": [
            {"port": "HKG", "available_teu": 890, "distance_nm": 1200},
            {"port": "PUS", "available_teu": 980, "distance_nm": 1500},
        ]
    },
    "port_shortage_vncmt": {
        "demanding_port": "VNCMT",
        "port_name": "Ho Chi Minh City (Cai Mep Terminal)",
        "shortage_teu": 3500,
        "urgency_level": "CRITICAL",
        "description": "Red Sea disruption causing export surge; containers urgently needed",
        "candidate_vessels": ["MV Gunhilde Maersk", "MV Ane Maersk"],
        "potential_savings": 125000,
        "estimated_lead_time": "6-10 hours",
        "supply_ports": [
            {"port": "PKG", "available_teu": 1200, "distance_nm": 800},
            {"port": "SGP", "available_teu": 1240, "distance_nm": 650},
        ]
    },
    "port_shortage_sha": {
        "demanding_port": "SHA",
        "port_name": "Shanghai (Yangshan Port)",
        "shortage_teu": 1000,
        "urgency_level": "HIGH",
        "description": "Post-holiday inventory depletion at Shanghai; immediate replenishment needed",
        "candidate_vessels": ["MV Ane Maersk", "MV Marie Maersk"],
        "potential_savings": 52000,
        "estimated_lead_time": "12-16 hours",
        "supply_ports": [
            {"port": "HKG", "available_teu": 890, "distance_nm": 700},
            {"port": "PUS", "available_teu": 980, "distance_nm": 600},
        ]
    },
}
