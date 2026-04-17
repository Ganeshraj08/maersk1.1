# ATLAS Maritime Intelligence — Quick Start

## Frontend (React + Vite + Tailwind)
```bash
cd frontend
npm install          # first time only
npm run dev          # starts on http://localhost:3000
```

## Backend (FastAPI — optional, frontend runs standalone)
```bash
cd backend
pip install -r requirements.txt
python main.py       # starts on http://localhost:8000
```

## Full Demo Flow
1. Open http://localhost:3000
2. Click **"Launch Container SC →"** on the Container Supply Chain card
3. **Global Monitor tab** → Click **"Simulate Alert"**
4. **Agent Pipeline tab** → Expand the alert → Click **"▶ Run ATLAS Agents"**
5. Watch 3 agents run in the terminal (Demand → Supply → Optimization)
6. Click **"Proceed to Approval →"** to see the SAP execution screen
7. Click **"✓ Approve and Execute"** → SAP steps animate
8. Act 5 Closing Screen: ATLAS prediction vs actual booking comparison
9. Click **"✓ Complete — Update Dashboard"** → KPIs update dynamically

## File Structure
```
frontend/
  src/
    data/maritimeData.js      ← All ports, vessels, scenarios, KPIs
    hooks/useAtlasFlow.js     ← State machine for the full demo flow
    pages/
      Home.jsx                ← Landing page with 5 use case cards
      ContainerSC.jsx         ← Main dashboard (4 tabs)
    components/
      dashboard/              ← MetricCard, PortCard, Charts, DataSources
      alerts/AlertPanel.jsx   ← Alert notification + signal detection
      acts/
        AgentPipeline.jsx     ← 3-agent terminal execution
        Act2AScreen.jsx       ← Repositioning recommendation table
        Act2CScreen.jsx       ← Philips co-load opportunity
        Act3Screen.jsx        ← Vinamilk booking request
        Act4BScreen.jsx       ← SAP execution + Approve button
        Act5Screen.jsx        ← Prediction vs Actual + Forecast chart

backend/
  main.py                     ← FastAPI with SSE agent streaming
  requirements.txt
```
