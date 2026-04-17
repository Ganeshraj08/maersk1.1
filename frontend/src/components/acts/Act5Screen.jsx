import React from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Area, AreaChart } from 'recharts'
import { FLOW_STAGES } from '../../hooks/useAtlasFlow'
import { ATLAS_PREDICTION, ACTUAL_BOOKING, PERFORMANCE_METRICS, PERFORMANCE_FORECAST, YEAR_FORECAST } from '../../data/maritimeData'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-maersk-dark border border-maersk-blue/30 rounded-lg p-3 text-xs">
      <p className="text-maersk-teal font-semibold mb-1">{label}</p>
      {payload.map(p => (
        <p key={p.dataKey} style={{ color: p.color }}>
          {p.name}: ${p.value}M
        </p>
      ))}
    </div>
  )
}

export default function Act5Screen({ flow }) {
  const { stage, complete, reset } = flow
  if (stage !== FLOW_STAGES.ACT5_CLOSING) return null

  const accuracy = PERFORMANCE_METRICS.predictionAccuracy

  return (
    <motion.div
      initial={{ opacity:0 }}
      animate={{ opacity:1 }}
      className="space-y-6"
    >
      {/* Teaser */}
      <div className="text-center py-4">
        <h2 className="text-2xl font-black text-white">Prediction vs Reality</h2>
        <p className="text-sm text-gray-400 mt-1">ATLAS predicted this 72 hours before any booking existed.</p>
      </div>

      {/* Prediction vs Actual comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* ATLAS prediction */}
        <motion.div
          initial={{ opacity:0, x:-30 }}
          animate={{ opacity:1, x:0 }}
          transition={{ delay:0.2 }}
          className="card p-5 border-maersk-blue/40"
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="w-2 h-2 rounded-full bg-maersk-teal" />
            <p className="text-xs font-bold text-maersk-teal uppercase tracking-widest">ATLAS PREDICTION — {ATLAS_PREDICTION.madeAt}</p>
          </div>
          <p className="text-[10px] text-gray-500 mb-3">{ATLAS_PREDICTION.madeLabel}</p>
          {[
            { label:'Expected demand', value:ATLAS_PREDICTION.expectedDemand },
            { label:'Region',          value:ATLAS_PREDICTION.region },
            { label:'Window',          value:ATLAS_PREDICTION.window },
            { label:'Confidence',      value:`${ATLAS_PREDICTION.confidence}%` },
            { label:'Action taken',    value:ATLAS_PREDICTION.actionTaken },
          ].map(item => (
            <div key={item.label} className="flex justify-between py-1.5 border-b border-maersk-blue/10 last:border-0">
              <span className="text-xs text-gray-400">{item.label}</span>
              <span className="text-xs font-semibold text-white">{item.value}</span>
            </div>
          ))}
        </motion.div>

        {/* Actual booking */}
        <motion.div
          initial={{ opacity:0, x:30 }}
          animate={{ opacity:1, x:0 }}
          transition={{ delay:0.3 }}
          className="card p-5 border-atlas-green/40 bg-atlas-green/5"
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="w-2 h-2 rounded-full bg-atlas-green animate-pulse-slow" />
            <p className="text-xs font-bold text-atlas-green uppercase tracking-widest">ACTUAL BOOKING — {ACTUAL_BOOKING.receivedAt}</p>
          </div>
          <p className="text-[10px] text-gray-500 mb-3">The real demand — arrived after prediction</p>
          {[
            { label:'Actual demand',        value:`${ACTUAL_BOOKING.actualDemand} TEUs` },
            { label:'Region',               value:ACTUAL_BOOKING.region },
            { label:'Decision time',        value:ACTUAL_BOOKING.decisionTime },
            { label:'Containers available', value:ACTUAL_BOOKING.containersAvailable },
          ].map(item => (
            <div key={item.label} className="flex justify-between py-1.5 border-b border-atlas-green/10 last:border-0">
              <span className="text-xs text-gray-400">{item.label}</span>
              <span className="text-xs font-semibold text-atlas-green">{item.value}</span>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Accuracy banner */}
      <motion.div
        initial={{ scale:0.9, opacity:0 }}
        animate={{ scale:1, opacity:1 }}
        transition={{ delay:0.5 }}
        className="bg-atlas-green/10 border border-atlas-green/30 rounded-2xl p-5 text-center"
      >
        <p className="text-sm font-bold text-atlas-green uppercase tracking-wider mb-1">
          Prediction accuracy: {accuracy}% — Containers staged 72 hours before the request arrived
        </p>
        <p className="text-xs text-gray-400">This was never a crisis. ATLAS turned it into a managed event 3 days earlier.</p>
      </motion.div>

      {/* KPI metrics row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label:'TEUs Staged at Zero Cost',  value:'340',    unit:'TEU',  color:'text-maersk-teal'  },
          { label:'Revenue from Cargo Co-Load',value:'$188K',  unit:'',     color:'text-atlas-green'  },
          { label:'Revenue from Second Slot',  value:'$58K',   unit:'',     color:'text-atlas-green'  },
          { label:'Crisis → Booking',          value:'4.2s',   unit:'',     color:'text-atlas-amber'  },
        ].map(kpi => (
          <div key={kpi.label} className="card p-4 text-center">
            <p className={`text-2xl font-black ${kpi.color}`}>{kpi.value}</p>
            <p className="text-[10px] text-gray-500 mt-1">{kpi.label}</p>
          </div>
        ))}
      </div>

      {/* Cost stopped */}
      <motion.div
        initial={{ opacity:0 }}
        animate={{ opacity:1 }}
        transition={{ delay:0.8 }}
        className="bg-atlas-red/10 border border-atlas-red/30 rounded-xl p-4 flex items-center justify-between"
      >
        <div>
          <p className="text-xs text-gray-400">Cost accumulated while we stood here</p>
          <p className="text-sm text-gray-300">ATLAS stops this number permanently</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-atlas-red font-semibold uppercase tracking-wider mb-0.5">Manual Overhead</p>
          <p className="text-3xl font-black text-atlas-red">${PERFORMANCE_METRICS.costAccumulated.toLocaleString()}</p>
        </div>
      </motion.div>

      {/* Performance Forecast Chart */}
      <div className="card p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h4 className="font-bold text-white">3-Year Performance Forecast</h4>
            <p className="text-xs text-gray-500">Cumulative value unlock — ATLAS platform</p>
          </div>
          <div className="flex gap-3">
            {YEAR_FORECAST.map(y => (
              <div key={y.year} className="text-right">
                <p className="text-[10px] text-gray-500">{y.year}</p>
                <p className="text-sm font-black" style={{ color: y.color }}>{y.label}</p>
              </div>
            ))}
          </div>
        </div>
        <ResponsiveContainer width="100%" height={180}>
          <AreaChart data={PERFORMANCE_FORECAST} margin={{ top:5, right:20, bottom:5, left:10 }}>
            <defs>
              <linearGradient id="cumGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#00B4D8" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#00B4D8" stopOpacity={0}   />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,119,182,0.15)" />
            <XAxis dataKey="month" tick={{ fill:'#5B8DB8', fontSize:10 }} />
            <YAxis tick={{ fill:'#5B8DB8', fontSize:10 }} tickFormatter={v => `$${v}M`} />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="cumulative" name="Cumulative Value"
              stroke="#00B4D8" strokeWidth={2} fill="url(#cumGrad)" />
            <Bar dataKey="monthly" name="Monthly Value" fill="#0077B6" opacity={0.6} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Complete flow */}
      <div className="flex gap-3">
        <button
          onClick={complete}
          className="btn-primary flex-1 py-3"
        >
          ✓ Complete — Update Dashboard
        </button>
        <button onClick={reset} className="btn-secondary px-6">
          Reset Demo
        </button>
      </div>
    </motion.div>
  )
}
