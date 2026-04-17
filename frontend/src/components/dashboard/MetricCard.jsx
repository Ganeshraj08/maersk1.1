import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function MetricCard({ label, value, unit, change, period, icon, onClick, chartData, highlight, alert, inverse = false }) {
  const [showChart, setShowChart] = useState(false)
  const up   = change > 0
  const down = change < 0
  const isNeg = inverse || label.toLowerCase().includes('cost') || label.toLowerCase().includes('time')
  const chartPoints = chartData?.points || []
  const chartValueKey = chartData?.dataKey || 'cost'
  const chartTitle = chartData?.title || '5-Year Trend'
  const chartUnit = chartData?.unit || ''
  const maxChartValue = chartPoints.length ? Math.max(...chartPoints.map(x => x[chartValueKey] || 0), 1) : 1

  const changeColor = isNeg
    ? (down ? 'text-atlas-green' : up ? 'text-atlas-red' : 'text-gray-400')
    : (up   ? 'text-atlas-green' : down ? 'text-atlas-red' : 'text-gray-400')

  const handleClick = () => {
    if (chartData) setShowChart(s => !s)
    if (onClick) onClick()
  }

  return (
    <motion.div
      whileHover={{ y:-2, borderColor:'rgba(0,180,216,0.4)' }}
      className={`metric-card relative h-full min-h-[136px] ${highlight ? 'border-maersk-teal/50 glow-teal' : ''} ${alert ? 'border-atlas-amber/60 glow-amber' : ''}`}
      onClick={handleClick}
      style={{ cursor: chartData || onClick ? 'pointer' : 'default' }}
    >
      {/* Alert pulse */}
      {alert && (
        <span className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-atlas-amber animate-pulse" />
      )}

      <div className="flex items-start justify-between mb-3">
        <div className="text-xl">{icon}</div>
        {change !== undefined && change !== 0 && (
          <span className={`text-xs font-semibold ${changeColor}`}>
            {up ? '↑' : '↓'} {Math.abs(change)}%
          </span>
        )}
      </div>

      <div className="metric-value mb-0.5">{value}</div>
      <div className="metric-label">{label}</div>

      {period && (
        <div className="mt-2 text-[10px] text-gray-600 uppercase tracking-wider">{period}</div>
      )}

      {chartData && (
        <div className="mt-2 text-[10px] text-maersk-teal">{chartTitle}</div>
      )}

      {/* Mini bar chart on expand */}
      <AnimatePresence>
        {showChart && chartData && (
          <motion.div
            initial={{ height:0, opacity:0 }}
            animate={{ height:'auto', opacity:1 }}
            exit={{ height:0, opacity:0 }}
            className="mt-3 pt-3 border-t border-maersk-blue/20 overflow-hidden"
          >
            <p className="text-[10px] text-gray-500 mb-2 uppercase tracking-wider">{chartTitle} ({chartUnit})</p>
            <div className="flex items-end gap-1.5 h-14">
              {chartPoints.map((d, i) => (
                <div key={d.year} className="flex-1 flex flex-col items-center gap-0.5">
                  <div
                    className="w-full rounded-t transition-all duration-500"
                    style={{
                      height: `${((d[chartValueKey] || 0) / maxChartValue) * 48}px`,
                      background: i === chartPoints.length - 1 ? '#00B4D8' : 'rgba(0,119,182,0.5)',
                    }}
                  />
                  <span className="text-[8px] text-maersk-light font-mono">{d[chartValueKey]}</span>
                  <span className="text-[8px] text-gray-600">{d.year}</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
