# TCS ATLAS v3.0 — Empty Container Repositioning System

## Comprehensive Implementation Prompt for Claude AI

---

## PROBLEM STATEMENT & NARRATIVE FOCUS

**Core Problem Being Solved:**
A.P. Moller-Maersk manages 1.2M+ empty TEUs (Twenty-Foot Equivalent Units) across 524 global ports. Without intelligent repositioning:

- Manual repositioning takes 20+ hours per decision
- SLA compliance drops to 62%
- Unnecessary repositioning costs $180M+ annually
- CO₂ emissions from empty container movements are inefficient

**Solution:** TCS ATLAS autonomous agent system intelligently matches empty container supply (surplus ports) with demand (shortage ports), optimizing routes in real-time by cost, SLA, and sustainability.

**User Journey:** Business professionals should understand this problem instantly and see:

1. Current network imbalance (shortage/surplus ports)
2. Immediate supply chain opportunity (demand alert)
3. Agent-driven optimization in real-time
4. Results comparison (planned vs optimized routes)
5. Performance metrics aligned to business KPIs

---

## ARCHITECTURAL CHANGES REQUIRED

### 1. PAGE STRUCTURE CONSOLIDATION

**Current State:** 5 separate pages (Overview, Agent Console, Fleet Map, What-If, Performance)
**Target State:** 3 main pages (Overview, Agent Console, Performance)

```
HOME PAGE
    ↓
CONTAINER SUPPLY CHAIN (Main Page)
    ├─ Overview Tab
    │   ├─ Network Status (shortage/surplus ports)
    │   ├─ Active Fleet with Planned Routes
    │   ├─ Fleet Map (INLINE — moved from separate page)
    │   ├─ Demand Alert (TRIGGER BUTTON RESULT)
    │   └─ Agent Trigger Button
    │
    ├─ Agent Console Tab
    │   ├─ Setup Phase (demand details)
    │   ├─ Running Phase (agent execution progress)
    │   ├─ Complete Phase (results with 3 optimized routes)
    │   ├─ Approved Phase (before/after comparison)
    │   ├─ [WHAT-IF BUTTON] - Expandable section within console
    │   └─ [PERFORMANCE BUTTON] - Expandable section within console
    │
    └─ Performance Tab (still separate, but also accessible via button in console)
```

---

## DETAILED REQUIREMENTS

### REQUIREMENT 1: Integrate Fleet Map into Overview Page

**Location:** Override the "Active Fleet" section entirely
**Old Structure:**

```
Active Fleet (table only)
├─ Vessel Name
├─ Route
├─ Empty TEU
└─ Status
```

**New Structure:**

```
Active Fleet Section
├─ [PLANNED ROUTES VISUALIZATION]
│  └─ Interactive Plotly map showing:
│     • Port network with surplus/shortage indicators
│     • Current vessel routes with empty TEU counts
│     • Planned routes for each vessel (BEFORE optimization)
│
└─ [PLANNED ROUTES TABLE BELOW MAP]
   ├─ Vessel Name
   ├─ Planned Route (from "planned_route" field in data)
   ├─ Empty TEU
   ├─ Status
   └─ Cost/TEU (from baseline plan)
```

**Data Model Changes Needed:**

- Add `"planned_route"` field to `FLEET_VESSELS` for each vessel's baseline/original plan
- Structure: `"planned_route": {"from_port": "SGP", "to_port": "SHGH", "cost_per_teu": 450, "teu_planned": 1200}`

**Map Functionality:**

- Same Plotly geo-scatter visualization as current Fleet Map page
- Highlight shortage ports (red ▼), surplus ports (green ▲), vessels (blue ◆)
- Interactive tooltips showing port inventory and vessel details

---

### REQUIREMENT 2: Redesign Trigger Button & Alert System

**Current Button:**

```python
st.button("🤖 Open Agent Console →")  # Just navigates
```

**New Button & Alert Flow:**

#### Step 2A: The Trigger Button (Overview Page)

