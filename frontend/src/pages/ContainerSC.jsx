import React, { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

import { useAtlasFlow, FLOW_STAGES, stageAtLeast } from '../hooks/useAtlasFlow'
import {
  ATLAS_PORTS, FLEET_VESSELS, PROBLEM_STATE_KPIS, RESOLVED_KPIS,
  COST_HISTORY, NEWS_ITEMS, SYSTEM_INFO,
} from '../data/maritimeData'

import MetricCard              from '../components/dashboard/MetricCard'
import PortCard                from '../components/dashboard/PortCard'
import ContainerInventoryChart from '../components/dashboard/ContainerInventoryChart'
import DataSourcesPanel        from '../components/dashboard/DataSourcesPanel'
import AlertPanel              from '../components/alerts/AlertPanel'
import AgentPipeline           from '../components/acts/AgentPipeline'
import Act2AScreen             from '../components/acts/Act2AScreen'
import Act2CScreen             from '../components/acts/Act2CScreen'
import Act3Screen              from '../components/acts/Act3Screen'
import Act4BScreen             from '../components/acts/Act4BScreen'
import Act5Screen              from '../components/acts/Act5Screen'

const TABS = [
  { id:'overview',  label:'Global Monitor' },
  { id:'pipeline',  label:'Agent Pipeline' },
  { id:'vessels',   label:'Fleet & Vessels' },
  { id:'kpi',       label:'KPI Impact' },
  { id:'bookings',  label:'Bookings' },
]

const REGION_OPTIONS = ['All Regions', 'SEA', 'NEAC', 'NWEUR', 'IOSC', 'MEA', 'NAWC', 'NAEC', 'MED', 'SAF', 'SAM']
const STATUS_OPTIONS = ['All Status', 'Surplus', 'Shortage', 'Balanced']

const KPI_ICONS = {
  emptyRepositioningCost: '📦',
  slaAdherence:           '✅',
  manualTimeline:         '⏱',
  decisionTime:           '⚡',
  proactiveAlerts:        '🚨',
  bookingNotifications:   '📬',
  containerLeaseCost:     '🏗',
  coLoadSavings:          '💰',
  co2Reduction:           '🌿',
}

// ──────────────────────────────────────────────────────────────────────────────
//  VESSEL TABLE
// ──────────────────────────────────────────────────────────────────────────────
function VesselTable() {
  return (
    <div className="card overflow-hidden">
      <div className="p-4 border-b border-maersk-blue/20">
        <h3 className="font-bold text-white">Active Fleet — {FLEET_VESSELS.length} Vessels</h3>
        <p className="text-xs text-gray-500 mt-0.5">Live AIS tracking · Updated every 2 minutes</p>
      </div>
      <div className="overflow-x-auto">
        <table className="data-table">
          <thead>
            <tr>
              <th>Vessel</th>
              <th>Type</th>
              <th>Capacity</th>
              <th>Cargo %</th>
              <th>Empty TEU</th>
              <th>Route</th>
              <th>ETA</th>
              <th>Status</th>
              <th>Speed</th>
            </tr>
          </thead>
          <tbody>
            {FLEET_VESSELS.map((v, i) => (
              <motion.tr
                key={v.id}
                initial={{ opacity:0 }}
                animate={{ opacity:1 }}
                transition={{ delay: i * 0.06 }}
              >
                <td>
                  <div className="font-semibold text-white">{v.name}</div>
                  <div className="text-[10px] text-gray-500 font-mono">{v.id}</div>
                </td>
                <td className="text-gray-300">{v.type}</td>
                <td className="font-mono text-gray-300">{(v.capacityTEU/1000).toFixed(0)}K TEU</td>
                <td>
                  <div className="flex items-center gap-2">
                    <div className="w-16 h-1.5 bg-maersk-dark rounded-full overflow-hidden">
                      <div className="h-full rounded-full bg-maersk-teal" style={{ width:`${v.cargoPct}%` }} />
                    </div>
                    <span className="text-xs text-gray-300">{v.cargoPct}%</span>
                  </div>
                </td>
                <td className="font-mono text-atlas-amber">{v.emptyTEU.toLocaleString()}</td>
                <td>
                  <span className="font-mono text-xs text-gray-300">{v.fromPort}</span>
                  <span className="text-gray-600 mx-1">→</span>
                  <span className="font-mono text-xs text-maersk-teal">{v.toPort}</span>
                </td>
                <td className="text-xs text-gray-300">{v.eta}</td>
                <td>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    v.status === 'En Route' ? 'bg-atlas-green/20 text-atlas-green' :
                    v.status === 'Loading'  ? 'bg-atlas-amber/20 text-atlas-amber' :
                    'bg-maersk-blue/20 text-maersk-teal'
                  }`}>{v.status}</span>
                </td>
                <td className="font-mono text-xs text-gray-400">
                  {v.speed > 0 ? `${v.speed} kn` : 'Berthed'}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

// ──────────────────────────────────────────────────────────────────────────────
//  KPI IMPACT TAB
// ──────────────────────────────────────────────────────────────────────────────
function KpiImpactTab() {
  const rows = [
    { metric:'Cost per TEU',       before:'$412',     after:'$298',    change:'-28%',    unit:'USD' },
    { metric:'SLA Compliance',     before:'62.3%',    after:'97.8%',   change:'+35.5pp', unit:'%' },
    { metric:'Response Time',      before:'72 hours', after:'4.2 sec', change:'-99.99%', unit:'' },
    { metric:'CO₂ per TEU',        before:'baseline', after:'-53.4%',  change:'↓53.4%',  unit:'' },
    { metric:'Empty TEU Cost',     before:'$1.82B',   after:'$1.20B',  change:'-34%',    unit:'USD' },
    { metric:'Forecast Accuracy',  before:'Manual',   after:'94%',     change:'+94pp',   unit:'%' },
  ]

  return (
    <div className="space-y-5">
      <div className="card overflow-hidden">
        <div className="p-4 border-b border-maersk-blue/20">
          <h3 className="font-bold text-white">Before vs After ATLAS</h3>
          <p className="text-xs text-gray-500">Manual operations vs AI-driven automation</p>
        </div>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Metric</th>
                <th>Manual (Before)</th>
                <th>ATLAS (After)</th>
                <th>Improvement</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <motion.tr
                  key={row.metric}
                  initial={{ opacity:0 }}
                  animate={{ opacity:1 }}
                  transition={{ delay: i * 0.07 }}
                >
                  <td className="font-medium text-gray-200">{row.metric}</td>
                  <td className="text-atlas-red font-mono">{row.before}</td>
                  <td className="text-atlas-green font-mono font-bold">{row.after}</td>
                  <td><span className="badge-green">{row.change}</span></td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card p-5">
        <h4 className="font-semibold text-white mb-1">Empty Repositioning Cost — 5-Year Trend</h4>
        <p className="text-xs text-gray-500 mb-4">$ Millions · ATLAS introduced Q1 2025</p>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={COST_HISTORY} margin={{ top:5, right:20, bottom:5, left:10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,119,182,0.15)" />
            <XAxis dataKey="year" tick={{ fill:'#5B8DB8', fontSize:11 }} />
            <YAxis tick={{ fill:'#5B8DB8', fontSize:11 }} tickFormatter={v => `$${v}M`} />
            <Tooltip
              contentStyle={{ background:'#00243D', border:'1px solid rgba(0,119,182,0.3)', borderRadius:'8px', fontSize:11 }}
              labelStyle={{ color:'#00B4D8' }}
            />
            <Bar dataKey="cost"  name="Repo Cost"  fill="#0077B6" radius={[3,3,0,0]} />
            <Bar dataKey="lease" name="Lease Cost" fill="#00B4D8" radius={[3,3,0,0]} opacity={0.7} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-maersk-blue/5 border border-maersk-blue/20 rounded-2xl p-6 text-center">
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Total Annual Value Unlock</p>
        <p className="text-5xl font-black text-maersk-teal">$534M</p>
        <p className="text-sm text-gray-400 mt-2">Across all 5 ATLAS use cases · A.P. Møller-Maersk Network</p>
      </div>
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════════
//  MAIN PAGE
// ══════════════════════════════════════════════════════════════════════════════
export default function ContainerSC() {
  const flow = useAtlasFlow()
  const { stage, dashboardUpdated, repositioningApproved, scenario, receiveBooking } = flow

  const [activeTab,         setActiveTab]         = useState('overview')
  const [portFilter,        setPortFilter]        = useState('All Regions')
  const [statusFilter,      setStatusFilter]      = useState('All Status')
  const [newsIdx,           setNewsIdx]           = useState(0)
  const [time,              setTime]              = useState(new Date())
  const [bookingPopupReady, setBookingPopupReady] = useState(false)
  const [bookingTime,       setBookingTime]       = useState('')

  // Auto-trigger alert whenever stage is IDLE (on mount and after any reset/scenario change)
  useEffect(() => {
    if (stage === FLOW_STAGES.IDLE) {
      flow.triggerAlert()
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stage])

  // Clock tick
  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  // News ticker
  useEffect(() => {
    const t = setInterval(() => setNewsIdx(i => (i + 1) % NEWS_ITEMS.length), 6000)
    return () => clearInterval(t)
  }, [])

  // Tab auto-switching based on flow stage
  useEffect(() => {
    if (stage === FLOW_STAGES.AGENTS_RUNNING) {
      setActiveTab('pipeline')
    } else if (stage === FLOW_STAGES.REPOSITIONING_APPROVED) {
      // Return to overview so user sees updated dashboard first
      setActiveTab('overview')
      setBookingPopupReady(false)
    } else if (stage === FLOW_STAGES.ACT3_BOOKING) {
      setActiveTab('bookings')
      setBookingPopupReady(false)
    }
  }, [stage])

  // 3-second delay before booking popup appears (lets user absorb dashboard update first)
  useEffect(() => {
    if (stage === FLOW_STAGES.REPOSITIONING_APPROVED) {
      const t = setTimeout(() => {
        setBookingPopupReady(true)
        setBookingTime(new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }))
      }, 3000)
      return () => clearTimeout(t)
    }
  }, [stage])

  // Filtered ports
  const ports = useMemo(() => {
    let list = Object.values(ATLAS_PORTS)
    if (portFilter   !== 'All Regions') list = list.filter(p => p.region    === portFilter)
    if (statusFilter !== 'All Status')  list = list.filter(p => p.invStatus === statusFilter)
    return list
  }, [portFilter, statusFilter])

  // Which ports get the "updated" glow — based on scenario + stage
  const updatedPortIds = useMemo(() => {
    const ids = new Set()
    if (repositioningApproved || dashboardUpdated) {
      // Source depot port gets "updated" glow after approval
      const winDepot = scenario?.repositionOptions?.find(o => o.highlight)?.depotId
      if (winDepot) ids.add(winDepot)
    }
    if (dashboardUpdated) {
      // Destination port gets "updated" glow after full completion
      if (scenario?.portId) ids.add(scenario.portId)
    }
    return ids
  }, [repositioningApproved, dashboardUpdated, scenario])

  // ── KPI values ──────────────────────────────────────────────────────────────
  const displayKpis = useMemo(() => {
    const base = dashboardUpdated ? RESOLVED_KPIS : PROBLEM_STATE_KPIS

    // Dynamic: alerts count
    const alertCount = stageAtLeast(stage, FLOW_STAGES.ALERT_ACTIVE)
      ? (dashboardUpdated ? 0 : 1)
      : 0

    // Dynamic: booking notifications — show "1 new ↑" only once popup is ready
    let bookingVal = base.bookingNotifications.value
    if (dashboardUpdated) {
      bookingVal = '132 sent'
    } else if (bookingPopupReady && stage === FLOW_STAGES.REPOSITIONING_APPROVED) {
      bookingVal = '1 new ↑'
    }

    return {
      ...base,
      proactiveAlerts:      { ...base.proactiveAlerts,      value: alertCount },
      bookingNotifications: { ...base.bookingNotifications, value: bookingVal },
    }
  }, [stage, dashboardUpdated, bookingPopupReady])

  // Booking popup shows only after 3-second delay post-approval
  const bookingPending = stage === FLOW_STAGES.REPOSITIONING_APPROVED && bookingPopupReady

  return (
    <div className="min-h-screen bg-maersk-navy">

      {/* ── Navbar ─────────────────────────────────────────────────────── */}
      <header className="sticky top-0 z-50 bg-maersk-dark/95 backdrop-blur-md border-b border-maersk-blue/20">
        <div className="max-w-screen-2xl mx-auto px-4 h-14 flex items-center gap-4">
          <Link to="/" className="flex items-center gap-2 shrink-0">
            <div className="w-7 h-7 rounded-lg bg-maersk-teal flex items-center justify-center text-maersk-dark font-black text-xs">A</div>
            <span className="font-bold text-white text-sm">ATLAS</span>
          </Link>
          <span className="text-gray-600 text-sm">/</span>
          <span className="text-maersk-teal text-sm font-medium">Container Repositioning</span>
          <div className="ml-auto flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 text-xs">
              <span className="stat-pill">⚓ {SYSTEM_INFO.network.vessels}</span>
              <span className="stat-pill">🗺 {SYSTEM_INFO.network.ports}</span>
            </div>
            <span className="text-xs text-maersk-muted font-mono">{time.toISOString().slice(11,19)} UTC</span>
            <div className="flex items-center gap-1.5">
              <span className="live-dot" />
              <span className="text-atlas-green text-xs font-medium">LIVE</span>
            </div>

          </div>
        </div>
      </header>

      {/* ── News ticker ───────────────────────────────────────────────── */}
      <div className="news-ticker-wrap shrink-0">
        <div className="max-w-screen-2xl mx-auto px-4 flex items-center gap-3">
          <span className="bg-maersk-blue text-white text-[10px] font-bold px-2 py-0.5 rounded shrink-0 uppercase tracking-wide">
            News Agent
          </span>
          <AnimatePresence mode="wait">
            <motion.div
              key={newsIdx}
              initial={{ opacity:0, x:10 }}
              animate={{ opacity:1, x:0 }}
              exit={{ opacity:0, x:-10 }}
              className="truncate"
            >
              <a
                href={NEWS_ITEMS[newsIdx]?.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-maersk-muted hover:text-maersk-teal transition-colors truncate cursor-pointer"
              >
                {NEWS_ITEMS[newsIdx]?.text}
              </a>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* ── KPI Metrics row ──────────────────────────────────────────── */}
      <div className="max-w-screen-2xl mx-auto px-4 py-4 w-full">
        <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 2xl:grid-cols-9 gap-3 items-stretch">
          {Object.entries(displayKpis).map(([k, kpi], i) => {
            const isBookingCard  = k === 'bookingNotifications'
            const isAlertCard    = k === 'proactiveAlerts'
            const canClickBooking = isBookingCard && bookingPending

            return (
              <motion.div
                key={k}
                initial={{ opacity:0, y:10 }}
                animate={{ opacity:1, y:0 }}
                transition={{ delay: i * 0.05 }}
                className="h-full"
              >
                <MetricCard
                  label={kpi.label}
                  value={String(kpi.value)}
                  change={kpi.change}
                  period={kpi.period}
                  icon={KPI_ICONS[k] || '📊'}
                  chartData={
                    k === 'emptyRepositioningCost'
                      ? { points: COST_HISTORY, dataKey:'cost',  title:'5-Year Cost Trend',  unit:'$M' }
                      : k === 'containerLeaseCost'
                        ? { points: COST_HISTORY, dataKey:'lease', title:'5-Year Lease Trend', unit:'$M' }
                        : null
                  }
                  alert={
                    (isAlertCard  && Number(kpi.value) > 0) ||
                    (isBookingCard && bookingPending)
                  }
                  highlight={k === 'coLoadSavings' && dashboardUpdated}
                  inverse={['emptyRepositioningCost','manualTimeline','decisionTime','containerLeaseCost'].includes(k)}
                  onClick={canClickBooking ? receiveBooking : undefined}
                />
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* ── Red Booking Popup Modal (fixed overlay) ──────────────────── */}
      <AnimatePresence>
        {bookingPending && (
          <motion.div
            initial={{ opacity:0 }}
            animate={{ opacity:1 }}
            exit={{ opacity:0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
          >
            <motion.div
              initial={{ scale:0.88, opacity:0, y:24 }}
              animate={{ scale:1,    opacity:1, y:0 }}
              exit={{ scale:0.92,   opacity:0, y:10 }}
              transition={{ type:'spring', stiffness:320, damping:28 }}
              className="relative bg-maersk-dark border-2 border-atlas-red/60 rounded-2xl p-6 w-full max-w-sm mx-4"
              style={{ boxShadow:'0 0 60px rgba(239,68,68,0.35), 0 20px 60px rgba(0,0,0,0.6)' }}
            >
              {/* Animated pulse ring */}
              <motion.div
                animate={{ scale:[1,1.08,1], opacity:[0.4,0,0.4] }}
                transition={{ duration:1.6, repeat:Infinity }}
                className="absolute -inset-1 rounded-2xl border-2 border-atlas-red/40 pointer-events-none"
              />

              {/* Header */}
              <div className="flex items-start gap-3 mb-5">
                <motion.div
                  animate={{ scale:[1,1.18,1] }}
                  transition={{ duration:0.9, repeat:Infinity }}
                  className="w-11 h-11 rounded-xl bg-atlas-red/20 border border-atlas-red/50 flex items-center justify-center text-xl shrink-0"
                >
                  🚨
                </motion.div>
                <div>
                  <p className="text-sm font-black text-atlas-red uppercase tracking-wider">New Booking Request</p>
                  <p className="text-xs text-gray-400 mt-0.5">Incoming — requires immediate action</p>
                </div>
                <span className="ml-auto text-[10px] text-gray-500 font-mono shrink-0 mt-1">Apr 18 {bookingTime}</span>
              </div>

              {/* Details */}
              <div className="bg-atlas-red/10 border border-atlas-red/20 rounded-xl p-4 mb-4 space-y-2.5">
                {[
                  { label:'Customer',    value: scenario.customer,                                         bold:true  },
                  { label:'Required',    value: `${scenario.teuRequired} TEU · ${scenario.containerType}`, red:true   },
                  { label:'Destination', value: scenario.destination },
                  { label:'SLA Window',  value: scenario.slaWindow,                                        amber:true },
                ].map(r => (
                  <div key={r.label} className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">{r.label}</span>
                    <span className={`text-sm font-semibold ${r.red ? 'text-atlas-red' : r.amber ? 'text-atlas-amber' : r.bold ? 'text-white' : 'text-gray-200'}`}>
                      {r.value}
                    </span>
                  </div>
                ))}
              </div>

              {/* ATLAS ready */}
              <div className="bg-atlas-green/10 border border-atlas-green/30 rounded-xl p-3 mb-5 text-center">
                <p className="text-xs font-bold text-atlas-green">✅ ATLAS containers already staged</p>
                <p className="text-[10px] text-gray-400 mt-0.5">Decision time: 4.2 seconds</p>
              </div>

              <button
                onClick={receiveBooking}
                className="w-full py-3 rounded-xl font-bold text-white text-sm tracking-wide"
                style={{ background:'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)', boxShadow:'0 4px 18px rgba(239,68,68,0.4)' }}
              >
                View Booking Request →
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Tabs ─────────────────────────────────────────────────────── */}
      <div className="max-w-screen-2xl mx-auto px-4 w-full">
        <div className="flex gap-1 border-b border-maersk-blue/20 pb-0">
          {TABS.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            >
              {tab.label}
              {tab.id === 'pipeline' && stage !== FLOW_STAGES.IDLE && (
                <span className="ml-1.5 w-1.5 h-1.5 rounded-full bg-atlas-green inline-block animate-pulse-slow" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* ── Tab content ───────────────────────────────────────────────── */}
      <div className="max-w-screen-2xl mx-auto px-4 py-4 w-full pb-16">
        <AnimatePresence mode="wait">

          {/* ─ OVERVIEW TAB ─────────────────────────────────────────── */}
          {activeTab === 'overview' && (
            <motion.div
              key="overview"
              initial={{ opacity:0 }}
              animate={{ opacity:1 }}
              exit={{ opacity:0 }}
              className="space-y-5"
            >
              {/* Alert panel — shown on overview unless flow is past REPOSITIONING_APPROVED */}
              {!stageAtLeast(stage, FLOW_STAGES.REPOSITIONING_APPROVED) && (
                <AlertPanel flow={flow} />
              )}

              {/* Post-approval success card */}
              {stageAtLeast(stage, FLOW_STAGES.REPOSITIONING_APPROVED) && !dashboardUpdated && (
                <motion.div
                  initial={{ opacity:0, y:-10 }}
                  animate={{ opacity:1, y:0 }}
                  className="card p-4 border-atlas-green/40 bg-atlas-green/5 flex items-center gap-3"
                >
                  <div className="w-8 h-8 rounded-lg bg-atlas-green/20 border border-atlas-green/40 flex items-center justify-center text-base shrink-0">🟢</div>
                  <div>
                    <p className="text-sm font-bold text-atlas-green">Repositioning On Stage</p>
                    <p className="text-xs text-gray-400">
                      {scenario.teuRequired} TEU ready via {scenario.repositionOptions?.find(o => o.highlight)?.vessel || 'ATLAS vessel'} —
                      containers staged and awaiting booking confirmation
                    </p>
                  </div>
                </motion.div>
              )}

              {/* Ports section */}
              <div>
                <div className="flex items-center justify-between flex-wrap gap-3 mb-3">
                  <div>
                    <h3 className="font-bold text-white">Global Port Network</h3>
                    <p className="text-xs text-gray-500">
                      {Object.values(ATLAS_PORTS).length} ports monitored — click to expand container details
                    </p>
                  </div>
                  <div className="flex gap-2 flex-wrap">
                    <select
                      className="bg-maersk-dark border border-maersk-blue/30 text-xs text-gray-300 rounded-lg px-3 py-1.5 focus:outline-none focus:border-maersk-teal"
                      value={portFilter}
                      onChange={e => setPortFilter(e.target.value)}
                    >
                      {REGION_OPTIONS.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                    <select
                      className="bg-maersk-dark border border-maersk-blue/30 text-xs text-gray-300 rounded-lg px-3 py-1.5 focus:outline-none focus:border-maersk-teal"
                      value={statusFilter}
                      onChange={e => setStatusFilter(e.target.value)}
                    >
                      {STATUS_OPTIONS.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                  </div>
                </div>

                <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin">
                  {ports.map(port => (
                    <PortCard
                      key={port.id}
                      port={port}
                      updated={updatedPortIds.has(port.id)}
                    />
                  ))}
                  {ports.length === 0 && (
                    <p className="text-sm text-gray-500 py-4">No ports match the selected filters.</p>
                  )}
                </div>

                <div className="mt-2 flex flex-wrap gap-2">
                  {[
                    { label:'Surplus ports',  count:Object.values(ATLAS_PORTS).filter(p => p.invStatus==='Surplus').length,  color:'text-atlas-green' },
                    { label:'Shortage ports', count:Object.values(ATLAS_PORTS).filter(p => p.invStatus==='Shortage').length, color:'text-atlas-red'   },
                    { label:'Total ports',    count:Object.values(ATLAS_PORTS).length,                                       color:'text-maersk-teal' },
                  ].map(s => (
                    <span key={s.label} className={`text-xs ${s.color}`}>
                      <span className="font-bold">{s.count}</span> {s.label}
                    </span>
                  ))}
                </div>
              </div>

              {/* Bottom row: inventory + data sources */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="lg:col-span-2">
                  <ContainerInventoryChart />
                </div>
                <DataSourcesPanel />
              </div>
            </motion.div>
          )}

          {/* ─ PIPELINE TAB ─────────────────────────────────────────── */}
          {activeTab === 'pipeline' && (
            <motion.div
              key="pipeline"
              initial={{ opacity:0 }}
              animate={{ opacity:1 }}
              exit={{ opacity:0 }}
              className="space-y-5"
            >
              {/* Pipeline header */}
              <div className="card p-4 flex items-center justify-between gap-3">
                <div>
                  <h3 className="font-bold text-white">ATLAS Multi-Agent Pipeline</h3>
                  <p className="text-xs text-gray-500">Demand Sensing → Supply Finder → Optimization Agent · Scenario: <span className="text-maersk-teal">{flow.scenario?.name}</span></p>
                </div>
                <span className="badge-green shrink-0">
                  <span className="w-1.5 h-1.5 rounded-full bg-atlas-green animate-pulse-slow" />
                  {flow.scenario?.prediction?.confidence}% confidence
                </span>
              </div>

              {/* Alert panel */}
              <AlertPanel flow={flow} />

              {/* Agent pipeline terminal */}
              <AgentPipeline flow={flow} />

              {/* Act screens for pipeline — street-turn + co-load only */}
              <Act2AScreen flow={flow} />
              <Act2CScreen flow={flow} />

            </motion.div>
          )}

          {/* ─ FLEET TAB ────────────────────────────────────────────── */}
          {activeTab === 'vessels' && (
            <motion.div key="vessels" initial={{ opacity:0 }} animate={{ opacity:1 }} exit={{ opacity:0 }}>
              <VesselTable />
            </motion.div>
          )}

          {/* ─ KPI TAB ──────────────────────────────────────────────── */}
          {activeTab === 'kpi' && (
            <motion.div key="kpi" initial={{ opacity:0 }} animate={{ opacity:1 }} exit={{ opacity:0 }}>
              <KpiImpactTab />
            </motion.div>
          )}

          {/* ─ BOOKINGS TAB ─────────────────────────────────────────── */}
          {activeTab === 'bookings' && (
            <motion.div
              key="bookings"
              initial={{ opacity:0 }}
              animate={{ opacity:1 }}
              exit={{ opacity:0 }}
              className="space-y-5"
            >
              {/* Empty state — no booking yet */}
              {!stageAtLeast(stage, FLOW_STAGES.ACT3_BOOKING) && (
                <div className="flex flex-col items-center justify-center py-24 text-center gap-4">
                  <div className="w-16 h-16 rounded-2xl bg-maersk-blue/10 border border-maersk-blue/20 flex items-center justify-center text-3xl">
                    📬
                  </div>
                  <div>
                    <p className="text-white font-semibold">No bookings yet</p>
                    <p className="text-xs text-gray-500 mt-1">Incoming booking requests will appear here</p>
                  </div>
                </div>
              )}

              {/* Act 3 — Booking card */}
              {stageAtLeast(stage, FLOW_STAGES.ACT3_BOOKING) && (
                <Act3Screen flow={flow} bookingTime={bookingTime} />
              )}

              {/* Act 4A — ATLAS Recommendation (once user clicks View Recommendation) */}
              <Act2AScreen flow={flow} />

              {/* Act 4B — SAP Execution */}
              <Act4BScreen flow={flow} />

              {/* Act 5 — Performance / Prediction Reveal */}
              <Act5Screen flow={flow} />

              {/* Reset once complete */}
              {stage === FLOW_STAGES.COMPLETE && (
                <motion.div
                  initial={{ opacity:0 }}
                  animate={{ opacity:1 }}
                  className="pt-2"
                >
                  <button onClick={flow.reset} className="btn-secondary w-full">
                    ↺ Reset Demo — Run Another Scenario
                  </button>
                </motion.div>
              )}
            </motion.div>
          )}

        </AnimatePresence>
      </div>
    </div>
  )
}
