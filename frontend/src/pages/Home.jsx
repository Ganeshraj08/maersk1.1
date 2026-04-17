import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { USE_CASES, SYSTEM_INFO, NEWS_ITEMS, IMPACT, DEMAND_SCENARIOS } from '../data/maritimeData'

// ── KPI tiles shown in hero ────────────────────────────────────────────────────
const HERO_KPIS = [
  { label:'Container Vessels', value:'700',  unit:'', icon:'⚓', color:'text-maersk-teal'  },
  { label:'Port Terminals',    value:'72',   unit:'', icon:'🗺', color:'text-maersk-light' },
  { label:'Containers / Year', value:'12M',  unit:'', icon:'📦', color:'text-atlas-amber'  },
  { label:'Annual Revenue',    value:'$51B', unit:'', icon:'💰', color:'text-atlas-green'  },
]

// ── Card icons & accent colours per use-case ──────────────────────────────────
const CARD_STYLES = {
  control_tower:       { bg:'from-[#1E3A5F] to-[#00243D]', accent:'#5B8DB8',  border:'border-[#5B8DB8]/30' },
  container_sc:        { bg:'from-[#003D6B] to-[#001D35]', accent:'#00B4D8',  border:'border-[#00B4D8]/40' },
  fuel_optimization:   { bg:'from-[#3B2800] to-[#1A1200]', accent:'#F59E0B',  border:'border-amber-500/30' },
  pricing_intelligence:{ bg:'from-[#002B1F] to-[#001410]', accent:'#10B981',  border:'border-emerald-500/30'},
  aiops:               { bg:'from-[#2D1B5E] to-[#150B30]', accent:'#8B5CF6',  border:'border-purple-500/30' },
}

// ── Animated counter ──────────────────────────────────────────────────────────
function Counter({ target, duration = 1500 }) {
  const [current, setCurrent] = useState(0)
  useEffect(() => {
    const numeric = parseFloat(target.replace(/[^0-9.]/g, ''))
    const start  = Date.now()
    const tick = () => {
      const elapsed = Date.now() - start
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setCurrent(Math.floor(numeric * eased))
      if (progress < 1) requestAnimationFrame(tick)
      else setCurrent(numeric)
    }
    requestAnimationFrame(tick)
  }, [target, duration])
  const prefix = target.startsWith('$') ? '$' : ''
  const suffix = target.endsWith('B') ? 'B' : target.endsWith('M') ? 'M' : target.endsWith('%') ? '%' : ''
  return <span>{prefix}{current}{suffix}</span>
}