```python
# Button triggers demand alert creation (doesn't just navigate)
st.button("🚀 Trigger Optimization", key="trigger_btn", use_container_width=True)
# On click:
#   1. Select a random SHORTAGE port as "demanding port"
#   2. Create demand alert: {demanding_port, shortage_amount, reason}
#   3. Store in st.session_state.active_alert
#   4. Set st.session_state.sc_tab = "console"
#   5. Auto-rerun (Streamlit handles this)
```

#### Step 2B: Demand Alert Display (Top of Page)

**Location:** Override `page_container_sc()` to show alert at TOP before any tab content

```python
if st.session_state.active_alert:
    alert_data = st.session_state.active_alert
    alert_html = f'''
    <div style="
        background: linear-gradient(135deg, {DANGER} 0%, #991B1B 100%);
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        cursor: pointer;
        border: 2px solid {WARNING};
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
    " onClick="...trigger_alert_click...">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">⚠️</span>
            <div style="flex: 1; color: #fff;">
                <div style="font-size: 1.1rem; font-weight: 700;">
                    PORT SHORTAGE DETECTED: {alert_data['port_name']}
                </div>
                <div style="font-size: 0.85rem; color: #FCA5A5; margin-top: 0.3rem;">
                    {alert_data['shortage_teu']:,} TEU required  |
                    {len(alert_data['candidate_vessels'])} vessels can reposition  |
                    Estimated cost savings: ${alert_data['potential_savings']:,}
                </div>
                <div style="font-size: 0.75rem; color: #DBEAFE; margin-top: 0.5rem;">
                    📍 {alert_data['description']}  •
                    ⏰ {alert_data['urgency_level']} priority
                </div>
            </div>
            <div style="text-align: right; color: #FCA5A5;">
                <div style="font-size: 0.7rem; font-weight: 700;">CLICK TO VIEW DETAILS</div>
                <div style="font-size: 1.3rem; margin-top: 0.5rem;">→</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(alert_html, unsafe_allow_html=True)
```

#### Step 2C: Alert Data Structure

```python
DEMAND_ALERTS = {
    "port_shortage_sgp": {
        "demanding_port": "SGP",  # Singapore
        "port_name": "Singapore (Tuas Port)",
        "shortage_teu": 2400,
        "urgency_level": "HIGH",
        "description": "Peak season surge in import demand; local empty container shortage",
        "candidate_vessels": ["MV Seatrade", "MV Maersk Esseberg"],  # from FLEET_VESSELS
        "potential_savings": 85000,  # $
        "estimated_lead_time": "8-12 hours",
        "supply_ports": [
            {"port": "SHGH", "available_teu": 1500, "distance_nm": 890},  # Shanghai
            {"port": "HK", "available_teu": 900, "distance_nm": 450},     # Hong Kong
        ]
    },
    # More alerts...
}
```

---

### REQUIREMENT 3: Enhanced Active Fleet Table with Planned Routes

**Before Optimization (Baseline):**

```
Vessel Name    | Planned Route           | Empty TEU | Current Status | Plan Cost/TEU
MV Seatrade    | SGP → SHGH             | 1,200     | In Transit     | $450
MV Esseberg    | HK → SHGH              | 900       | In Transit     | $385
```

**After Agent Execution (Show Changed Plans):**
When `st.session_state.opt_result` is populated after agent runs, update table to show:

```
Vessel Name    | Planned Route | ↓ Optimized Route | Empty TEU | Status | Delta ($)
MV Seatrade    | SGP → SHGH   | SGP → SGP (stays) | 1,200     | New    | +$180
MV Esseberg    | HK → SHGH    | HK → SGP          | 900       | Route  | -$2100
```

**Implementation:**

- Add condition in `_sc_overview()`:
  ```python
  if st.session_state.approved_route:  # After optimization
      # Show "Optimized Route" column
      # Highlight cost differences (green = savings, red = additional)
      # Remove old "Open Agent Console" button, replace with update button
  else:  # Before optimization
      # Show only "Planned Route" column
      # Keep "Trigger Optimization" button visible
  ```

**Data Model Addition:**

