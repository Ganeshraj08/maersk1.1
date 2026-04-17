import { useState, useCallback, useRef } from 'react'
import { DEMAND_SCENARIOS, SAP_EXECUTION_STEPS } from '../data/maritimeData'

// Flow stages — order matters for UI progression
export const FLOW_STAGES = {
  IDLE:                   'IDLE',
  ALERT_ACTIVE:           'ALERT_ACTIVE',
  DEMAND_EXPANDED:        'DEMAND_EXPANDED',
  AGENTS_RUNNING:         'AGENTS_RUNNING',
  ACT2A_STREET_TURN:      'ACT2A_STREET_TURN',   // repositioning recommendation
  ACT2C_COLOAD:           'ACT2C_COLOAD',          // co-load optimization
  REPOSITIONING_APPROVED: 'REPOSITIONING_APPROVED', // dashboard updates, booking fires
  ACT3_BOOKING:           'ACT3_BOOKING',           // booking request arrives
  ACT4A_RECOMMEND:        'ACT4A_RECOMMEND',        // view detailed recommendation
  ACT4B_EXECUTE:          'ACT4B_EXECUTE',          // SAP execution
  ACT5_CLOSING:           'ACT5_CLOSING',           // performance reveal
  COMPLETE:               'COMPLETE',               // all done, KPIs updated
}

// Ordered array for stage comparison
const STAGE_ORDER = [
  FLOW_STAGES.IDLE,
  FLOW_STAGES.ALERT_ACTIVE,
  FLOW_STAGES.DEMAND_EXPANDED,
  FLOW_STAGES.AGENTS_RUNNING,
  FLOW_STAGES.ACT2A_STREET_TURN,
  FLOW_STAGES.ACT2C_COLOAD,
  FLOW_STAGES.REPOSITIONING_APPROVED,
  FLOW_STAGES.ACT3_BOOKING,
  FLOW_STAGES.ACT4A_RECOMMEND,
  FLOW_STAGES.ACT4B_EXECUTE,
  FLOW_STAGES.ACT5_CLOSING,
  FLOW_STAGES.COMPLETE,
]

export function stageIndex(stage) {
  return STAGE_ORDER.indexOf(stage)
}

export function stageAtLeast(current, target) {
  return stageIndex(current) >= stageIndex(target)
}

