import React from 'react'
import { motion } from 'framer-motion'
import { DATA_SOURCES } from '../../data/maritimeData'

export default function DataSourcesPanel() {
  return (
    <div className="card p-4">
      <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Live Data Sources</h3>
      <div className="space-y-2">
        {DATA_SOURCES.map((src, i) => (
          <motion.div
            key={src.name}
            initial={{ opacity:0 }}
            animate={{ opacity:1 }}
            transition={{ delay: i * 0.07 }}
            className="flex items-center justify-between py-1.5 border-b border-maersk-blue/10 last:border-0"
          >
            <div className="flex items-center gap-2">
              <span className="text-base">{src.icon}</span>
              <div>
                <p className="text-xs font-medium text-gray-200">{src.name}</p>
                <p className="text-[10px] text-gray-500">{src.records} records · {src.latency}</p>
              </div>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-atlas-green animate-pulse-slow" />
              <span className="text-[10px] text-atlas-green font-medium">Connected</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