// ── Single use-case card ────────────────────────────────────────────────────────
function UseCaseCard({ uc, onLaunch }) {
  const style = CARD_STYLES[uc.id] || CARD_STYLES.control_tower
  const [hovered, setHovered] = useState(false)

  return (
    <motion.div
      layout
      initial={{ opacity:0, y:30 }}
      animate={{ opacity:1, y:0 }}
      whileHover={{ y:-4, scale:1.01 }}
      transition={{ duration:0.3 }}
      className={`relative rounded-2xl border ${style.border} bg-gradient-to-br ${style.bg}
                  overflow-hidden cursor-default flex flex-col`}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{ minHeight:'280px' }}
    >
      {/* Glow overlay on hover */}
      <div
        className="absolute inset-0 opacity-0 transition-opacity duration-500 pointer-events-none rounded-2xl"
        style={{ opacity: hovered ? 0.08 : 0, background: `radial-gradient(circle at 60% 30%, ${style.accent}, transparent 70%)` }}
      />

      {/* Active indicator */}
      {uc.active && (
        <div className="absolute top-3 right-3 flex items-center gap-1.5 bg-atlas-green/20 border border-atlas-green/40 px-2.5 py-1 rounded-full">
          <span className="w-1.5 h-1.5 rounded-full bg-atlas-green animate-pulse-slow" />
          <span className="text-atlas-green text-[10px] font-bold uppercase tracking-widest">Live</span>
        </div>
      )}

      <div className="p-6 flex flex-col flex-1">
        {/* Icon + title */}
        <div className="flex items-start gap-4 mb-4">
          <div
            className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shrink-0"
            style={{ background:`${style.accent}20`, border:`1px solid ${style.accent}40` }}
          >
            {uc.icon}
          </div>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-0.5" style={{ color: style.accent }}>
              {uc.subtitle}
            </p>
            <h3 className="text-lg font-bold text-white leading-tight">{uc.title}</h3>
          </div>
        </div>

        {/* KPI chips */}
        <div className="flex flex-wrap gap-1.5 mb-5">
          {uc.kpis.map(k => (
            <span key={k} className="text-[11px] px-2.5 py-0.5 rounded-full font-medium"
              style={{ background:`${style.accent}15`, color: style.accent, border:`1px solid ${style.accent}30` }}>
              {k}
            </span>
          ))}
        </div>

        {/* Annual value */}
        <div className="flex items-center justify-between mt-auto mb-4">
          <div>
            <p className="text-[10px] text-gray-500 uppercase tracking-wider">Annual Value</p>
            <p className="text-xl font-bold" style={{ color: style.accent }}>{uc.annualValue}</p>
          </div>
        </div>

        {/* CTA */}
        {uc.active ? (
          <motion.button
            whileHover={{ scale:1.03 }}
            whileTap={{ scale:0.97 }}
            onClick={() => onLaunch(uc)}
            className="w-full py-2.5 rounded-xl font-semibold text-sm transition-all duration-200"
            style={{ background: style.accent, color:'#00243D' }}
          >
            Launch Container SC →
          </motion.button>
        ) : null}
      </div>
    </motion.div>
  )
}

