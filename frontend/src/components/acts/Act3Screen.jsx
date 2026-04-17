import React from 'react'
import { motion } from 'framer-motion'
import { FLOW_STAGES, stageAtLeast } from '../../hooks/useAtlasFlow'

export default function Act3Screen({ flow, bookingTime }) {
  const { stage, scenario, goToAct4A } = flow
  if (!stageAtLeast(stage, FLOW_STAGES.ACT3_BOOKING)) return null

  // Once past ACT3_BOOKING the "View Recommendation" button is no longer needed
  // (user already clicked it and is on pipeline tab — we just show the card as a record)
  const canViewRec = stage === FLOW_STAGES.ACT3_BOOKING

  return (
    <motion.div
      initial={{ opacity:0, y:20 }}
      animate={{ opacity:1, y:0 }}
      className="space-y-6"
    >
      {/* Booking card */}
      <motion.div
        initial={{ scale:0.95, opacity:0 }}
        animate={{ scale:1, opacity:1 }}
        transition={{ delay:0.15 }}
        className="card p-6 border-maersk-teal/40 bg-maersk-dark/90"
        style={{ boxShadow:'0 0 40px rgba(0,180,216,0.12)' }}
      >
        {/* Incoming header */}
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <motion.div
              animate={{ opacity:[1,0.4,1] }}
              transition={{ duration:1.5, repeat:Infinity }}
              className="w-2 h-2 rounded-full bg-atlas-green"
            />
            <span className="text-xs font-bold text-atlas-green uppercase tracking-widest">
              Booking Request Arrives
            </span>
          </div>
          <span className="text-[10px] text-gray-500 font-mono">Apr 18, {bookingTime}</span>
        </div>

        {/* Customer */}
        <div className="bg-maersk-blue/10 border border-maersk-blue/20 rounded-xl p-4 mb-5">
          <h4 className="text-xl font-black text-white">{scenario.customer}</h4>
          <div className="flex items-center gap-2 mt-1.5">
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-atlas-red/20 text-atlas-red border border-atlas-red/40 font-bold uppercase">
              {scenario.urgency}
            </span>
            <span className="text-xs text-gray-400">{scenario.slaWindow} SLA window</span>
          </div>
        </div>

        {/* Details */}
        <div className="space-y-0">
          {[
            { label:'TEUs required',   value:`${scenario.teuRequired} TEUs`,                   icon:'📦' },
            { label:'Container type',  value:scenario.containerType,                           icon:'🏗' },
            { label:'Destination',     value:scenario.destination,                             icon:'📍' },
            { label:'Required by',     value:`${scenario.requiredBy} — ${scenario.slaWindow}`, icon:'📅' },
            { label:'SAP booking ref', value:scenario.sapRef,                                  icon:'📋' },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between py-2 border-b border-maersk-blue/10 last:border-0">
              <div className="flex items-center gap-2">
                <span className="text-sm">{item.icon}</span>
                <span className="text-xs text-gray-400">{item.label}</span>
              </div>
              <span className="text-sm font-semibold text-white">{item.value}</span>
            </div>
          ))}
        </div>

        <div className="mt-4 bg-maersk-dark/60 rounded-lg p-2 text-center">
          <span className="text-[10px] text-gray-500 font-mono">
            ref: {scenario.sapRef} · Received 06:42:17 UTC
          </span>
        </div>
      </motion.div>

      {/* Context */}
      <motion.div
        initial={{ opacity:0 }}
        animate={{ opacity:1 }}
        transition={{ delay:0.5 }}
        className="bg-atlas-green/10 border border-atlas-green/30 rounded-xl p-4 text-center"
      >
        <p className="text-sm font-bold text-atlas-green mb-1">
          ✅ ATLAS containers already staged — decision in 4.2 seconds
        </p>
        <p className="text-xs text-gray-400">
          Without ATLAS this triggers 72 hours of spreadsheets, phone calls, and missed SLAs.
        </p>
      </motion.div>

      {canViewRec && (
        <button onClick={goToAct4A} className="btn-primary w-full">
          View Recommendation →
        </button>
      )}
      {!canViewRec && (
        <div className="text-center py-2">
          <span className="badge-green">✓ Booking processed — see Agent Pipeline for recommendation</span>
        </div>
      )}
    </motion.div>
  )
}
