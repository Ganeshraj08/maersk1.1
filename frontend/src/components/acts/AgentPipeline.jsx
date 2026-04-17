import React, { useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FLOW_STAGES } from '../../hooks/useAtlasFlow'

const AGENTS = [
  { key:'demand',       label:'Demand Sensing',  icon:'📡', color:'#00B4D8', desc:'Cross-referencing market signals, SAP orders & AIS data' },
  { key:'supply',       label:'Supply Finder',   icon:'🔍', color:'#8B5CF6', desc:'Scanning 60+ global depots against vessel schedules' },
  { key:'optimization', label:'Optimization',    icon:'⚡', color:'#F97316', desc:'XGBoost multi-objective cost/SLA/carbon ranking' },
]

const LOG_COLORS = {
  demand:       '#00B4D8',
  supply:       '#8B5CF6',
  optimization: '#F97316',
}

// Stages where agent pipeline should remain visible (complete state)
const COMPLETE_STAGES = new Set([
  FLOW_STAGES.ACT2A_STREET_TURN,
  FLOW_STAGES.ACT2C_COLOAD,
  FLOW_STAGES.REPOSITIONING_APPROVED,
  FLOW_STAGES.ACT3_BOOKING,
  FLOW_STAGES.ACT4A_RECOMMEND,
  FLOW_STAGES.ACT4B_EXECUTE,
  FLOW_STAGES.ACT5_CLOSING,
  FLOW_STAGES.COMPLETE,
])

export default function AgentPipeline({ flow }) {
  const { stage, agentLogs, activeAgent, agentProgress } = flow
  const logRef = useRef(null)

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight
    }
  }, [agentLogs])

  const isRunning  = stage === FLOW_STAGES.AGENTS_RUNNING
  const isComplete = COMPLETE_STAGES.has(stage)

  if (!isRunning && !isComplete) return null

  return (
    <motion.div
      initial={{ opacity:0, y:20 }}
      animate={{ opacity:1, y:0 }}
      className="space-y-4"
    >
      {/* Agent steps */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {AGENTS.map((ag) => {
          const isDone    = isComplete || (isRunning && agentLogs.some(l => l.agent === ag.key && l.prefix === '[RESULT]'))
          const isActive  = activeAgent === ag.key
          const isPending = !isDone && !isActive

          return (
            <div
              key={ag.key}
              className={`agent-step ${isPending ? 'pending' : isActive ? 'running' : 'complete'}`}
            >
              <div
                className="w-9 h-9 rounded-xl flex items-center justify-center text-lg shrink-0"
                style={{ background:`${ag.color}20`, border:`1px solid ${ag.color}40` }}
              >
                {isDone ? '✅' : isActive ? (
                  <motion.span animate={{ rotate:[0,360] }} transition={{ duration:2, repeat:Infinity, ease:'linear' }}>⚙️</motion.span>
                ) : ag.icon}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <p className="text-sm font-semibold text-white">{ag.label} Agent</p>
                  {isActive && <span className="badge-blue text-[9px]">Running</span>}
                  {isDone   && <span className="badge-green text-[9px]">Done</span>}
                </div>
                <p className="text-[11px] text-gray-500 mt-0.5">{ag.desc}</p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Progress bar */}
      {isRunning && (
        <div>
          <div className="flex justify-between text-[10px] text-gray-500 mb-1">
            <span>Agent Pipeline Progress</span>
            <span>{Math.round(agentProgress)}%</span>
          </div>
          <div className="h-1.5 bg-maersk-dark rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-maersk-blue to-maersk-teal rounded-full"
              style={{ width:`${agentProgress}%` }}
              transition={{ duration:0.3 }}
            />
          </div>
        </div>
      )}

      {/* Terminal output */}
      <div ref={logRef} className="terminal h-56 space-y-0.5">
        <div className="terminal-line">
          <span className="terminal-time">00:00:00</span>
          <span className="terminal-agent" style={{ color:'#00B4D8' }}>[ATLAS]</span>
          <span className="text-gray-300">Initialising multi-agent repositioning pipeline...</span>
        </div>
        {agentLogs.map((log, i) => (
          <motion.div
            key={i}
            initial={{ opacity:0 }}
            animate={{ opacity:1 }}
            className="terminal-line"
          >
            <span className="terminal-time">{log.time}</span>
            <span className="terminal-agent" style={{ color: log.color || LOG_COLORS[log.agent] || '#42B4E6' }}>
              {log.prefix}
            </span>
            <span className="text-gray-300">{log.text}</span>
          </motion.div>
        ))}
        {isRunning && (
          <div className="terminal-line">
            <span className="terminal-time">--:--:--</span>
            <motion.span
              animate={{ opacity:[1,0,1] }}
              transition={{ duration:1, repeat:Infinity }}
              className="text-maersk-teal"
            >▋</motion.span>
          </div>
        )}
        {isComplete && (
          <div className="terminal-line">
            <span className="terminal-time">--:--:--</span>
            <span className="terminal-agent" style={{ color:'#10B981' }}>[ATLAS]</span>
            <span className="text-atlas-green">Pipeline complete — recommendation ready</span>
          </div>
        )}
      </div>
    </motion.div>
  )
}