```python
# In FLEET_VESSELS, add:
{
    "vessel": "MV Seatrade",
    "planned_route": {"from_port": "SGP", "to_port": "SHGH", "cost": 540000, "teu": 1200},
    "from_port": "SGP",
    "to_port": "SHGH",
    "empty_teu": 1200,
    "status": "In Transit"
}
```

---

### REQUIREMENT 4: What-If Analysis as Expandable Section in Agent Console

**Current State:** Separate "⚡ What-If" page with scenario selection

**New State:**

- Move all What-If functionality into Agent Console tab
- Add "What-If Analysis" as EXPANDABLE section at bottom of Agent Console
- Triggered by button: "📊 Run What-If Scenarios"

**Implementation Structure:**

```python
def _sc_console():
    phase = st.session_state.console_phase
    if phase == "setup":       _console_setup()
    elif phase == "running":   _console_running()
    elif phase == "complete":  _console_complete()
    elif phase == "approved":  _console_approved()

    # NEW: What-If Section (always present)
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 What-If Analysis", expanded=False):
        _console_whatif_section()  # Contains all what-if logic
```

**What-If Content:**

```python
def _console_whatif_section():
    st.markdown(f'<span class="sec-header">Scenario Comparison</span>', unsafe_allow_html=True)

    # Show selector for weight profile (Cost vs SLA vs Green)
    weight = st.radio("Optimization Profile",
                     ["💰 Cost-Focused", "⏱️ SLA-Focused", "🌱 Sustainable"],
                     horizontal=True)

    # Show 3 scenario cards:
    # Baseline (current plan)
    # Optimized (agent-selected)
    # What-If (alternative scenario)

    c1, c2, c3 = st.columns(3)
    scenarios = [
        ("Baseline", BASELINE_STATIC, "#94A3B8"),
        ("Agent Selected", st.session_state.opt_result, "#16A34A"),
        ("What-If Scenario", WHATIF_SCENARIOS[weight], "#0077B6")
    ]
    for col, (label, data, color) in zip([c1, c2, c3], scenarios):
        with col:
            st.metric(label, f"${data['cost_per_teu']}/TEU",
                     f"{data['sla_pct']}% SLA",
                     f"{data['co2_kilotons']:.2f} Kt CO₂")
```

**Note:** Remove "⚡ What-If" from `_SC_TABS` and `page_container_sc()`

---

### REQUIREMENT 5: Performance Metrics as Expandable Section in Agent Console

**Current State:** Separate "📈 Performance" page

**New State:**

- Add "Performance Metrics" expandable section in Agent Console
- Also keep separate Performance tab (for detailed analysis)
- Button in console: "📈 View Performance Metrics"

**Implementation:**

```python
def _sc_console():
    # ... existing code ...

    # Existing What-If expander
    with st.expander("📊 What-If Analysis", expanded=False):
        _console_whatif_section()

    # NEW: Performance expander
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📈 Performance Metrics", expanded=False):
        _console_performance_section()  # Simplified version of perf page

def _console_performance_section():
    st.markdown(f'<span class="sec-header">Key Performance Indicators</span>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Cost/TEU Saved", f"${st.session_state.opt_result['cost_per_teu'] - BASELINE_STATIC['cost_per_teu']}",
                      "vs Baseline")
    with c2: st.metric("SLA Improvement", f"+{st.session_state.opt_result['sla_pct'] - BASELINE_STATIC['sla_pct']}%")
    with c3: st.metric("CO₂ Reduction", f"-{(BASELINE_STATIC['co2_kilotons'] - st.session_state.opt_result['co2_kilotons']):.3f} Kt")
    with c4: st.metric("Decision Time", "-18+ hrs", "Automated")

    # Show graph comparing baseline vs optimized
    # Show table of port-by-port improvements
```

**Note:** Keep Performance tab as standalone page in nav (`_SC_TABS` still has "📈 Performance")

---

### REQUIREMENT 6: Agent Console Execution Flow with Run Button

**Current Flow:**

- "Setup" phase → Manual form input → "Running" phase → "Complete" phase

**New Flow with Trigger:**

