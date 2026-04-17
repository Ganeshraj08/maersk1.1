import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const CONTAINER_TYPES = [
  { type:'40ft Dry',    base:52, spread:18, color:'#0077B6' },
  { type:'20ft Dry',    base:47, spread:22, color:'#00B4D8' },
  { type:'40ft Reefer', base:26, spread:16, color:'#42B4E6' },
  { type:'In Transit',  base:38, spread:20, color:'#8B5CF6' },
]

function getPortInventoryMix(port, updated) {
  const seed = port.id.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0)
  const total = Math.max(Math.abs(port.surplusTEU), 1)
  const rawWeights = CONTAINER_TYPES.map((ct, idx) => {
    const variance = (seed * (idx + 5)) % ct.spread
    const updatedBias = updated ? (idx === 0 ? 5 : idx === 1 ? 4 : 2) : 0
    return Math.max(1, ct.base + variance + updatedBias)
  })

  const weightSum = rawWeights.reduce((sum, weight) => sum + weight, 0)
  const allocations = rawWeights.map((weight, idx) => {
    const exact = (weight / weightSum) * total
    const available = Math.floor(exact)
    return {
      ...CONTAINER_TYPES[idx],
      exact,
      available,
      remainder: exact - available,
    }
  })

  let remaining = total - allocations.reduce((sum, item) => sum + item.available, 0)
  const ranked = [...allocations].sort((a, b) => b.remainder - a.remainder)

  for (let i = 0; i < remaining; i += 1) {
    const target = ranked[i % ranked.length]
    target.available += 1
  }

  return allocations.map(item => ({
    type: item.type,
    color: item.color,
    available: item.available,
    pct: Math.round((item.available / total) * 100),
  }))
}

export default function PortCard({ port, updated }) {
  const [expanded, setExpanded] = useState(false)
  const isSurplus  = port.invStatus === 'Surplus'
  const isShortage = port.invStatus === 'Shortage'
  const teu = port.surplusTEU
  const inventoryMix = getPortInventoryMix(port, updated)

  const statusColor  = isSurplus ? '#10B981' : isShortage ? '#EF4444' : '#F59E0B'
  const statusLabel  = isSurplus ? 'Surplus' : isShortage ? 'Shortage' : 'Balanced'
  const statusBg     = isSurplus ? 'bg-atlas-green/10 border-atlas-green/30' : isShortage ? 'bg-atlas-red/10 border-atlas-red/30' : 'bg-atlas-amber/10 border-atlas-amber/30'

  return (
    <motion.div
      layout
      className={`shrink-0 w-52 rounded-xl border cursor-pointer transition-all duration-300
                  ${expanded ? 'border-maersk-teal/60 bg-maersk-slate/60' : 'border-maersk-blue/20 bg-maersk-slate/30 hover:border-maersk-blue/40'}`}
      onClick={() => setExpanded(e => !e)}
      style={{ boxShadow: updated ? '0 0 12px rgba(16,185,129,0.4)' : undefined }}
    >
      <div className="p-3.5">
        {/* Port ID + region */}
        <div className="flex items-start justify-between mb-2">
          <div>
            <span className="text-[10px] font-bold text-maersk-teal uppercase tracking-widest">{port.id}</span>
            <p className="text-sm font-semibold text-white leading-tight">{port.name}</p>
            <p className="text-[10px] text-gray-500">{port.country} · {port.region}</p>
          </div>
          {port.depot && (
            <span className="badge-blue text-[9px] py-0">Depot</span>
          )}
        </div>

        {/* Status + TEU */}
        <div className={`flex items-center justify-between rounded-lg px-2.5 py-1.5 border ${statusBg}`}>
          <span className="text-xs font-semibold" style={{ color: statusColor }}>{statusLabel}</span>
          <span className="text-sm font-black" style={{ color: statusColor }}>
            {teu > 0 ? '+' : ''}{teu.toLocaleString()} TEU
          </span>
        </div>

        {/* Berths */}
        <div className="flex items-center justify-between mt-2 text-[10px] text-gray-500">
          <span>Berths</span>
          <span className="text-maersk-light font-medium">{port.berths}</span>
        </div>

        {/* Expand hint */}
        <div className="mt-2 text-[10px] text-maersk-muted text-center">
          {expanded ? '▲ Hide details' : '▼ Container details'}
        </div>
      </div>

      {/* Expanded container inventory */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height:0, opacity:0 }}
            animate={{ height:'auto', opacity:1 }}
            exit={{ height:0, opacity:0 }}
            className="overflow-hidden border-t border-maersk-blue/20 px-3.5 pb-3.5"
          >
            <p className="text-[10px] text-gray-500 uppercase tracking-wider pt-3 mb-2">Container Availability by Type</p>
            <div className="space-y-2">
              {inventoryMix.map(ct => {
                return (
                  <div key={ct.type}>
                    <div className="flex justify-between text-[10px] mb-0.5">
                      <span className="text-gray-400">{ct.type}</span>
                      <span className="font-medium" style={{ color: ct.color }}>{ct.available} TEU · {ct.pct}%</span>
                    </div>
                    <div className="h-1.5 bg-maersk-dark/60 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width:0 }}
                        animate={{ width: `${ct.pct}%` }}
                        transition={{ duration:0.6, delay:0.1 }}
                        className="h-full rounded-full"
                        style={{ background: ct.color }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Coordinates */}
            <div className="mt-3 pt-2 border-t border-maersk-blue/10 grid grid-cols-2 gap-1">
              <div className="text-[10px]">
                <span className="text-gray-600">Lat </span>
                <span className="text-maersk-muted font-mono">{port.lat.toFixed(2)}°</span>
              </div>
              <div className="text-[10px]">
                <span className="text-gray-600">Lon </span>
                <span className="text-maersk-muted font-mono">{port.lon.toFixed(2)}°</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
