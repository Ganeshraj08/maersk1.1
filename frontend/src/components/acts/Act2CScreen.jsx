import React from 'react'
import { motion } from 'framer-motion'
import { FLOW_STAGES } from '../../hooks/useAtlasFlow'

export default function Act2CScreen({ flow }) {
  const { stage, scenario, approveRepositioning } = flow
  if (stage !== FLOW_STAGES.ACT2C_COLOAD) return null

  const streetTurn = scenario?.streetTurn || {}
  const { oldWay = {}, atlasWay = {} } = streetTurn

  return (
    <motion.div
      initial={{ opacity:0, y:20 }}
      animate={{ opacity:1, y:0 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center gap-3 pb-3 border-b border-maersk-blue/20">
        <div>
          <h3 className="font-bold text-white">Moving with cargo, not empty.</h3>
          <p className="text-xs text-gray-500">ATLAS Cargo Match — containers travel full, not empty</p>
        </div>
      </div>

      {/* Route header */}
      <div className="card p-4 bg-maersk-dark/80">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <p className="text-[10px] text-gray-500 uppercase tracking-wider">Route</p>
            <p className="text-base font-bold text-white">{atlasWay.route || '—'}</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] text-gray-500 uppercase tracking-wider">Vessel · Duration</p>
            <p className="text-sm font-semibold text-maersk-teal">
              {atlasWay.vessel} · {atlasWay.duration} · Co-loaded
            </p>
          </div>
        </div>
        <div className="mt-3 flex items-center gap-2">
          <div className="flex-1 h-1.5 bg-maersk-dark rounded-full overflow-hidden">
            <motion.div
              initial={{ width:0 }}
              animate={{ width:'100%' }}
              transition={{ duration:1.5, ease:'easeOut' }}
              className="h-full bg-gradient-to-r from-maersk-blue to-maersk-teal rounded-full"
            />
          </div>
          <span className="badge-green">{atlasWay.shipment}</span>
        </div>
      </div>

      {/* Old way vs ATLAS side-by-side */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Old way */}
        <div className="card p-4 border-atlas-red/20 bg-atlas-red/5">
          <p className="text-xs font-bold text-atlas-red uppercase tracking-wider mb-3">❌ Old Way — Empty Repositioning</p>
          <table className="w-full text-sm">
            <tbody>
              {[
                ['Cost per TEU',      `$${oldWay.costPerTEU || 0}`],
                ['Containers',        `${oldWay.containers || 0} TEUs`],
                ['Total cost',        `-$${Math.abs(oldWay.totalCost || 0).toLocaleString()}`],
                ['Revenue generated', '$0'],
              ].map(([k, v]) => (
                <tr key={k} className="border-b border-atlas-red/10">
                  <td className="py-1.5 text-gray-400">{k}</td>
                  <td className="py-1.5 text-right font-semibold text-gray-200">{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-3 text-center">
            <p className="text-xs text-gray-500">Revenue generated</p>
            <p className="text-2xl font-black text-atlas-red">$0</p>
          </div>
        </div>

        {/* ATLAS way */}
        <div className="card p-4 border-atlas-green/30 bg-atlas-green/5">
          <p className="text-xs font-bold text-atlas-green uppercase tracking-wider mb-3">✅ ATLAS — Co-loaded with Cargo</p>
          <table className="w-full text-sm">
            <tbody>
              {[
                ['Freight rate',   `$${atlasWay.freightRate || 0}/TEU × ${atlasWay.containers || 0}`],
                ['Containers',     `${atlasWay.containers || 0} TEUs`],
                ['Total revenue',  `+$${(atlasWay.totalRevenue || 0).toLocaleString()}`],
                ['Net saving vs old', `+$${(atlasWay.netSaving || 0).toLocaleString()}`],
              ].map(([k, v]) => (
                <tr key={k} className="border-b border-atlas-green/10">
                  <td className="py-1.5 text-gray-400">{k}</td>
                  <td className="py-1.5 text-right font-semibold text-atlas-green">{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-3 bg-atlas-green/10 border border-atlas-green/30 rounded-xl p-3 text-center">
            <p className="text-xs text-gray-400 mb-0.5">Cost centre → Profit centre</p>
            <p className="text-2xl font-black text-atlas-green">+${(atlasWay.netSaving || 0).toLocaleString()}</p>
            <p className="text-xs text-gray-500">vs -${Math.abs(oldWay.totalCost || 0).toLocaleString()} old way</p>
          </div>
        </div>
      </div>

      {/* Saving pill */}
      <motion.div
        initial={{ scale:0.9, opacity:0 }}
        animate={{ scale:1, opacity:1 }}
        transition={{ delay:0.5 }}
        className="bg-atlas-green/10 border border-atlas-green/30 rounded-xl p-4 text-center"
      >
        <p className="text-sm text-gray-300 mb-1">Container type matching — automatic</p>
        <p className="text-3xl font-black text-atlas-green">+${(atlasWay.netSaving || 0).toLocaleString()}</p>
        <p className="text-xs text-gray-500 mt-1">Net saving · Containers travel full, not empty</p>
      </motion.div>

      {/* Approve Repositioning CTA */}
      <motion.div
        initial={{ opacity:0, y:10 }}
        animate={{ opacity:1, y:0 }}
        transition={{ delay:0.7 }}
        className="bg-maersk-teal/5 border border-maersk-teal/30 rounded-xl p-4"
      >
        <p className="text-xs text-gray-400 mb-3 text-center">
          ATLAS has pre-positioned containers and found co-load match. Ready to commit repositioning.
        </p>
        <button onClick={approveRepositioning} className="btn-primary w-full text-base py-3">
          ✅ Repositioning On Stage →
        </button>
        <p className="text-[10px] text-gray-600 text-center mt-2">
          Containers staged and ready — dashboard will update with port changes.
        </p>
      </motion.div>
    </motion.div>
  )
}
