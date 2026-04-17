import React from 'react'
import { motion } from 'framer-motion'
import { FLOW_STAGES } from '../../hooks/useAtlasFlow'

export default function Act2AScreen({ flow }) {
  const { stage, scenario, goToAct2C, goToAct4B } = flow

  const isStreetTurn = stage === FLOW_STAGES.ACT2A_STREET_TURN
  const isRecommend  = stage === FLOW_STAGES.ACT4A_RECOMMEND

  if (!isStreetTurn && !isRecommend) return null

  // ── Street-Turn view (Act 2A) ──────────────────────────────────────────────
  if (isStreetTurn) {
    const matches   = scenario?.streetTurnMatches || []
    const totalTeus = scenario?.streetTurnTotalTeus || 0
    const remaining = scenario?.remainingTeus || 0
    const own       = scenario?.ownFleet || {}
    const lease     = scenario?.emergencyLease || {}
    const saving    = scenario?.fleetSavingPerBooking || 0

    return (
      <motion.div
        initial={{ opacity:0, y:20 }}
        animate={{ opacity:1, y:0 }}
        className="space-y-5"
      >
        {/* ── STEP 1: Street-Turn Matches ── */}
        <div className="card overflow-hidden">
          <div className="p-4 border-b border-maersk-blue/20">
            <p className="text-[10px] font-bold text-maersk-teal uppercase tracking-widest mb-0.5">
              Step 1 — Street-Turn Matches Found First (Zero Repositioning Cost)
            </p>
            <p className="text-xs text-gray-500">Containers reloaded direct — never travel empty</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-maersk-blue/15 bg-maersk-dark/40">
                  <th className="text-left px-4 py-2.5 text-[10px] font-bold text-gray-500 uppercase tracking-wider">Unload Point</th>
                  <th className="px-3 py-2.5 text-[10px] font-bold text-gray-500 uppercase tracking-wider text-center">→</th>
                  <th className="text-left px-4 py-2.5 text-[10px] font-bold text-gray-500 uppercase tracking-wider">Direct Reload</th>
                  <th className="text-right px-4 py-2.5 text-[10px] font-bold text-gray-500 uppercase tracking-wider">TEUs</th>
                  <th className="text-right px-4 py-2.5 text-[10px] font-bold text-gray-500 uppercase tracking-wider">Cost</th>
                </tr>
              </thead>
              <tbody>
                {matches.map((m, i) => (
                  <motion.tr
                    key={i}
                    initial={{ opacity:0, x:-15 }}
                    animate={{ opacity:1, x:0 }}
                    transition={{ delay: i * 0.1 }}
                    className="border-b border-maersk-blue/10 hover:bg-maersk-blue/5 transition-colors"
                  >
                    <td className="px-4 py-3 text-gray-300 text-sm">{m.from}</td>
                    <td className="px-3 py-3 text-center">
                      <span className="text-maersk-teal font-bold">→</span>
                    </td>
                    <td className="px-4 py-3 text-white font-medium text-sm">{m.to}</td>
                    <td className="px-4 py-3 text-right font-mono font-bold text-maersk-teal">
                      {m.teus} TEUs
                    </td>
                    <td className="px-4 py-3 text-right font-mono font-black text-atlas-green">
                      ${m.cost}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="bg-atlas-green/5 border-t border-atlas-green/20">
                  <td colSpan={3} className="px-4 py-3 text-sm font-bold text-white">
                    Street-turn total — containers never travel empty
                  </td>
                  <td className="px-4 py-3 text-right font-mono font-black text-atlas-green">
                    {totalTeus} TEUs
                  </td>
                  <td className="px-4 py-3 text-right font-mono font-black text-atlas-green">
                    $0 cost
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>

        {/* ── STEP 2: Own Fleet vs Emergency Lease ── */}
        <div className="card p-4">
          <p className="text-[10px] font-bold text-maersk-teal uppercase tracking-widest mb-3">
            Step 2 — Remaining {remaining} TEUs: Own Fleet vs Emergency Lease
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            {/* Own Fleet — SELECTED */}
            <motion.div
              initial={{ opacity:0, y:10 }}
              animate={{ opacity:1, y:0 }}
              transition={{ delay:0.3 }}
              className="border-2 border-atlas-green/50 bg-atlas-green/5 rounded-xl p-4"
            >
              <div className="flex items-center gap-2 mb-3">
                <div className="w-2 h-2 rounded-full bg-atlas-green" />
                <p className="text-xs font-black text-atlas-green uppercase tracking-wider">Own Fleet — Selected</p>
              </div>
              <p className="text-3xl font-black text-white mb-2">${own.costPerTEU}<span className="text-base font-normal text-gray-400">/TEU</span></p>
              <p className="text-sm text-gray-300 mb-1">{own.depot}</p>
              <p className="text-xs text-gray-500">{own.schedule}</p>
            </motion.div>

            {/* Emergency Lease — REJECTED */}
            <motion.div
              initial={{ opacity:0, y:10 }}
              animate={{ opacity:1, y:0 }}
              transition={{ delay:0.4 }}
              className="border border-atlas-red/30 bg-atlas-red/5 rounded-xl p-4 opacity-75"
            >
              <div className="flex items-center gap-2 mb-3">
                <div className="w-2 h-2 rounded-full bg-atlas-red" />
                <p className="text-xs font-black text-atlas-red uppercase tracking-wider">Emergency Lease — Rejected</p>
              </div>
              <p className="text-3xl font-black text-gray-400 mb-2 line-through">${lease.costPerTEU}<span className="text-base font-normal">/TEU</span></p>
              <p className="text-sm text-gray-500 mb-1">{lease.source}</p>
              <p className="text-xs text-gray-600">{lease.note}</p>
            </motion.div>
          </div>

          {/* Savings footer */}
          <motion.div
            initial={{ opacity:0, scale:0.97 }}
            animate={{ opacity:1, scale:1 }}
            transition={{ delay:0.5 }}
            className="bg-atlas-green/10 border border-atlas-green/30 rounded-xl p-3.5 flex items-center justify-between"
          >
            <span className="text-sm text-gray-300 font-medium">Own fleet selected — saving per booking</span>
            <span className="text-xl font-black text-atlas-green">
              ${saving.toLocaleString()} saved
            </span>
          </motion.div>
        </div>

        {/* Action */}
        <button onClick={goToAct2C} className="btn-primary w-full">
          View Co-load Optimisation →
        </button>
      </motion.div>
    )
  }

  // ── Recommendation view (Act 4A) ───────────────────────────────────────────
  const repositionOptions = scenario?.repositionOptions || []

  return (
    <motion.div
      initial={{ opacity:0, y:20 }}
      animate={{ opacity:1, y:0 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center gap-3 pb-3 border-b border-maersk-blue/20">
        <div>
          <h3 className="font-bold text-white">Repositioning Recommendation</h3>
          <p className="text-xs text-gray-500">Best depot confirmed — proceed to execute</p>
        </div>
        <span className="badge-green ml-auto">Ready</span>
      </div>

      {/* Options table */}
      <div className="overflow-x-auto">
        <table className="data-table w-full">
          <thead>
            <tr>
              <th>Depot</th>
              <th>Distance</th>
              <th>Cost/TEU</th>
              <th>Listed SLA</th>
              <th>Real SLA</th>
              <th>Available</th>
              <th>Decision</th>
            </tr>
          </thead>
          <tbody>
            {repositionOptions.map((opt, i) => (
              <motion.tr
                key={opt.depot}
                initial={{ opacity:0, x:-20 }}
                animate={{ opacity:1, x:0 }}
                transition={{ delay: i * 0.12 }}
                className={opt.highlight ? 'bg-atlas-green/5' : opt.rejected ? 'bg-atlas-red/5' : ''}
              >
                <td>
                  <div className="font-semibold text-white">{opt.depot}</div>
                  <div className="text-[10px] text-gray-500">{opt.depotId}</div>
                </td>
                <td className="text-gray-300">{opt.distance}</td>
                <td className="font-mono font-semibold" style={{ color: opt.highlight ? '#10B981' : '#9CA3AF' }}>
                  {opt.costTEU === 0 ? 'Pre-staged' : `$${opt.costTEU}`}
                </td>
                <td className="text-gray-400">{opt.listedSLA}</td>
                <td>
                  <span className={`font-bold ${parseInt(opt.realSLA) >= 80 ? 'text-atlas-green' : parseInt(opt.realSLA) >= 50 ? 'text-atlas-amber' : 'text-atlas-red'}`}>
                    {opt.realSLA}
                  </span>
                </td>
                <td className="font-mono text-gray-300">{opt.available.toLocaleString()}</td>
                <td>
                  <span className={`px-2.5 py-1 rounded-lg text-xs font-bold ${
                    opt.decision === 'Pre-positioned' ? 'bg-atlas-green/20 text-atlas-green border border-atlas-green/40' :
                    opt.decision === 'All conflict'   ? 'bg-atlas-red/20 text-atlas-red border border-atlas-red/40' :
                    'bg-atlas-amber/20 text-atlas-amber border border-atlas-amber/40'
                  }`}>{opt.decision}</span>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Reasoning */}
      <div className="space-y-3">
        {repositionOptions.filter(o => o.rejected).map(opt => (
          <div key={opt.depot} className="bg-atlas-red/5 border border-atlas-red/20 rounded-xl p-4">
            <p className="text-xs font-bold text-atlas-red uppercase tracking-wider mb-2">❌ Why {opt.depot} Was Rejected — AIS Live Data</p>
            <p className="text-sm text-gray-300 leading-relaxed">{opt.reasoning}</p>
          </div>
        ))}
        {repositionOptions.filter(o => o.highlight).map(opt => (
          <div key={opt.depot} className="bg-atlas-green/5 border border-atlas-green/20 rounded-xl p-4">
            <p className="text-xs font-bold text-atlas-green uppercase tracking-wider mb-2">✅ Why {opt.depot} Wins</p>
            <p className="text-sm text-gray-300 leading-relaxed">{opt.reasoning}</p>
          </div>
        ))}
      </div>

      <button onClick={goToAct4B} className="btn-primary">
        Proceed to SAP Execution →
      </button>
    </motion.div>
  )
}
