import React from 'react'
import { motion } from 'framer-motion'
import { FLOW_STAGES, stageAtLeast } from '../../hooks/useAtlasFlow'
import { FLEET_VESSELS } from '../../data/maritimeData'

export default function Act4BScreen({ flow }) {
  const { stage, sapStepsDone, executeApprove, goToAct5, scenario } = flow
  if (!stageAtLeast(stage, FLOW_STAGES.ACT4B_EXECUTE)) return null

  // Use scenario-specific SAP steps (each scenario has its own sapSteps)
  const sapSteps = scenario?.sapSteps || []

  // Winning depot vessel from this scenario's recommendation
  const winningOption = scenario?.repositionOptions?.find(o => o.highlight)
  const vesselId      = winningOption?.vessel
  const vessel        = FLEET_VESSELS.find(v => v.id === vesselId) || FLEET_VESSELS[1]

  const isExecuting = sapStepsDone.length > 0 && sapStepsDone.length < sapSteps.length
  const isDone      = sapSteps.length > 0 && sapStepsDone.length === sapSteps.length

  // Scenario-specific autonomous co-load upsell
  const coloadOpp = {
    vietnam_surge:     { company:'PT Sinarmas Agro',   route:`HCMC → Jakarta`,          teu:280, rev:68_400  },
    philippines:       { company:'Ayala Fashion Group', route:'Manila → Singapore',       teu:210, rev:51_450  },
    bangladesh_crisis: { company:'H&M Bangladesh',      route:'Chittagong → Rotterdam',   teu:185, rev:52_725  },
    india_automotive:  { company:'Tata Steel Export',   route:'JNPT → Rotterdam',         teu:240, rev:70_800  },
    korea_electronics: { company:'LG Display Corp.',    route:'Busan → LA/LB',            teu:280, rev:161_000 },
  }[scenario?.id] || { company:'Local Cargo Partner', route:`${scenario?.destination} → hub`, teu:200, rev:50_000 }

  return (
    <motion.div
      initial={{ opacity:0, y:20 }}
      animate={{ opacity:1, y:0 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center gap-3 pb-3 border-b border-maersk-blue/20">
        <div>
          <h3 className="font-bold text-white">One-click approval. SAP execution.</h3>
          <p className="text-xs text-gray-500">Full automation from decision to vessel slot confirmation</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* SAP execution steps */}
        <div className="card p-4">
          <p className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">SAP Execution — One Click</p>
          <div className="space-y-2">
            {sapSteps.map((step) => {
              const done   = sapStepsDone.includes(step.id)
              const active = !done && sapStepsDone.length === step.id - 1
              return (
                <motion.div
                  key={step.id}
                  className={`flex items-start gap-3 p-2.5 rounded-lg border transition-all duration-500 ${
                    done   ? 'border-atlas-green/30 bg-atlas-green/5' :
                    active ? 'border-maersk-teal/40 bg-maersk-teal/5 animate-pulse-slow' :
                             'border-maersk-blue/10 bg-transparent opacity-40'
                  }`}
                >
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs shrink-0 mt-0.5 ${
                    done ? 'bg-atlas-green text-maersk-dark' : 'bg-maersk-blue/20 text-gray-500'
                  }`}>
                    {done ? '✓' : step.id}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-white">{step.text}</p>
                    <p className="text-[10px] text-gray-500 mt-0.5">{step.sub}</p>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>

        {/* Vessel capacity panel */}
        <div className="card p-4">
          <p className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
            {vessel?.name} — Remaining Capacity
          </p>
          {vessel && (
            <div className="space-y-3">
              {/* Capacity bar */}
              <div className="relative">
                <div className="h-20 bg-maersk-dark/60 border border-maersk-blue/20 rounded-xl overflow-hidden flex">
                  <motion.div
                    initial={{ width:0 }}
                    animate={{ width:`${(scenario.teuRequired / vessel.capacityTEU) * 100}%` }}
                    transition={{ duration:1, ease:'easeOut' }}
                    className="h-full bg-gradient-to-r from-maersk-blue to-maersk-teal"
                  />
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-lg font-black text-white">{scenario.teuRequired} TEU</p>
                    <p className="text-[10px] text-gray-400">of {vessel.capacityTEU.toLocaleString()} TEU capacity</p>
                  </div>
                </div>
              </div>

              {/* Stats row */}
              <div className="grid grid-cols-3 gap-2">
                {[
                  { label:'Vessel Cap', value:`${(vessel.capacityTEU/1000).toFixed(0)}K` },
                  { label:'Allocated',  value:`${scenario.teuRequired}` },
                  { label:'Remaining',  value:`${(vessel.capacityTEU - scenario.teuRequired - Math.round(vessel.capacityTEU * vessel.cargoPct / 100)).toLocaleString()}` },
                ].map(s => (
                  <div key={s.label} className="text-center card p-2">
                    <p className="text-[10px] text-gray-500">{s.label}</p>
                    <p className="text-base font-bold text-maersk-teal">{s.value}</p>
                  </div>
                ))}
              </div>

              {/* Autonomous co-load upsell */}
              <div className="bg-atlas-amber/5 border border-atlas-amber/30 rounded-xl p-3">
                <p className="text-[10px] font-bold text-atlas-amber uppercase tracking-wider mb-1">
                  ⚡ ATLAS Autonomous Opportunity Detected
                </p>
                <p className="text-xs text-gray-300">
                  {coloadOpp.company} requires {coloadOpp.teu} TEUs · {coloadOpp.route} · same window.
                  Revenue: ${coloadOpp.rev.toLocaleString()}. Booking initiated autonomously.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* CTA states */}
      {!isDone && !isExecuting && (
        <motion.button
          whileHover={{ scale:1.02 }}
          whileTap={{ scale:0.98 }}
          onClick={executeApprove}
          className="w-full py-4 rounded-2xl font-bold text-lg text-maersk-dark transition-all"
          style={{ background:'linear-gradient(135deg, #00B4D8, #0077B6)', boxShadow:'0 4px 20px rgba(0,180,216,0.4)' }}
        >
          ✓ Approve and Execute
        </motion.button>
      )}

      {isExecuting && (
        <div className="w-full py-4 rounded-2xl bg-maersk-blue/20 border border-maersk-blue/40 text-center">
          <motion.p
            animate={{ opacity:[1,0.5,1] }}
            transition={{ duration:1, repeat:Infinity }}
            className="text-maersk-teal font-semibold"
          >
            Executing SAP orders…
          </motion.p>
        </div>
      )}

      {isDone && (
        <motion.div
          initial={{ opacity:0, scale:0.9 }}
          animate={{ opacity:1, scale:1 }}
          className="space-y-3"
        >
          <div className="bg-atlas-green/10 border border-atlas-green/30 rounded-2xl p-4 text-center">
            <div className="text-3xl mb-2">✅</div>
            <p className="text-atlas-green font-bold">All SAP orders executed successfully</p>
            <p className="text-xs text-gray-400 mt-1">
              {scenario.teuRequired} TEUs confirmed · {vessel?.name} slot locked · {scenario.customer} notified
            </p>
          </div>
          <button onClick={goToAct5} className="btn-primary w-full">
            View Performance →
          </button>
        </motion.div>
      )}
    </motion.div>
  )
}