// ── Generate scenario-driven agent logs ──────────────────────────────────────
function generateAgentLogs(scenario) {
  const opts = scenario.repositionOptions || []
  const rejected = opts.find(o => o.rejected)
  const winner   = opts.find(o => o.highlight)
  const backup   = opts.find(o => !o.rejected && !o.highlight)

  const demandLogs = [
    { ms:200,  color:'#00B4D8', prefix:'[DEMAND]',  text:`Initialising Demand Sensing Agent v2.4 — scenario: ${scenario.name}` },
    { ms:600,  color:'#00B4D8', prefix:'[DEMAND]',  text:`Connecting to PortSight™ Live feed for ${scenario.region}...` },
    ...(scenario.signals || []).slice(0, 3).map((sig, i) => ({
      ms: 1000 + i * 400,
      color:'#42B4E6', prefix:'[DATA]',
      text: `${sig.source}: ${sig.signal.substring(0, 80)}`,
    })),
    { ms:2200, color:'#10B981', prefix:'[RESULT]',  text:`DEMAND CONFIRMED: ${scenario.prediction.demand}, ${scenario.prediction.region}, ${scenario.prediction.window}, confidence ${scenario.prediction.confidence}%` },
  ]

  const supplyLogs = [
    { ms:200,  color:'#8B5CF6', prefix:'[SUPPLY]',  text:'Initialising Supply Finder Agent v1.9...' },
    { ms:500,  color:'#8B5CF6', prefix:'[SUPPLY]',  text:`Scanning ${Object.keys(DEMAND_SCENARIOS).length * 12}+ depot locations...` },
    ...(rejected ? [
      { ms:900,  color:'#42B4E6', prefix:'[SCAN]',    text:`${rejected.depot}: ${rejected.available.toLocaleString()} TEU listed — cross-checking AIS...` },
      { ms:1300, color:'#EF4444', prefix:'[CONFLICT]',text:`${rejected.depot} REJECTED: AIS conflict — real SLA ${rejected.realSLA} vs listed ${rejected.listedSLA}` },
    ] : []),
    ...(winner ? [
      { ms:1700, color:'#42B4E6', prefix:'[SCAN]',    text:`${winner.depot}: ${winner.available.toLocaleString()} TEU confirmed — no conflicts in window` },
      { ms:2100, color:'#10B981', prefix:'[MATCH]',   text:`${winner.depot} SELECTED: ${winner.method} — SLA ${winner.realSLA} — $${winner.costTEU}/TEU` },
    ] : []),
    { ms:2500, color:'#10B981', prefix:'[RESULT]',  text:`${opts.length} supply options ranked: ${opts.map(o => `${o.depot}(${o.realSLA})`).join(' > ')}` },
  ]

  const st = scenario.streetTurn
  const saving = st?.atlasWay?.netSaving
  const optLine = winner ? `${winner.depot} route: cost $${winner.costTEU}/TEU, ${winner.transitDays} days, CO₂ ${winner.co2Saving}, SLA ${winner.realSLA}` : 'Optimization complete'
  const coloadLine = st ? `Co-load opportunity: ${st.atlasWay.shipment} detected` : 'Co-load opportunities analysed'
  const savingLine = saving ? `Co-load net saving: $${saving.toLocaleString()} vs empty repositioning` : 'Savings calculated'

  const optimizationLogs = [
    { ms:200,  color:'#F97316', prefix:'[OPTIM]',   text:'Initialising Optimization Agent v3.1 (XGBoost ensemble)...' },
    { ms:600,  color:'#F97316', prefix:'[OPTIM]',   text:'Running cost/SLA/carbon multi-objective optimisation...' },
    { ms:1000, color:'#42B4E6', prefix:'[CALC]',    text:optLine },
    { ms:1400, color:'#42B4E6', prefix:'[CALC]',    text:coloadLine },
    { ms:1800, color:'#10B981', prefix:'[COLOAD]',  text:savingLine },
    { ms:2200, color:'#10B981', prefix:'[RESULT]',  text:`RECOMMENDATION: ${winner ? winner.depot : 'optimal depot'} via ${winner?.vessel || 'best vessel'} + co-load match` },
  ]

  return { demand: demandLogs, supply: supplyLogs, optimization: optimizationLogs }
}