```
1. USER CLICKS "Trigger Optimization" (Overview)
   ↓
2. DEMAND ALERT CREATED (red banner at top)
   ├─ Demanding port: SGP
   ├─ Shortage: 2,400 TEU
   ├─ Candidate vessels: [MV Seatrade, MV Esseberg]
   ↓
3. AGENT CONSOLE TAB OPENS
   ├─ SETUP PHASE shows alert details
   ├─ Auto-populated form:
   │  ├─ Demanding Port: SGP (from alert)
   │  ├─ Shortage Amount: 2,400 TEU
   │  ├─ Weight Profile: Balanced (dropdown)
   │  ├─ Available Vessels: [MV Seatrade, MV Esseberg] (checkboxes)
   │  └─ [RUN AGENT →] BUTTON
   ↓
4. USER CLICKS "RUN AGENT →"
   ├─ Sets st.session_state.console_phase = "running"
   ├─ Calls agent execution (demand_agent, supply_agent, optimization_agent, congestion_agent)
   ↓
5. RUNNING PHASE
   ├─ Shows real-time agent reasoning/logs
   ├─ Progress indicators for each agent step
   ↓
6. COMPLETE PHASE
   ├─ Shows 3 optimized route options
   ├─ Each route card shows:
   │  ├─ Cost per TEU
   │  ├─ SLA compliance %
   │  ├─ CO₂ emissions
   │  ├─ Route details (vessel, ports, timeline)
   │  └─ [APPROVE THIS ROUTE] button
   ↓
7. APPROVED PHASE
   ├─ Shows final approved route
   ├─ Comparison: baseline vs optimized (before/after)
   ├─ "Update Fleet Plan" button (commits to database)
   ├─ "Run What-If Analysis" expander (available)
   ├─ "View Performance Metrics" expander (available)
```

**Implementation Changes Needed:**

A. Modify `_init_state()` to include:

```python
"active_alert": None,  # Current demand alert
"alert_demanding_port": None,
"alert_shortage_teu": None,
"alert_candidates": [],
```

B. Modify `_console_setup()` to auto-populate from alert:

```python
def _console_setup():
    alert = st.session_state.active_alert

    st.markdown(f"Alert: {alert['port_name']} needs {alert['shortage_teu']} TEU")

    # Form is pre-filled
    selected_weight = st.radio("Weight Profile", ["Cost", "SLA", "Sustainability"])
    selected_vessels = st.multiselect("Vessels", alert['candidate_vessels'],
                                      default=alert['candidate_vessels'])

    if st.button("🚀 Run Agent Optimization →"):
        st.session_state.console_phase = "running"
        st.rerun()
```

---

### REQUIREMENT 7: Narrative & Positioning for Business Professionals

**Goal:** Make the problem & solution immediately obvious
**Locations:**

#### A. HOME PAGE

Replace generic text with:

```
🌍 EMPTY CONTAINER REPOSITIONING CRISIS

Maersk moves 1.2M empty TEUs annually across 524 ports.
Without intelligent repositioning:
  ❌ $180M+ in unnecessary repositioning costs
  ❌ 20+ hours manual decision-making per repositioning
  ❌ 62% SLA compliance (should be 95%+)
  ❌ Massive CO₂ waste from suboptimal routes

THE SOLUTION: TCS ATLAS Autonomous Supply Chain Agent
✅ Real-time demand sensing
✅ Instant supply matching
✅ Autonomous route optimization
✅ 18+ hours faster decision-making
✅ 28-35% cost reduction
✅ 45% lower CO₂ emissions from repositioning
```

#### B. OVERVIEW PAGE (Top Section)

Add "Problem Statement" card:

```python
st.markdown(f'''
<div style="background: linear-gradient(135deg, #FEE2E2 0%, #FFE4E6 100%);
            border: 2px solid {DANGER}; border-radius: 10px; padding: 1.2rem;">
    <div style="font-size: 1.1rem; font-weight: 700; color: #7F1D1D; margin-bottom: 0.5rem;">
        🎯 Today's Challenge
    </div>
    <div style="font-size: 0.9rem; color: #991B1B; line-height: 1.6;">
        Global network has <span style="font-weight: 700;">{shortage_total}K TEU shortage</span>
        and <span style="font-weight: 700;">{surplus_total}K TEU surplus</span>.
        Deploy autonomous agents to reposition {best_match_teu}K TEU across {num_routes} routes,
        saving ${potential_value}M in repositioning costs while meeting SLA targets.
    </div>
</div>
''', unsafe_allow_html=True)
```

