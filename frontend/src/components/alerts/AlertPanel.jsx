import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FLOW_STAGES } from '../../hooks/useAtlasFlow'

export default function AlertPanel({ flow }) {
  const { stage, scenario, runAgents } = flow
  const [demandOpen, setDemandOpen] = useState(false)

  // Don't render in pipeline tab once agents have started running
  if (
    stage === FLOW_STAGES.IDLE ||
    stage === FLOW_STAGES.AGENTS_RUNNING ||
    stagePassedAgents(stage)
  ) return null

  function stagePassedAgents(s) {
    return [
      FLOW_STAGES.ACT2A_STREET_TURN,
      FLOW_STAGES.ACT2C_COLOAD,
      FLOW_STAGES.REPOSITIONING_APPROVED,
      FLOW_STAGES.ACT3_BOOKING,
      FLOW_STAGES.ACT4A_RECOMMEND,
      FLOW_STAGES.ACT4B_EXECUTE,
      FLOW_STAGES.ACT5_CLOSING,
      FLOW_STAGES.COMPLETE,
    ].includes(s)
  }

  return (
    <motion.div
      initial={{ opacity:0, y:-10 }}
      animate={{ opacity:1, y:0 }}
      className="space-y-3"
    >
      {/* Alert header — click to expand signal detection */}
      <div
        className="card p-4 border-atlas-amber/50 bg-atlas-amber/5 flex items-center justify-between cursor-pointer"
        onClick={() => setDemandOpen(o => !o)}
      >
        <div className="flex items-center gap-3">
          <motion.div
            animate={{ scale:[1,1.1,1] }}
            transition={{ duration:1.5, repeat:Infinity }}
            className="w-8 h-8 rounded-lg bg-atlas-amber/20 border border-atlas-amber/40 flex items-center justify-center"
          >
            <span className="text-lg">⚠️</span>
          </motion.div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <p className="text-sm font-bold text-atlas-amber">1 Proactive Alert</p>
              <span className="badge-green">
                <span className="w-1.5 h-1.5 rounded-full bg-atlas-green animate-pulse-slow" />
                Autonomous Demand Detected
              </span>
            </div>
            <p className="text-xs text-gray-400 mt-0.5 max-w-xl">{scenario.description}</p>
          </div>
        </div>
        <span className="text-xs text-gray-500 shrink-0 ml-2">{demandOpen ? '▲' : '▼'}</span>
      </div>

      {/* Signal detection — hidden until header clicked */}
      <AnimatePresence>
        {demandOpen && (
          <motion.div
            initial={{ height:0, opacity:0 }}
            animate={{ height:'auto', opacity:1 }}
            exit={{ height:0, opacity:0 }}
            className="overflow-hidden"
          >
            <div className="card p-5 border-maersk-teal/30 bg-maersk-dark/80">
              {/* Title */}
              <div className="flex items-center gap-3 mb-4">
                <div className="w-2 h-2 rounded-full bg-atlas-green animate-pulse-slow" />
                <h3 className="font-bold text-white">ATLAS Autonomous Signal Detection</h3>
                <span className="badge-green ml-auto">Active</span>
              </div>

              {/* Signal rows */}
              <div className="space-y-2 mb-4">
                {(scenario.signals || []).map((sig, i) => (
                  <motion.div
                    key={sig.source}
                    initial={{ opacity:0, x:-10 }}
                    animate={{ opacity:1, x:0 }}
                    transition={{ delay: i * 0.08 }}
                    className="flex items-start gap-3 p-2.5 rounded-lg bg-maersk-dark/60 border border-maersk-blue/10"
                  >
                    <span className="text-base shrink-0">{sig.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-xs font-semibold text-maersk-teal">{sig.source}</span>
                        <span className="text-[10px] text-gray-500">weight: {(sig.weight * 100).toFixed(0)}%</span>
                      </div>
                      <p className="text-xs text-gray-300 mt-0.5">{sig.signal}</p>
                    </div>
                    <div className="shrink-0 w-16">
                      <div className="h-1 bg-maersk-dark rounded-full overflow-hidden">
                        <div
                          className="h-full bg-maersk-teal rounded-full"
                          style={{ width:`${Math.min(sig.weight * 100 * 3, 100)}%` }}
                        />
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* ATLAS conclusion */}
              <div className="bg-atlas-green/10 border border-atlas-green/30 rounded-xl p-4 mb-4">
                <p className="text-xs font-bold text-atlas-green uppercase tracking-wider mb-2">📊 ATLAS Conclusion</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {[
                    { label:'Demand',     value: scenario.prediction?.demand },
                    { label:'Region',     value: scenario.prediction?.region },
                    { label:'Window',     value: scenario.prediction?.window },
                    { label:'Confidence', value: `${scenario.prediction?.confidence}%` },
                  ].map(item => (
                    <div key={item.label}>
                      <p className="text-[10px] text-gray-500 uppercase tracking-wider">{item.label}</p>
                      <p className="text-sm font-bold text-white">{item.value}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Run agents CTA */}
              <button onClick={runAgents} className="btn-primary w-full">
                ▶ Run ATLAS Agents
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