// ══════════════════════════════════════════════════════════════════════════════
//  HOME PAGE
// ══════════════════════════════════════════════════════════════════════════════
export default function Home() {
  const navigate = useNavigate()
  const [newsIdx, setNewsIdx]         = useState(0)
  const [time, setTime]               = useState(new Date())
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [activeScenario, setActiveScenario] = useState(
    () => localStorage.getItem('atlas_scenario') || 'vietnam_surge'
  )

  const handleScenarioChange = (id) => {
    localStorage.setItem('atlas_scenario', id)
    setActiveScenario(id)
    setSettingsOpen(false)
  }

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(t)
  }, [])
  useEffect(() => {
    const t = setInterval(() => setNewsIdx(i => (i + 1) % NEWS_ITEMS.length), 6000)
    return () => clearInterval(t)
  }, [])

  const handleLaunch = (uc) => {
    if (uc.route) navigate(uc.route)
  }

  return (
    <div className="min-h-screen bg-maersk-navy overflow-x-hidden">

      {/* ── Top navbar ────────────────────────────────────────────────── */}
      <header className="sticky top-0 z-50 bg-maersk-dark/95 backdrop-blur-md border-b border-maersk-blue/20">
        <div className="max-w-screen-2xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            {/* Logo */}
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-maersk-teal flex items-center justify-center text-maersk-dark font-black text-sm">A</div>
              <div>
                <span className="font-bold text-white tracking-wide text-sm">ATLAS</span>
                <span className="text-maersk-muted text-xs ml-1.5">Maritime Intelligence</span>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-1 text-xs text-maersk-muted">
              <span className="text-maersk-blue/50">|</span>
              <span className="ml-2">TCS Crystallus Platform</span>
              <span className="ml-2 px-1.5 py-0.5 rounded bg-maersk-blue/20 text-maersk-teal text-[10px] font-semibold">v{SYSTEM_INFO.version}</span>
            </div>
          </div>

          <div className="flex items-center gap-5">
            {/* Live stats */}
            <div className="hidden lg:flex items-center gap-3 text-xs">
              <span className="stat-pill">⚓ {SYSTEM_INFO.network.vessels}+ vessels</span>
              <span className="stat-pill">🗺 {SYSTEM_INFO.network.ports}+ terminals</span>
              <span className="stat-pill">📦 {(SYSTEM_INFO.network.emptyTEUs/1000000).toFixed(0)}M+ containers</span>
            </div>
            {/* Clock */}
            <div className="text-xs text-maersk-muted font-mono">
              UTC {time.toISOString().slice(11,19)}
            </div>
            {/* Settings gear */}
            <div className="relative">
              <button
                onClick={() => setSettingsOpen(o => !o)}
                className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${
                  settingsOpen
                    ? 'bg-maersk-teal/20 border border-maersk-teal/50 text-maersk-teal'
                    : 'bg-maersk-blue/10 border border-maersk-blue/30 text-gray-400 hover:text-white hover:border-maersk-blue/60'
                }`}
                title="Demo settings"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </button>

              <AnimatePresence>
                {settingsOpen && (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setSettingsOpen(false)} />
                    <motion.div
                      initial={{ opacity:0, y:-8, scale:0.95 }}
                      animate={{ opacity:1, y:0,  scale:1 }}
                      exit={{ opacity:0,  y:-8, scale:0.95 }}
                      transition={{ duration:0.15 }}
                      className="absolute right-0 top-10 z-50 w-72 bg-maersk-dark border border-maersk-blue/30 rounded-xl shadow-2xl p-4"
                      style={{ boxShadow:'0 8px 40px rgba(0,0,0,0.6)' }}
                    >
                      <p className="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-3">Demo Settings</p>

                      <div className="mb-3">
                        <p className="text-xs text-gray-400 mb-1.5">Active Demand Scenario</p>
                        <select
                          className="w-full bg-maersk-navy border border-maersk-blue/30 text-xs text-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:border-maersk-teal"
                          value={activeScenario}
                          onChange={e => handleScenarioChange(e.target.value)}
                        >
                          {Object.values(DEMAND_SCENARIOS).map(s => (
                            <option key={s.id} value={s.id}>{s.name}</option>
                          ))}
                        </select>
                        <p className="text-[10px] text-gray-600 mt-1.5">
                          Select a scenario before launching Container SC.
                        </p>
                      </div>

                      <div className="bg-maersk-blue/10 border border-maersk-blue/20 rounded-lg p-2.5">
                        <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Active</p>
                        <p className="text-xs font-semibold text-maersk-teal">{DEMAND_SCENARIOS[activeScenario]?.name}</p>
                        <p className="text-[10px] text-gray-500 mt-0.5">
                          {DEMAND_SCENARIOS[activeScenario]?.prediction?.demand} · {DEMAND_SCENARIOS[activeScenario]?.prediction?.confidence}% confidence
                        </p>
                      </div>
                    </motion.div>
                  </>
                )}
              </AnimatePresence>
            </div>

            {/* Live dot */}
            <div className="flex items-center gap-1.5">
              <span className="live-dot" />
              <span className="text-atlas-green text-xs font-medium">LIVE</span>
            </div>
          </div>
        </div>
      </header>

      {/* ── News ticker ────────────────────────────────────────────────── */}
      <div className="news-ticker-wrap">
        <div className="max-w-screen-2xl mx-auto px-6 flex items-center gap-3">
          <span className="bg-maersk-blue text-white text-[10px] font-bold px-2 py-0.5 rounded shrink-0 uppercase tracking-wide">
            News Agent
          </span>
          <AnimatePresence mode="wait">
            <motion.div
              key={newsIdx}
              initial={{ opacity:0, x:20 }}
              animate={{ opacity:1, x:0 }}
              exit={{ opacity:0, x:-20 }}
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

      {/* ── Hero section ──────────────────────────────────────────────── */}
      <section className="relative overflow-hidden">
        {/* Ocean bg */}
        <div className="absolute inset-0 bg-grid-pattern opacity-30" />
        <div className="absolute inset-0" style={{ background:'radial-gradient(ellipse 80% 60% at 50% -20%, rgba(0,119,182,0.25) 0%, transparent 70%)' }} />

        <div className="relative max-w-screen-2xl mx-auto px-6 pt-14 pb-10">
          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">
            {/* Text */}
            <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} className="max-w-2xl">
              <div className="flex items-center gap-2 mb-3">
                <span className="badge-blue">A.P. Møller-Maersk</span>
                <span className="badge-green">
                  <span className="w-1.5 h-1.5 rounded-full bg-atlas-green animate-pulse-slow" />
                  All Systems Operational
                </span>
              </div>
              <h1 className="text-4xl lg:text-5xl font-black text-white leading-tight mb-3">
                Maritime Intelligence
                <span className="block text-maersk-teal">Control Tower</span>
              </h1>
              <p className="text-base text-gray-400 leading-relaxed max-w-xl">
                AI-driven insights across the world's largest container shipping network.
                Real-time decisions. Autonomous execution. Zero manual overhead.
              </p>
            </motion.div>

            {/* KPI tiles */}
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-2 xl:grid-cols-4 gap-3 w-full lg:w-auto">
              {HERO_KPIS.map((k, i) => (
                <motion.div
                  key={k.label}
                  initial={{ opacity:0, scale:0.9 }}
                  animate={{ opacity:1, scale:1 }}
                  transition={{ delay: i * 0.1 }}
                  className="card p-4 text-center min-w-[100px]"
                >
                  <div className="text-2xl mb-1">{k.icon}</div>
                  <div className={`text-xl font-black ${k.color}`}>
                    <Counter target={k.value} />
                  </div>
                  <div className="text-[10px] text-gray-500 uppercase tracking-wider mt-0.5">{k.label}</div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Impact bar */}
          <motion.div
            initial={{ opacity:0 }}
            animate={{ opacity:1 }}
            transition={{ delay:0.4 }}
            className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-3"
          >
            {[
              { before: IMPACT.costPerTEUBefore, after: IMPACT.costPerTEUAfter, label:'Cost/TEU', unit:'$', reduction:IMPACT.costReduction },
              { before: IMPACT.slaBefore, after: IMPACT.slaAfter, label:'SLA Compliance', unit:'', reduction:'+35.5pp' },
              { before: IMPACT.responseTimeBefore, after: IMPACT.responseTimeAfter, label:'Response Time', unit:'', reduction:'99.99% faster' },
              { before: '–', after: IMPACT.co2Reduction, label:'CO₂ Reduction', unit:'', reduction:'vs baseline' },
            ].map(item => (
              <div key={item.label} className="bg-maersk-dark/60 border border-maersk-blue/15 rounded-xl p-3.5">
                <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">{item.label}</p>
                <div className="flex items-center gap-2">
                  {item.before !== '–' && (
                    <>
                      <span className="text-sm text-gray-500 line-through">{item.unit}{item.before}</span>
                      <span className="text-gray-600">→</span>
                    </>
                  )}
                  <span className="text-lg font-bold text-atlas-green">{item.unit}{item.after}</span>
                </div>
                <p className="text-[10px] text-maersk-teal mt-1">{item.reduction}</p>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── Use Cases ────────────────────────────────────────────────────── */}
      <section className="max-w-screen-2xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-white">AI Modules</h2>
            <p className="text-sm text-gray-500 mt-0.5">Powered by TCS Crystallus — Click Container SC to explore the full demo</p>
          </div>
          <span className="badge-blue">5 modules</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {USE_CASES.map((uc, i) => (
            <motion.div
              key={uc.id}
              initial={{ opacity:0, y:20 }}
              animate={{ opacity:1, y:0 }}
              transition={{ delay: i * 0.08 }}
            >
              <UseCaseCard uc={uc} onLaunch={handleLaunch} />
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Footer ────────────────────────────────────────────────────── */}
      <footer className="border-t border-maersk-blue/10 mt-8">
        <div className="max-w-screen-2xl mx-auto px-6 py-4 flex items-center justify-between text-xs text-gray-600">
          <span>ATLAS v{SYSTEM_INFO.version} — TCS Crystallus Platform — A.P. Møller-Maersk</span>
          <span>{new Date().getFullYear()} © Confidential</span>
        </div>
      </footer>
    </div>
  )
}