#### C. DEMAND ALERT

Alert should explicitly state the business impact:

```
⚠️ PORT SHORTAGE DETECTED: Singapore (Tuas Port)
   2,400 TEU required | HIGH urgency | Peak season demand surge

📊 BUSINESS IMPACT:
   • Revenue at risk: $2.1M without containers
   • Reposition cost (manual): $1.2M
   • Our optimized cost: $285K
   • Net savings: $915K
   • Time to decision: <2 mins (vs 20+ hours manual)
```

#### D. RESULTS COMPARISON (Approved Phase)

Show explicit ROI:

```python
c1, c2 = st.columns(2)

with c1:
    st.markdown(f'<div style="background: #FFF8F0; border: 2px solid {WARNING}; ...>')
    st.markdown(f"**BASELINE (Manual Plan)**")
    st.metric("Cost/TEU", "$540")
    st.metric("SLA", "72%")
    st.metric("Decision Time", "22 hours")

with c2:
    st.markdown(f'<div style="background: #F0FFF4; border: 2px solid {SUCCESS}; ...>')
    st.markdown(f"**AGENT OPTIMIZED**")
    st.metric("Cost/TEU", "$385", "-$155 (-29%)")
    st.metric("SLA", "94%", "+22%")
    st.metric("Decision Time", "2 mins", "-22 hrs")
    st.metric("CO₂", "-0.45 Kt", "-18% emissions")
```

---

## FILE STRUCTURE & MODIFICATIONS

### Files to Modify:

1. **app.py** (Main application)
   - Update CSS: Remove Fleet Map page nav
   - Update `_SC_TABS` navigation dictionary
   - Integrate map into `_sc_overview()`
   - Add alert display logic in `page_container_sc()`
   - Create `_console_whatif_section()` function
   - Create `_console_performance_section()` function
   - Modify button flows with correct callbacks
   - Add problem statement narrative cards

2. **config.py** (Configuration)
   - Add `DEMAND_ALERTS` dictionary with sample alerts
   - Add "planned_route" to each vessel in `FLEET_VESSELS`
   - Update `WHATIF_SCENARIOS` to include weight profiles

3. **\_sc_whatif()** function
   - Move entire logic into `_console_whatif_section()`
   - Remove from standalone page

4. **\_sc_performance()** function
   - Keep standalone page logic intact
   - Extract key metrics into `_console_performance_section()`

### New Data Fields Required:

```python
# FLEET_VESSELS items need:
"planned_route": {
    "from_port": "SHGH",
    "to_port": "SPORE",
    "cost_per_teu": 520,
    "total_cost": 624000,
    "teu_count": 1200,
    "days_to_arrival": 4
}

# New session state keys:
"active_alert": {...}  # Current demand alert object
"alert_timestamp": None  # When alert was triggered
```

---

## USER INTERACTION FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│ HOME PAGE                                                       │
│ (Problem Statement + Solution Overview)                        │
│ [Select Container Supply Chain Use Case] ──────┐               │
└──────────────────────────────────────────────────┼──────────────┘
                                                   │
                                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ OVERVIEW TAB (Default)                                           │
│                                                                  │
│ ⚠️ [PORT SHORTAGE ALERT - if active]                             │
│                                                                  │
│ 📊 Network Status: 5 key ports (shortage/surplus)               │
│ 📍 Fleet Map (Inline)                                            │
│    - Shows port network and current vessel routes               │
│    - Surplus ports (green ▲), Shortage ports (red ▼)            │
│    - Active vessels (blue ◆) with routes                        │
│                                                                  │
│ 📋 Active Fleet Plan                                             │
│    | Vessel    | Planned Route  | ↓ Optimized | TEU  | ¢/TEU  |
│    | Seatrade  | SGP → SHGH     | SGP → SGP   | 1.2K | $385   |
│                                                                  │
│ [🚀 TRIGGER OPTIMIZATION BUTTON]                                │
│                                                                  │
└────┬─────────────────────────────────────────────────────────────┘
     │ Click "Trigger"
     ↓
