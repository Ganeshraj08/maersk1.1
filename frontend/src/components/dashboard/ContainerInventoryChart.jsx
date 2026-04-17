import React from 'react'
import { motion } from 'framer-motion'
import { CONTAINER_INVENTORY } from '../../data/maritimeData'

export default function ContainerInventoryChart() {
  return (
    <div className="card p-4">
      <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Container Inventory by Type</h3>
      <div className="space-y-3">
        {CONTAINER_INVENTORY.map((item, i) => (
          <motion.div
            key={item.type}
            initial={{ opacity:0, x:-20 }}
            animate={{ opacity:1, x:0 }}
            transition={{ delay: i * 0.08 }}
          >
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-300">{item.type}</span>
              <div className="flex items-center gap-3">
                <span className="text-gray-500 font-mono text-[10px]">{item.available.toLocaleString()} avail</span>
                <span className="font-bold" style={{ color: item.color }}>{item.fill}%</span>
              </div>
            </div>
            <div className="h-2 bg-maersk-dark/60 rounded-full overflow-hidden">
              <motion.div
                initial={{ width:0 }}
                animate={{ width: `${item.fill}%` }}
                transition={{ duration:0.8, delay: i * 0.1, ease:'easeOut' }}
                className="h-full rounded-full"
                style={{ background: `linear-gradient(90deg, ${item.color}99, ${item.color})` }}
              />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Total */}
      <div className="mt-4 pt-3 border-t border-maersk-blue/10 flex items-center justify-between text-xs">
        <span className="text-gray-500">Total Fleet</span>
        <span className="font-bold text-white">1,247,000 TEU</span>
      </div>
    </div>
  )
}