export function useAtlasFlow() {
  const [stage, setStage]               = useState(FLOW_STAGES.IDLE)
  const [activeScenario, setScenario]   = useState('vietnam_surge')
  const [agentLogs, setAgentLogs]       = useState([])
  const [activeAgent, setActiveAgent]   = useState(null)
  const [agentProgress, setAgentProgress] = useState(0)
  const [approvedRouteIdx, setApprovedRouteIdx] = useState(0)
  const [sapStepsDone, setSapStepsDone] = useState([])
  const [dashboardUpdated, setDashboardUpdated]         = useState(false)
  const [repositioningApproved, setRepositioningApproved] = useState(false)
  const timerRefs = useRef([])

  const scenario = DEMAND_SCENARIOS[activeScenario] || DEMAND_SCENARIOS.vietnam_surge

  const clearTimers = () => {
    timerRefs.current.forEach(t => clearTimeout(t))
    timerRefs.current = []
  }

  const schedule = (fn, ms) => {
    const t = setTimeout(fn, ms)
    timerRefs.current.push(t)
    return t
  }

  // ── Step 1: Show alert ──────────────────────────────────────────────────────
  const triggerAlert = useCallback(() => {
    setStage(FLOW_STAGES.ALERT_ACTIVE)
  }, [])

  // ── Step 2: Expand demand details (click on alert header) ──────────────────
  const expandDemand = useCallback(() => {
    setStage(FLOW_STAGES.DEMAND_EXPANDED)
  }, [])

  // ── Step 3: Run agents ──────────────────────────────────────────────────────
  const runAgents = useCallback(() => {
    clearTimers()
    setStage(FLOW_STAGES.AGENTS_RUNNING)
    setAgentLogs([])
    setAgentProgress(0)

    const currentScenario = DEMAND_SCENARIOS[activeScenario] || DEMAND_SCENARIOS.vietnam_surge
    const AGENT_LOGS = generateAgentLogs(currentScenario)
    const agentKeys = ['demand', 'supply', 'optimization']
    let globalOffset = 0

    agentKeys.forEach((agentKey, agentIdx) => {
      const logs = AGENT_LOGS[agentKey]
      const agentStart = globalOffset

      schedule(() => setActiveAgent(agentKey), agentStart)

      logs.forEach(({ ms, ...log }) => {
        schedule(() => {
          setAgentLogs(prev => [...prev, {
            ...log,
            agent: agentKey,
            time: new Date().toLocaleTimeString('en-US', { hour12:false }),
          }])
          const totalLogs = agentKeys.reduce((sum, k) => sum + AGENT_LOGS[k].length, 0)
          const doneCount = agentKeys.slice(0, agentIdx).reduce((sum, k) => sum + AGENT_LOGS[k].length, 0) + logs.indexOf({ ms, ...log }) + 1
          setAgentProgress(Math.round((doneCount / totalLogs) * 100))
        }, agentStart + ms)
      })

      globalOffset += 3200

      if (agentIdx === agentKeys.length - 1) {
        // After all agents complete → go directly to Act 2A (Street-Turn)
        schedule(() => {
          setActiveAgent(null)
          setAgentProgress(100)
          setStage(FLOW_STAGES.ACT2A_STREET_TURN)
        }, globalOffset + 400)
      }
    })
  }, [activeScenario])

  // ── Navigation actions ──────────────────────────────────────────────────────
  const goToAct2A = useCallback(() => setStage(FLOW_STAGES.ACT2A_STREET_TURN), [])
  const goToAct2C = useCallback(() => setStage(FLOW_STAGES.ACT2C_COLOAD),      [])
  const goToAct3  = useCallback(() => setStage(FLOW_STAGES.ACT3_BOOKING),      [])
  const goToAct4A = useCallback(() => setStage(FLOW_STAGES.ACT4A_RECOMMEND),   [])
  const goToAct4B = useCallback(() => setStage(FLOW_STAGES.ACT4B_EXECUTE),     [])
  const goToAct5  = useCallback(() => setStage(FLOW_STAGES.ACT5_CLOSING),      [])

  // ── Kept for backward compat ────────────────────────────────────────────────
  const viewReasoning = useCallback(() => setStage(FLOW_STAGES.ACT2A_STREET_TURN), [])

  // ── Approve Repositioning — returns to dashboard, updates ports ─────────────
  const approveRepositioning = useCallback(() => {
    setStage(FLOW_STAGES.REPOSITIONING_APPROVED)
    setRepositioningApproved(true)
  }, [])

  // ── Receive Booking — triggers Act 3 ───────────────────────────────────────
  const receiveBooking = useCallback(() => {
    setStage(FLOW_STAGES.ACT3_BOOKING)
  }, [])

  // ── Execute SAP (from Act 4B) — uses scenario-specific sapSteps ────────────
  const executeApprove = useCallback(() => {
    setStage(FLOW_STAGES.ACT4B_EXECUTE)
    setSapStepsDone([])

    const currentScenario = DEMAND_SCENARIOS[activeScenario] || DEMAND_SCENARIOS.vietnam_surge
    const steps = currentScenario.sapSteps || SAP_EXECUTION_STEPS

    steps.forEach(({ id, delay }) => {
      schedule(() => {
        setSapStepsDone(prev => [...prev, id])
        if (id === steps.length) {
          schedule(() => setStage(FLOW_STAGES.ACT5_CLOSING), 800)
        }
      }, delay)
    })
  }, [activeScenario])

  // ── Complete → navigate to dashboard ───────────────────────────────────────
  const complete = useCallback(() => {
    setStage(FLOW_STAGES.COMPLETE)
    setDashboardUpdated(true)
  }, [])

  // ── Reset flow ──────────────────────────────────────────────────────────────
  const reset = useCallback(() => {
    clearTimers()
    setStage(FLOW_STAGES.IDLE)
    setAgentLogs([])
    setActiveAgent(null)
    setAgentProgress(0)
    setSapStepsDone([])
    setDashboardUpdated(false)
    setRepositioningApproved(false)
  }, [])

  return {
    stage, scenario, agentLogs, activeAgent, agentProgress,
    approvedRouteIdx, setApprovedRouteIdx,
    sapStepsDone, dashboardUpdated, repositioningApproved,
    // Actions
    triggerAlert, expandDemand, runAgents, viewReasoning,
    goToAct2A, goToAct2C, goToAct3, goToAct4A, goToAct4B, goToAct5,
    approveRepositioning, receiveBooking,
    executeApprove, complete, reset,
    setScenario,
  }
}