┌──────────────────────────────────────────────────────────────────┐
│ AGENT CONSOLE TAB (Auto-switch)                                 │
│                                                                  │
│ ⚠️ PORT SHORTAGE ALERT (Top) ◄── Click alert to stay here       │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ SETUP PHASE                                                 │ │
│ │                                                             │ │
│ │ Demanding Port:  SGP                                        │ │
│ │ Shortage:        2,400 TEU                                  │ │
│ │ Weight Profile:  [Balanced ▼]                              │ │
│ │ Vessels:         ☐ MV Seatrade  ☑ MV Esseberg             │ │
│ │                                                             │ │
│ │ [🚀 RUN AGENT OPTIMIZATION →]                              │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ (After Running...)                                               │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ RUNNING PHASE (Real-time logs)                              │ │
│ │ 🤖 Demand agent analyzing... ✓                              │ │
│ │ 🏪 Supply agent finding matches... ✓                        │ │
│ │ 📍 Route optimizer running...                                │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ (After Complete...)                                              │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ COMPLETE PHASE (3 route options)                            │ │
│ │                                                             │ │
│ │ ┌─────┐  ┌─────┐  ┌─────┐                                   │ │
│ │ │ #1  │  │ #2  │  │ #3  │                                   │ │
│ │ │$385 │  │$420 │  │$515 │                                   │ │
│ │ │94%  │  │89%  │  │98%  │                                   │ │
│ │ │[✓]  │  │     │  │     │                                   │ │
│ │ └─────┘  └─────┘  └─────┘                                   │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ (After Approval...)                                              │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ APPROVED PHASE                                              │ │
│ │                                                             │ │
│ │ ✅ Route Approved: SGP → SGP (via vessel repositioning)      │ │
│ │                                                             │ │
│ │ BASELINE → OPTIMIZED COMPARISON                            │ │
│ │ Before: $540/TEU, 72% SLA, 22h decision time              │ │
│ │ After:  $385/TEU, 94% SLA, 2m decision time               │ │
│ │                                                             │ │
│ │ [📊 What-If Analysis ▼]  ← EXPANDABLE                      │ │
│ │ [📈 Performance Metrics ▼] ← EXPANDABLE                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
     │
     ├─ [What-If ▼] expands to show scenario comparison
     └─ [Performance ▼] expands to show KPI breakdown
```

---

## SUCCESS CRITERIA

✅ **Problem Clarity:** Business user understands container shortage/surplus problem within 10 seconds
✅ **One-Click Optimization:** Single "Trigger" button initiates agent execution
✅ **Real-Time Visibility:** Map shows network imbalance + vessels + optimized routing
✅ **Narrative Flow:** Red alert → Auto-navigate → Agent execution → Results comparison → Performance gain
✅ **Business Metrics:** Every decision shows ROI (cost saved, SLA improved, CO₂ reduced, time saved)
✅ **Expandable Depth:** What-If and Performance available without page jumps
✅ **Data Persistence:** Planned routes → Optimized routes visible in same table
✅ **Page Consolidation:** 5 pages → 3 pages (Home, Container SC with tabs, separate Performance tab)

---

## IMPLEMENTATION PRIORITY

**Phase 1 (Critical):**

1. Move Fleet Map to Overview (inline)
2. Add Demand Alert system with banners
3. Modify console flow with "Run Agent" button
4. Add before/after route comparison in table

**Phase 2 (High):** 5. Add What-If expandable section in console 6. Add Performance expandable section in console 7. Refine narrative cards for business clarity

**Phase 3 (Nice-to-Have):** 8. Enhanced visualizations (custom charts for ROI) 9. Multi-scenario support 10. Export/reporting functionality
