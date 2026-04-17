// ═══════════════════════════════════════════════════════════════════
//  ATLAS Maritime Intelligence — Data Layer
// ═══════════════════════════════════════════════════════════════════

export const SYSTEM_INFO = {
  name: 'ATLAS',
  version: '3.0',
  platform: 'TCS Crystallus',
  client: 'A.P. Møller-Maersk',
  network: { ports: 72, countries: 130, vessels: 700, depots: 450, emptyTEUs: 12_000_000 },
}

// ─── PORTS ───────────────────────────────────────────────────────────────────
export const ATLAS_PORTS = {
  SGP:  { id:'SGP',  name:'Singapore',         country:'Singapore',    region:'SEA',   lat:1.29,   lon:103.83, berths:55, surplusTEU:2847,  invStatus:'Surplus',  depot:true  },
  VNCMT:{ id:'VNCMT',name:'Ho Chi Minh City',  country:'Vietnam',      region:'SEA',   lat:10.77,  lon:106.70, berths:18, surplusTEU:-1247, invStatus:'Shortage', depot:false },
  PKG:  { id:'PKG',  name:'Port Klang',         country:'Malaysia',     region:'SEA',   lat:3.00,   lon:101.40, berths:32, surplusTEU:1890,  invStatus:'Surplus',  depot:true  },
  SHA:  { id:'SHA',  name:'Shanghai',           country:'China',        region:'NEAC',  lat:31.23,  lon:121.47, berths:120,surplusTEU:5420,  invStatus:'Surplus',  depot:true  },
  CNQIN:{ id:'CNQIN',name:'Qingdao',           country:'China',        region:'NEAC',  lat:36.06,  lon:120.38, berths:60, surplusTEU:3210,  invStatus:'Surplus',  depot:true  },
  KRPUS:{ id:'KRPUS',name:'Busan',             country:'South Korea',  region:'NEAC',  lat:35.10,  lon:129.04, berths:40, surplusTEU:1560,  invStatus:'Surplus',  depot:false },
  JPYOK:{ id:'JPYOK',name:'Yokohama',          country:'Japan',        region:'NEAC',  lat:35.44,  lon:139.64, berths:35, surplusTEU:890,   invStatus:'Surplus',  depot:false },
  INBOM:{ id:'INBOM',name:'Mumbai JNPT',       country:'India',        region:'IOSC',  lat:18.93,  lon:72.93,  berths:21, surplusTEU:-2100, invStatus:'Shortage', depot:true  },
  INAD: { id:'INAD', name:'Adani Port Mundra',  country:'India',        region:'IOSC',  lat:22.84,  lon:69.71,  berths:16, surplusTEU:-890,  invStatus:'Shortage', depot:false },
  BDCTG:{ id:'BDCTG',name:'Chittagong',        country:'Bangladesh',   region:'IOSC',  lat:22.33,  lon:91.83,  berths:12, surplusTEU:-1870, invStatus:'Shortage', depot:false },
  LKCMB:{ id:'LKCMB',name:'Colombo',           country:'Sri Lanka',    region:'IOSC',  lat:6.93,   lon:79.84,  berths:25, surplusTEU:1240,  invStatus:'Surplus',  depot:false },
  RTM:  { id:'RTM',  name:'Rotterdam',          country:'Netherlands',  region:'NWEUR', lat:51.90,  lon:4.48,   berths:95, surplusTEU:6100,  invStatus:'Surplus',  depot:true  },
  DEHAM:{ id:'DEHAM',name:'Hamburg',           country:'Germany',      region:'NWEUR', lat:53.55,  lon:9.98,   berths:65, surplusTEU:2890,  invStatus:'Surplus',  depot:true  },
  GBFXT:{ id:'GBFXT',name:'Felixstowe',        country:'UK',           region:'NWEUR', lat:51.96,  lon:1.35,   berths:28, surplusTEU:1470,  invStatus:'Surplus',  depot:false },
  LAX:  { id:'LAX',  name:'Los Angeles / LB',   country:'USA',          region:'NAWC',  lat:33.74,  lon:-118.27,berths:70, surplusTEU:3850,  invStatus:'Surplus',  depot:true  },
  USNYE:{ id:'USNYE',name:'New York / NJ',     country:'USA',          region:'NAEC',  lat:40.68,  lon:-74.07, berths:30, surplusTEU:2100,  invStatus:'Surplus',  depot:false },
  AEDJB:{ id:'AEDJB',name:'Jebel Ali Dubai',  country:'UAE',          region:'MEA',   lat:24.97,  lon:55.07,  berths:70, surplusTEU:4200,  invStatus:'Surplus',  depot:true  },
  EGPSD:{ id:'EGPSD',name:'Port Said',         country:'Egypt',        region:'MEA',   lat:31.26,  lon:32.30,  berths:18, surplusTEU:-420,  invStatus:'Shortage', depot:false },
  ZACPT:{ id:'ZACPT',name:'Cape Town',         country:'South Africa', region:'SAF',   lat:-33.90, lon:18.42,  berths:12, surplusTEU:340,   invStatus:'Surplus',  depot:false },
  BRSSZ:{ id:'BRSSZ',name:'Santos Brazil',     country:'Brazil',       region:'SAM',   lat:-23.93, lon:-46.30, berths:22, surplusTEU:890,   invStatus:'Surplus',  depot:false },
  LCCHG:{ id:'LCCHG',name:'Laem Chabang',      country:'Thailand',     region:'SEA',   lat:13.08,  lon:100.88, berths:22, surplusTEU:1240,  invStatus:'Surplus',  depot:false },
  MYPKG:{ id:'MYPKG',name:'Penang Port',       country:'Malaysia',     region:'SEA',   lat:5.41,   lon:100.34, berths:10, surplusTEU:640,   invStatus:'Surplus',  depot:false },
  PHMNL:{ id:'PHMNL',name:'Manila',            country:'Philippines',  region:'SEA',   lat:14.59,  lon:120.97, berths:14, surplusTEU:-527,  invStatus:'Shortage', depot:false },
  NLAMF:{ id:'NLAMF',name:'Amsterdam',         country:'Netherlands',  region:'NWEUR', lat:52.38,  lon:4.90,   berths:20, surplusTEU:507,   invStatus:'Surplus',  depot:true  },
  ESMAD:{ id:'ESMAD',name:'Algeciras',         country:'Spain',        region:'MED',   lat:36.13,  lon:-5.45,  berths:25, surplusTEU:1810,  invStatus:'Surplus',  depot:false },
}

// ─── VESSELS ─────────────────────────────────────────────────────────────────
// Sources: MarineTraffic AIS · Vessel Finder · Lloyd's Register
export const FLEET_VESSELS = [
  { id:'MSC-AURORA',   name:'MSC AURORA',      type:'Neo-Panamax',  capacityTEU:14_000, cargoPct:78, emptyTEU:3080, fromPort:'SHA',   toPort:'VNCMT', status:'En Route',  eta:'Apr 19', speed:18.2, heading:'SE', lat:20.5,  lon:115.2 },
  { id:'EVER-GOLDEN',  name:'EVER GOLDEN',     type:'ULCV',         capacityTEU:20_000, cargoPct:82, emptyTEU:3600, fromPort:'VNCMT', toPort:'RTM',   status:'Loading',   eta:'Apr 19', speed:0,    heading:'W',  lat:10.77, lon:106.70 },
  { id:'MAERSK-ELENA', name:'MAERSK ELENA',    type:'Triple-E',     capacityTEU:18_000, cargoPct:91, emptyTEU:1620, fromPort:'RTM',   toPort:'SHA',   status:'Loading',   eta:'Apr 22', speed:0,    heading:'E',  lat:51.9,  lon:4.48  },
  { id:'CMA-LIBERTY',  name:'CMA CGM LIBERTY', type:'Panamax',      capacityTEU:9_000,  cargoPct:65, emptyTEU:3150, fromPort:'SGP',   toPort:'INBOM', status:'En Route',  eta:'Apr 19', speed:17.0, heading:'W',  lat:6.5,   lon:82.3  },
  { id:'OOCL-TIANJIN', name:'OOCL TIANJIN',    type:'New Panamax',  capacityTEU:12_000, cargoPct:74, emptyTEU:3120, fromPort:'KRPUS', toPort:'LAX',   status:'En Route',  eta:'Apr 18', speed:20.1, heading:'E',  lat:37.0,  lon:168.4 },
  { id:'HMM-DANUBE',   name:'HMM DANUBE',      type:'Feeder',       capacityTEU:4_800,  cargoPct:55, emptyTEU:2160, fromPort:'LCCHG', toPort:'SGP',   status:'Anchored',  eta:'Apr 20', speed:0,    heading:'S',  lat:10.5,  lon:104.1 },
  { id:'ANE-MAERSK',   name:'ANE MAERSK',      type:'Feeder',       capacityTEU:6_200,  cargoPct:68, emptyTEU:1984, fromPort:'SGP',   toPort:'PHMNL', status:'En Route',  eta:'Apr 19', speed:16.8, heading:'NE', lat:8.2,   lon:114.3 },
  { id:'MARIE-MAERSK', name:'MARIE MAERSK',    type:'Panamax',      capacityTEU:10_500, cargoPct:80, emptyTEU:2100, fromPort:'SGP',   toPort:'PHMNL', status:'Anchored',  eta:'Apr 18', speed:0,    heading:'N',  lat:1.3,   lon:103.9 },
]

// ─── DEMAND SCENARIOS ────────────────────────────────────────────────────────
export const DEMAND_SCENARIOS = {
  vietnam_surge: {
    id:'vietnam_surge', key:'vietnam_surge',
    name:'Vietnam Manufacturing Surge',
    portId:'VNCMT', portName:'Ho Chi Minh City',
    winningDepotId:'VNCMT',            // containers are pre-staged AT HCMC
    region:'Vietnam – HCMC',
    teuRequired:847,
    containerType:'40ft Dry',
    destination:'Ho Chi Minh City',
    requiredBy:'April 21',
    slaWindow:'72 hours',
    urgency:'CRITICAL',
    confidence:94,
    // ↓ Description uses range — never reveals exact booking TEUs
    description:'ATLAS demand signal detected — Vietnam PMI surge + Vinamih SAP PO activity indicates 800–900 TEU demand window opening 72 hours ahead',
    customer:'Vinamih Vietnam',
    sapRef:'VNM-2026-0047',
    signals:[
      { source:'Vietnam PMI Index',    signal:'Manufacturing PMI 54.2 — 6-month high. Export orders +18% MoM.',                 weight:0.31, icon:'📊' },
      { source:'Vinamih SAP Orders',   signal:'3 new POs in SAP: 280 TEU electronics, 190 TEU garments, 377 TEU mixed cargo.',   weight:0.28, icon:'📦' },
      { source:'Weather / ECMWF',      signal:'Typhoon Malakas track shifted north — 14-day HCMC port window clear.',            weight:0.19, icon:'🌤' },
      { source:'AIS Vessel Feed',      signal:'MSC AURORA (3,080 empty TEU) Shanghai → HCMC, ETA Apr 19. Capacity confirmed.',   weight:0.14, icon:'🛸' },
      { source:'Historical Patterns',  signal:'Apr–May peak for Vietnam garment & electronics exports. 2024/25 YoY +22%.',       weight:0.08, icon:'📈' },
    ],
    // Demand prediction — always a range, not exact
    prediction:{ demand:'800–900 TEUs', region:'Vietnam – HCMC', window:'April 18–21', confidence:94 },
    candidateVessels:['EVER-GOLDEN','MSC-AURORA','HMM-DANUBE'],
    penaltyPerDay:18_500,
    potentialSavings:286_400,
    // ── Repositioning recommendation table ──────────────────────────────────
    // Row 1: demand port itself (pre-staged, distance 0) — LOWEST cost
    // Row 2: nearest viable surplus port — moderate cost
    // Row 3: conflicted port — rejected
    repositionOptions:[
      {
        rank:1, decision:'Pre-positioned', depot:'Ho Chi Minh City', depotId:'VNCMT',
        distance:'0 km (pre-staged)', costTEU:0, listedSLA:'99%', realSLA:'99%',
        available:890, conflictVessels:[], method:'ATLAS pre-staged via EVER GOLDEN',
        highlight:true, savings:215, co2Saving:'35%', transitDays:0,
        reasoning:'ATLAS detected the demand signal 72 hours early and pre-positioned 847 TEUs at Cai Mep Terminal, HCMC, before any booking existed. Containers shipped Port Klang → HCMC via EVER GOLDEN co-load window (Apr 15). Already staged on-site. Zero additional transit. Booking confirmed in 4.2 seconds.',
        vessel:'EVER-GOLDEN',
      },
      {
        rank:2, decision:'Available', depot:'Port Klang', depotId:'PKG',
        distance:'1,640 km', costTEU:215, listedSLA:'89%', realSLA:'91%',
        available:890, conflictVessels:[], method:'EVER GOLDEN direct',
        highlight:false, savings:80, co2Saving:'18%', transitDays:2.8,
        reasoning:'890 TEUs available at Port Klang, Malaysia. EVER GOLDEN could depart Apr 18 06:00 → HCMC within 72-hour SLA. Used as the pre-staging source — containers already moved to HCMC 72 hours ago.',
        vessel:'EVER-GOLDEN',
      },
      {
        rank:3, decision:'All conflict', depot:'Singapore', depotId:'SGP',
        distance:'1,240 km', costTEU:180, listedSLA:'97%', realSLA:'23%',
        available:2847, conflictVessels:['MSC-AURORA'], method:'Direct',
        highlight:false, savings:0, co2Saving:'18%', transitDays:1.9,
        rejected:true,
        reasoning:'Singapore Tanjong Pagar lists 2,100 TEU available. BUT AIS data confirms MSC AURORA arrives Apr 19 with 1,547 TEU offload destined for Tanjong Pagar — post-offload net available: 263 TEU — insufficient for 847 TEU requirement. Real SLA probability: 23%. This data source was NOT in any spreadsheet.',
        vessel:'MSC-AURORA',
      },
    ],
    streetTurn:{
      oldWay:{
        label:'Empty Repositioning',
        costPerTEU:210, containers:507,
        totalCost:-106_470, revenueGenerated:0,
      },
      atlasWay:{
        label:'Co-loaded with Cargo',
        route:'Port Klang → HCMC (EVER GOLDEN co-load)',
        shipment:'Philips Electronics — 507 TEUs outbound to HCMC',
        vessel:'EVER GOLDEN',
        departsDate:'Apr 15',
        duration:'3 days',
        freightRate:355,
        containers:507, costPerTEU:355,
        totalRevenue:179_985,
        netSaving:286_455,
      },
    },
    streetTurnMatches:[
      { from:'HCMC – Vinamih unload',    to:'Samsung Electronics outbound',  teus:180, cost:0 },
      { from:'HCMC – Nestlé unload',     to:'Unilever outbound Apr 18',       teus:95,  cost:0 },
      { from:'HCMC – P&G unload',        to:'Vinamih Apr 19 partial fill',    teus:65,  cost:0 },
    ],
    streetTurnTotalTeus:340,
    remainingTeus:507,
    ownFleet:{
      costPerTEU:0,
      depot:'HCMC – Cai Mep Terminal (ATLAS pre-staged)',
      schedule:'Already on-site — staged Apr 15 via EVER GOLDEN co-load',
    },
    emergencyLease:{
      costPerTEU:340,
      source:'Local leasing company – Ho Chi Minh City',
      note:'Available immediately · Premium surge rate',
    },
    fleetSavingPerBooking:172_380,
    // ── SAP execution steps — HCMC specific ──
    sapSteps:[
      { id:1, text:'SAP TM order TM-2026-04729 created',       sub:'HCMC Cai Mep Terminal — 847 TEU · Pre-staged allocation released',        delay:400  },
      { id:2, text:'Vessel booking confirmed — EVER GOLDEN',   sub:'Departs HCMC Apr 19 06:00 · Full slot secured · AIS updated',             delay:900  },
      { id:3, text:'Cai Mep Terminal operations notified',      sub:'Container gate-in scheduled Apr 19 04:00 · 847 TEU handed over',          delay:1500 },
      { id:4, text:'Vinamih Vietnam — ETA confirmed',           sub:'Customer ETA notification sent · Delivery Apr 20 confirmed via SAP',      delay:2200 },
      { id:5, text:'EU AI Act audit trail logged',              sub:'Full decision transparency recorded · 4.2s decision time archived',       delay:2900 },
    ],
  },

  philippines: {
    id:'philippines', key:'philippines',
    name:'Philippines Inland Distribution Surge',
    portId:'PHMNL', portName:'Manila',
    winningDepotId:'PHMNL',
    region:'Philippines – Manila',
    teuRequired:847,
    containerType:'40ft Dry',
    destination:'Manila',
    requiredBy:'April 20',
    slaWindow:'72 hours',
    urgency:'CRITICAL',
    confidence:91,
    description:'ATLAS demand signal detected — Philippines PMI spike + Inland Team order pattern indicates 800–870 TEU demand window opening 72 hours ahead',
    customer:'Inland Team Philippines',
    sapRef:'PHL-2026-0092',
    signals:[
      { source:'Philippines PMI',      signal:'Philippines Manufacturing PMI 55.3 — multi-year high. Export orders +21% MoM.',               weight:0.29, icon:'📊' },
      { source:'SAP / Inland Orders',  signal:'3 urgent POs from Inland Team: 320 TEU consumer goods, 280 TEU electronics, 247 TEU mixed.',  weight:0.31, icon:'📦' },
      { source:'AIS Vessel Feed',      signal:'Ane-Maersk (1,984 empty TEU) en route SGP → PHMNL, ETA Apr 19. Pre-position confirmed.',      weight:0.22, icon:'🛸' },
      { source:'Port Congestion',      signal:'Manila South Harbour berth availability restored to 88% — clear window Apr 18–25.',            weight:0.10, icon:'🏗' },
      { source:'Historical Patterns',  signal:'Apr–Jun peak for Philippines consumer goods & electronics. 2024/25 YoY +27%.',                weight:0.08, icon:'📈' },
    ],
    prediction:{ demand:'800–870 TEUs', region:'Philippines – Manila', window:'April 18–21', confidence:91 },
    candidateVessels:['ANE-MAERSK','MARIE-MAERSK'],
    penaltyPerDay:16_200,
    potentialSavings:256_035,
    repositionOptions:[
      {
        rank:1, decision:'Pre-positioned', depot:'Manila', depotId:'PHMNL',
        distance:'0 km (pre-staged)', costTEU:0, listedSLA:'99%', realSLA:'99%',
        available:830, conflictVessels:[], method:'ATLAS pre-staged via Ane-Maersk',
        highlight:true, savings:195, co2Saving:'32%', transitDays:0,
        reasoning:'ATLAS pre-positioned 830 TEUs at Manila South Harbour 72 hours before this booking. Detected Philippines PMI spike + Inland Team SAP order patterns 3 days early. Ane-Maersk delivered containers Apr 15. On-site and ready. Additional 17 TEU sourced from Marie-Maersk berth allocation.',
        vessel:'ANE-MAERSK',
      },
      {
        rank:2, decision:'Available', depot:'Laem Chabang', depotId:'LCCHG',
        distance:'2,200 km', costTEU:225, listedSLA:'84%', realSLA:'84%',
        available:1240, conflictVessels:[], method:'Via HMM Danube feeder',
        highlight:false, savings:60, co2Saving:'14%', transitDays:3.5,
        reasoning:'1,240 TEUs available at Laem Chabang. Viable backup via HMM Danube feeder with 3.5-day transit — within 72-hour SLA but significantly higher cost.',
        vessel:'HMM-DANUBE',
      },
      {
        rank:3, decision:'All conflict', depot:'Singapore', depotId:'SGP',
        distance:'2,380 km', costTEU:180, listedSLA:'92%', realSLA:'31%',
        available:2847, conflictVessels:['MARIE-MAERSK','MSC-AURORA'], method:'Direct',
        highlight:false, savings:0, co2Saving:'18%', transitDays:3.2,
        rejected:true,
        reasoning:'Singapore lists 2,847 TEU but AIS confirms MSC AURORA arriving Apr 19 with 1,547 TEU offload PLUS Marie-Maersk block-booking consuming 900 TEU slots. Net available post-conflicts: ~400 TEU — insufficient. Real SLA: 31%.',
        vessel:'MARIE-MAERSK',
      },
    ],
    streetTurn:{
      oldWay:{ label:'Empty Repositioning', costPerTEU:195, containers:507, totalCost:-98_865, revenueGenerated:0 },
      atlasWay:{
        label:'Co-loaded with Cargo',
        route:'Singapore → Manila (Ane-Maersk co-load)',
        shipment:'Ayala Fashion Group — 507 TEUs outbound consumer goods',
        vessel:'ANE-MAERSK',
        departsDate:'Apr 15',
        duration:'3 days',
        freightRate:310,
        containers:507, costPerTEU:310,
        totalRevenue:157_170,
        netSaving:256_035,
      },
    },
    streetTurnMatches:[
      { from:'Manila – ICTSI unload',    to:'Ayala Fashion Group outbound',   teus:210, cost:0 },
      { from:'Manila – Cosco unload',    to:'SM Retail outbound Apr 18',       teus:120, cost:0 },
      { from:'Singapore – DHL unload',   to:'Inland Team Apr 19 partial',      teus:90,  cost:0 },
    ],
    streetTurnTotalTeus:420,
    remainingTeus:427,
    ownFleet:{
      costPerTEU:0,
      depot:'Manila – South Harbour (ATLAS pre-staged via Ane-Maersk)',
      schedule:'Already on-site — staged Apr 15 via Ane-Maersk co-load',
    },
    emergencyLease:{
      costPerTEU:315,
      source:'Pan Asia Leasing Co. — Manila',
      note:'Available immediately · Surge pricing',
    },
    fleetSavingPerBooking:134_505,
    sapSteps:[
      { id:1, text:'SAP TM order PHL-2026-0092 created',       sub:'Manila South Harbour — 847 TEU · Pre-staged allocation released',        delay:400  },
      { id:2, text:'Vessel slot confirmed — ANE MAERSK',       sub:'Departs Manila Apr 19 08:00 · Full slot secured',                        delay:900  },
      { id:3, text:'Manila South Harbour notified',             sub:'Container gate-in scheduled Apr 19 06:00 · 847 TEU allocated',           delay:1500 },
      { id:4, text:'Inland Team Philippines — ETA confirmed',  sub:'Customer notification sent · Delivery Apr 20 confirmed',                 delay:2200 },
      { id:5, text:'EU AI Act audit trail logged',              sub:'Full decision transparency archived · 4.2s decision time',               delay:2900 },
    ],
  },

  bangladesh_crisis: {
    id:'bangladesh_crisis', key:'bangladesh_crisis',
    name:'Bangladesh Garment Export Crisis',
    portId:'BDCTG', portName:'Chittagong',
    winningDepotId:'BDCTG',
    region:'Bangladesh – Chittagong',
    teuRequired:620,
    containerType:'20ft Dry',
    destination:'Chittagong',
    requiredBy:'April 22',
    slaWindow:'96 hours',
    urgency:'HIGH',
    confidence:87,
    description:'ATLAS demand signal detected — Bangladesh RMG PMI 56.8 + DBL Group purchase orders indicate 580–650 TEU container shortage risk ahead of peak season',
    customer:'DBL Group',
    sapRef:'BGD-2026-0089',
    signals:[
      { source:'Bangladesh PMI',      signal:'RMG sector PMI 56.8 — 8-year high. Export orders +24% MoM (H&M, Primark sourcing shift).', weight:0.32, icon:'📊' },
      { source:'SAP / DBL Group',     signal:'DBL Group: 3 confirmed POs — 210 TEU knitwear, 180 TEU denim, 230 TEU mixed garments.',    weight:0.27, icon:'📦' },
      { source:'AIS Vessel Feed',     signal:'No surplus vessel inbound to Chittagong in 14-day window. CMA CGM LIBERTY re-routing.',    weight:0.22, icon:'🛸' },
      { source:'Competitor Intel',    signal:'MSC & Hapag-Lloyd both reporting 0 TEU availability at CTG. Market-wide squeeze.',          weight:0.12, icon:'🌍' },
      { source:'Historical Patterns', signal:'Apr–Jun RMG peak season. Bangladesh textile exports +31% YoY 2024/25.',                   weight:0.07, icon:'📈' },
    ],
    prediction:{ demand:'580–650 TEUs', region:'Bangladesh – Chittagong', window:'April 18–22', confidence:87 },
    candidateVessels:['CMA-LIBERTY'],
    penaltyPerDay:12_000,
    potentialSavings:197_400,
    repositionOptions:[
      {
        rank:1, decision:'Pre-positioned', depot:'Chittagong', depotId:'BDCTG',
        distance:'0 km (pre-staged)', costTEU:0, listedSLA:'95%', realSLA:'92%',
        available:620, conflictVessels:[], method:'ATLAS pre-staged via CMA CGM LIBERTY',
        highlight:true, savings:185, co2Saving:'28%', transitDays:0,
        reasoning:'ATLAS pre-positioned 620 TEUs at Chittagong container terminal 48 hours before booking, routed via CMA CGM LIBERTY Colombo → Chittagong leg. Bangladesh PMI + DBL Group PO signals triggered early action. Containers on-site. No transit penalty.',
        vessel:'CMA-LIBERTY',
      },
      {
        rank:2, decision:'Available', depot:'Colombo', depotId:'LKCMB',
        distance:'2,100 km', costTEU:185, listedSLA:'89%', realSLA:'87%',
        available:1240, conflictVessels:[], method:'CMA CGM LIBERTY direct',
        highlight:false, savings:98, co2Saving:'21%', transitDays:3.2,
        reasoning:'1,240 TEUs at Colombo, Sri Lanka. CMA CGM LIBERTY available for Colombo → Chittagong run, ETA Apr 21. Within 96-hour SLA window. Backup if pre-staged TEUs were insufficient.',
        vessel:'CMA-LIBERTY',
      },
      {
        rank:3, decision:'All conflict', depot:'Mumbai JNPT', depotId:'INBOM',
        distance:'2,800 km', costTEU:210, listedSLA:'72%', realSLA:'12%',
        available:0, conflictVessels:['MULTIPLE'], method:'N/A',
        highlight:false, savings:0, co2Saving:'0%', transitDays:4.1,
        rejected:true,
        reasoning:'Mumbai JNPT (INBOM) is itself in a 2,100 TEU shortage. Cannot source from a port in deficit. Cross-referencing SAP confirms all available slots block-booked. Zero net available for external repositioning.',
        vessel:null,
      },
    ],
    streetTurn:{
      oldWay:{ label:'Empty Repositioning', costPerTEU:185, containers:420, totalCost:-77_700, revenueGenerated:0 },
      atlasWay:{
        label:'Co-loaded with Cargo',
        route:'Colombo → Chittagong (CMA CGM LIBERTY co-load)',
        shipment:'BGMEA Export Batch — 420 TEU garments outbound',
        vessel:'CMA CGM LIBERTY',
        departsDate:'Apr 18',
        duration:'2.5 days',
        freightRate:285,
        containers:420, costPerTEU:285,
        totalRevenue:119_700,
        netSaving:197_400,
      },
    },
    streetTurnMatches:[
      { from:'CTG – DBL Group unload',   to:'H&M Bangladesh outbound',        teus:150, cost:0 },
      { from:'CTG – Square Textiles',    to:'Primark export Apr 21',           teus:85,  cost:0 },
      { from:'Colombo – local unload',   to:'DBL Group Apr 22 fill',           teus:55,  cost:0 },
    ],
    streetTurnTotalTeus:290,
    remainingTeus:330,
    ownFleet:{
      costPerTEU:0,
      depot:'Chittagong – CTG Terminal (ATLAS pre-staged via CMA CGM LIBERTY)',
      schedule:'Already on-site — staged Apr 18 via CMA CGM LIBERTY co-load',
    },
    emergencyLease:{
      costPerTEU:320,
      source:'Bay of Bengal Leasing – Chittagong',
      note:'Available Apr 19 · Emergency premium rate',
    },
    fleetSavingPerBooking:105_600,
    sapSteps:[
      { id:1, text:'SAP TM order BGD-2026-0089 created',       sub:'Chittagong Terminal — 620 TEU · Pre-staged allocation released',          delay:400  },
      { id:2, text:'Vessel booking confirmed — CMA CGM LIBERTY',sub:'Departs CTG Apr 22 06:00 · Full slot secured',                          delay:900  },
      { id:3, text:'Chittagong Terminal (CTG) notified',         sub:'Container gate-in confirmed · 620 TEU DBL Group allocated',             delay:1500 },
      { id:4, text:'DBL Group Bangladesh — ETA confirmed',       sub:'Customer SAP notification sent · Export window Apr 22 secured',         delay:2200 },
      { id:5, text:'EU AI Act audit trail logged',               sub:'Full decision transparency recorded · 4.2s decision time',              delay:2900 },
    ],
  },

  india_automotive: {
    id:'india_automotive', key:'india_automotive',
    name:'India Automotive Export Surge',
    portId:'INBOM', portName:'Mumbai JNPT',
    winningDepotId:'INBOM',
    region:'India – Mumbai JNPT',
    teuRequired:720,
    containerType:'40ft Dry',
    destination:'Mumbai JNPT',
    requiredBy:'April 23',
    slaWindow:'120 hours',
    urgency:'HIGH',
    confidence:88,
    description:'ATLAS demand signal detected — India PMI 58.1 + Tata Motors SAP orders indicate 680–750 TEU auto-component export window opening ahead of UK/EU delivery',
    customer:'Tata Motors Export',
    sapRef:'IND-2026-0134',
    signals:[
      { source:'India PMI',          signal:'India Manufacturing PMI 58.1 — 11-year high. Auto exports +32% YoY, FY2026 record.',            weight:0.30, icon:'📊' },
      { source:'Tata Motors SAP',    signal:'4 confirmed export POs: 720 TEU auto parts & CKD kits — UK/Germany delivery Apr 30.',          weight:0.26, icon:'📦' },
      { source:'AIS Vessel Feed',    signal:'No inbound surplus vessel at JNPT in 10-day window. Colombo pre-positioning triggered.',        weight:0.22, icon:'🛸' },
      { source:'Trade Intelligence', signal:'India-UK FTA implementation driving +28% surge in UK-bound auto shipments Q1 2026.',            weight:0.14, icon:'🌍' },
      { source:'Historical Patterns',signal:'Apr–May auto-export peak aligned with UK/EU fiscal year inventory restocking cycle.',           weight:0.08, icon:'📈' },
    ],
    prediction:{ demand:'680–750 TEUs', region:'India – Mumbai JNPT', window:'April 19–23', confidence:88 },
    candidateVessels:['CMA-LIBERTY','MAERSK-ELENA'],
    penaltyPerDay:15_000,
    potentialSavings:225_600,
    repositionOptions:[
      {
        rank:1, decision:'Pre-positioned', depot:'Mumbai JNPT', depotId:'INBOM',
        distance:'0 km (pre-staged)', costTEU:0, listedSLA:'97%', realSLA:'95%',
        available:720, conflictVessels:[], method:'ATLAS pre-staged via CMA CGM LIBERTY',
        highlight:true, savings:175, co2Saving:'30%', transitDays:0,
        reasoning:'ATLAS detected India PMI + Tata Motors SAP signals and pre-positioned 720 TEUs at JNPT Nhava Sheva terminal 60 hours ahead. CMA CGM LIBERTY repositioned from Colombo Apr 18. Containers on-site and allocated to TM-2026-0134. Zero transit delay.',
        vessel:'CMA-LIBERTY',
      },
      {
        rank:2, decision:'Available', depot:'Colombo', depotId:'LKCMB',
        distance:'1,540 km', costTEU:175, listedSLA:'91%', realSLA:'91%',
        available:1240, conflictVessels:[], method:'CMA CGM LIBERTY',
        highlight:false, savings:112, co2Saving:'24%', transitDays:2.1,
        reasoning:'1,240 TEU at Colombo, Sri Lanka. CMA CGM LIBERTY departs Apr 20 → JNPT ETA Apr 22. Backup source used for pre-positioning — containers already moved to JNPT 60 hours ago.',
        vessel:'CMA-LIBERTY',
      },
      {
        rank:3, decision:'All conflict', depot:'Adani Mundra', depotId:'INAD',
        distance:'480 km', costTEU:95, listedSLA:'66%', realSLA:'8%',
        available:0, conflictVessels:['MULTIPLE'], method:'N/A',
        highlight:false, savings:0, co2Saving:'0%', transitDays:1.2,
        rejected:true,
        reasoning:'Adani Mundra (INAD) shows -890 TEU shortage in SAP. Port is in deficit — cannot source from a port that itself has a shortage. Cross-referencing SAP confirms all vessel block-bookings have consumed available slots.',
        vessel:null,
      },
    ],
    streetTurn:{
      oldWay:{ label:'Empty Repositioning', costPerTEU:175, containers:480, totalCost:-84_000, revenueGenerated:0 },
      atlasWay:{
        label:'Co-loaded with Cargo',
        route:'Colombo → Mumbai JNPT (CMA CGM LIBERTY co-load)',
        shipment:'Sri Lanka Tea Export Board — 480 TEU outbound',
        vessel:'CMA CGM LIBERTY',
        departsDate:'Apr 18',
        duration:'2.1 days',
        freightRate:295,
        containers:480, costPerTEU:295,
        totalRevenue:141_600,
        netSaving:225_600,
      },
    },
    streetTurnMatches:[
      { from:'JNPT – Tata Motors unload',  to:'Mahindra export outbound',       teus:160, cost:0 },
      { from:'JNPT – L&T Engineering',     to:'Auto components Apr 22',          teus:95,  cost:0 },
      { from:'Colombo – local unload',     to:'Tata Motors Apr 23 fill',         teus:65,  cost:0 },
    ],
    streetTurnTotalTeus:320,
    remainingTeus:400,
    ownFleet:{
      costPerTEU:0,
      depot:'Mumbai JNPT – Nhava Sheva (ATLAS pre-staged via CMA CGM LIBERTY)',
      schedule:'Already on-site — staged Apr 18 via Colombo co-load',
    },
    emergencyLease:{
      costPerTEU:295,
      source:'Mumbai Port Leasing Ltd. – JNPT',
      note:'Available immediately · Spot rate',
    },
    fleetSavingPerBooking:118_000,
    sapSteps:[
      { id:1, text:'SAP TM order IND-2026-0134 created',        sub:'Mumbai JNPT Nhava Sheva — 720 TEU · Pre-staged TEU allocation released', delay:400  },
      { id:2, text:'Vessel slot confirmed — CMA CGM LIBERTY',   sub:'Departs JNPT Apr 23 14:00 · UK/EU-bound · Slot locked',                  delay:900  },
      { id:3, text:'JNPT Nhava Sheva operations notified',       sub:'Container gate-in confirmed · Tata Motors TM-2026-0134 allocated',       delay:1500 },
      { id:4, text:'Tata Motors Export — ETA UK confirmed',      sub:'Customer notification sent · AP Moller-Maersk ETA Apr 30',              delay:2200 },
      { id:5, text:'EU AI Act audit trail logged',               sub:'Full decision transparency recorded · 4.2s decision time',              delay:2900 },
    ],
  },

  korea_electronics: {
    id:'korea_electronics', key:'korea_electronics',
    name:'Korea Electronics US Export Surge',
    portId:'KRPUS', portName:'Busan',
    winningDepotId:'KRPUS',
    region:'South Korea – Busan',
    teuRequired:580,
    containerType:'40ft Dry',
    destination:'Los Angeles / LB',
    requiredBy:'April 25',
    slaWindow:'144 hours',
    urgency:'MEDIUM',
    confidence:82,
    description:'ATLAS demand signal detected — Korea semiconductor exports +41% YoY + Samsung PO data indicate 540–600 TEU co-load window on Busan → LA corridor',
    customer:'Samsung Electronics Co.',
    sapRef:'KOR-2026-0211',
    signals:[
      { source:'Korea Export Data',    signal:'Korea semiconductor exports +41% YoY — DRAM & NAND Flash driven by US AI datacenter demand.', weight:0.34, icon:'📊' },
      { source:'Samsung SAP Orders',   signal:'Samsung: 580 TEU 40ft dry confirmed — chips + display panels, LA delivery May 2.',            weight:0.28, icon:'📦' },
      { source:'AIS Vessel Feed',      signal:'OOCL TIANJIN departs Busan Apr 18, 3,120 empty TEU — perfect co-load window.',               weight:0.20, icon:'🛸' },
      { source:'Market Intelligence',  signal:'US AI infrastructure capex +62% Q1 2026. Nvidia/AMD supply chain pulling forward DRAM.',     weight:0.12, icon:'🌍' },
      { source:'Historical Patterns',  signal:'Q2 Korea electronics export peak aligns with US fiscal hardware procurement cycles.',         weight:0.06, icon:'📈' },
    ],
    prediction:{ demand:'540–600 TEUs', region:'South Korea – Busan', window:'April 18–21', confidence:82 },
    candidateVessels:['OOCL-TIANJIN'],
    penaltyPerDay:11_500,
    potentialSavings:201_700,
    repositionOptions:[
      {
        rank:1, decision:'Pre-positioned', depot:'Busan', depotId:'KRPUS',
        distance:'0 km (pre-staged)', costTEU:0, listedSLA:'97%', realSLA:'97%',
        available:1560, conflictVessels:[], method:'ATLAS pre-staged · OOCL TIANJIN',
        highlight:true, savings:185, co2Saving:'28%', transitDays:0,
        reasoning:'ATLAS pre-allocated 580 TEU to Samsung shipment 5 days ago based on AI datacenter procurement signals + OOCL TIANJIN departure window. 1,560 TEU already staged at Busan Gamman Terminal. Zero additional repositioning cost — containers are at origin.',
        vessel:'OOCL-TIANJIN',
      },
      {
        rank:2, decision:'Available', depot:'Yokohama', depotId:'JPYOK',
        distance:'940 km', costTEU:165, listedSLA:'88%', realSLA:'85%',
        available:890, conflictVessels:[], method:'Feeder to Busan',
        highlight:false, savings:90, co2Saving:'18%', transitDays:1.8,
        reasoning:'890 TEU at Yokohama. Feeder connection to Busan adds 1.8 days but comfortably within 144-hour SLA. Backup option.',
        vessel:null,
      },
      {
        rank:3, decision:'All conflict', depot:'Shanghai', depotId:'SHA',
        distance:'900 km', costTEU:140, listedSLA:'95%', realSLA:'28%',
        available:5420, conflictVessels:['MAERSK-ELENA','EVER-GOLDEN'], method:'Direct',
        highlight:false, savings:0, co2Saving:'0%', transitDays:2.1,
        rejected:true,
        reasoning:'Shanghai lists 5,420 TEU but AIS shows MAERSK ELENA loading for RTM and EVER GOLDEN has 4,200 TEU slot-booked by three carriers. Net available after block allocations: ~380 TEU — insufficient for 580 TEU. Real SLA: 28%.',
        vessel:'MAERSK-ELENA',
      },
    ],
    streetTurn:{
      oldWay:{ label:'Single Carrier Empty Return', costPerTEU:145, containers:280, totalCost:-40_600, revenueGenerated:0 },
      atlasWay:{
        label:'Co-loaded with LG Electronics',
        route:'Busan → Los Angeles (OOCL TIANJIN co-load)',
        shipment:'LG Electronics — 280 TEU OLED panels consolidated',
        vessel:'OOCL TIANJIN',
        departsDate:'Apr 18',
        duration:'14 days',
        freightRate:575,
        containers:280, costPerTEU:575,
        totalRevenue:161_000,
        netSaving:201_600,
      },
    },
    streetTurnMatches:[
      { from:'Busan – Samsung unload',   to:'LG Electronics LA outbound',     teus:180, cost:0 },
      { from:'Busan – Hyundai unload',   to:'SK Hynix export Apr 18',          teus:95,  cost:0 },
      { from:'Yokohama – Sony unload',   to:'Samsung Apr 19 fill',             teus:25,  cost:0 },
    ],
    streetTurnTotalTeus:300,
    remainingTeus:280,
    ownFleet:{
      costPerTEU:0,
      depot:'Busan – Gamman Terminal (ATLAS pre-staged · OOCL TIANJIN)',
      schedule:'Already on-site — pre-allocated 5 days ago via ATLAS signal',
    },
    emergencyLease:{
      costPerTEU:265,
      source:'Korea Container Leasing Corp. – Busan',
      note:'Available Apr 18 · Peak season rate',
    },
    fleetSavingPerBooking:74_200,
    sapSteps:[
      { id:1, text:'SAP TM order KOR-2026-0211 created',        sub:'Busan Gamman Terminal — 580 TEU · Pre-staged allocation released',       delay:400  },
      { id:2, text:'Vessel slot confirmed — OOCL TIANJIN',      sub:'Departs Busan Apr 18 22:00 → LA/LB ETA May 2 · Slot locked',            delay:900  },
      { id:3, text:'Busan Gamman Terminal notified',             sub:'Container gate-in Apr 18 18:00 · Samsung Electronics allocated',        delay:1500 },
      { id:4, text:'Samsung Electronics — ETA LA confirmed',    sub:'Customer notification sent · Delivery May 2 confirmed',                 delay:2200 },
      { id:5, text:'EU AI Act audit trail logged',              sub:'Full decision transparency recorded · 4.2s decision time',              delay:2900 },
    ],
  },
}

// ─── GLOBAL FALLBACKS ─────────────────────────────────────────────────────────
export const REPOSITION_OPTIONS = DEMAND_SCENARIOS.vietnam_surge.repositionOptions
export const STREET_TURN        = DEMAND_SCENARIOS.vietnam_surge.streetTurn

// ─── SAP EXECUTION (global fallback — each scenario overrides via sapSteps) ───
export const SAP_EXECUTION_STEPS = DEMAND_SCENARIOS.vietnam_surge.sapSteps

// ─── ATLAS PREDICTION vs ACTUAL ──────────────────────────────────────────────
export const ATLAS_PREDICTION = {
  madeAt:         'April 15, 03:14 AM',
  madeLabel:      '3 days ago — before any booking request existed',
  expectedDemand: '800–900 TEUs',
  region:         'Vietnam – HCMC',
  window:         'April 18–21',
  confidence:     94,
  actionTaken:    'Pre-positioned at HCMC Cai Mep Terminal',
}

export const ACTUAL_BOOKING = {
  receivedAt:           'April 18, 06:42 AM',
  actualDemand:         847,
  region:               'Vietnam – HCMC',
  window:               'April 18 — 22 hours SLA',
  decisionTime:         '4.2 seconds',
  containersAvailable:  '890 TEUs — already staged at HCMC',
}

export const PERFORMANCE_METRICS = {
  predictionAccuracy:      94,
  teusStaged:              340,
  revenueFromCargo:        188_000,
  revenueFromSecondSlot:   58_000,
  crisisResolvedSeconds:   4.2,
  costAccumulated:         12_851,
  vsManualTimeline:        { manual:'72 hours', ai:'4.2 seconds' },
}

// ─── PERFORMANCE FORECAST ────────────────────────────────────────────────────
export const PERFORMANCE_FORECAST = [
  { year:1, month:'Q1',  cumulative:89,   monthly:89  },
  { year:1, month:'Q2',  cumulative:188,  monthly:99  },
  { year:1, month:'Q3',  cumulative:320,  monthly:132 },
  { year:1, month:'Q4',  cumulative:535,  monthly:215 },
  { year:2, month:'Q5',  cumulative:680,  monthly:145 },
  { year:2, month:'Q6',  cumulative:850,  monthly:170 },
  { year:2, month:'Q7',  cumulative:1050, monthly:200 },
  { year:2, month:'Q8',  cumulative:1280, monthly:230 },
  { year:3, month:'Q9',  cumulative:1520, monthly:240 },
  { year:3, month:'Q10', cumulative:1760, monthly:240 },
  { year:3, month:'Q11', cumulative:2000, monthly:240 },
  { year:3, month:'Q12', cumulative:2240, monthly:240 },
]

export const YEAR_FORECAST = [
  { year:'Year 1', value:535,  label:'$535M',  color:'#00B4D8' },
  { year:'Year 2', value:1280, label:'$1.28B', color:'#0077B6' },
  { year:'Year 3', value:2240, label:'$2.24B', color:'#005F8E' },
]

// ─── CONTAINER INVENTORY ─────────────────────────────────────────────────────
export const CONTAINER_INVENTORY = [
  { type:'40ft Dry',    fill:58, total:412500, available:239250, color:'#0077B6' },
  { type:'20ft Dry',    fill:72, total:380000, available:273600, color:'#00B4D8' },
  { type:'40ft Reefer', fill:41, total:85000,  available:34850,  color:'#42B4E6' },
  { type:'In Transit',  fill:65, total:180000, available:117000, color:'#8B5CF6' },
  { type:'Damaged',     fill:12, total:42000,  available:5040,   color:'#EF4444' },
]

// ─── DATA SOURCES ─────────────────────────────────────────────────────────────
export const DATA_SOURCES = [
  { name:'PortSight™ Live',   status:'Connected', latency:'1.2s', records:'2.4M',   icon:'🛰', color:'green' },
  { name:'AIS Vessel Feed',   status:'Connected', latency:'0.8s', records:'14.2K',  icon:'⚓', color:'green' },
  { name:'SAP TM Inventory',  status:'Connected', latency:'3.1s', records:'847K',   icon:'💼', color:'green' },
  { name:'Weather / ECMWF',   status:'Connected', latency:'5.4s', records:'Global', icon:'🌤', color:'green' },
  { name:'Geopolitical API',  status:'Connected', latency:'2.7s', records:'180+',   icon:'🌍', color:'green' },
  { name:'Market Price Feed', status:'Connected', latency:'1.9s', records:'Daily',  icon:'📈', color:'green' },
]

// ─── DASHBOARD KPIs ───────────────────────────────────────────────────────────
export const PROBLEM_STATE_KPIS = {
  emptyRepositioningCost: { value:'$1.82B',   change:+12.4, label:'Empty Repositioning Cost',  period:'YTD',    unit:'USD', inverse:true  },
  slaAdherence:           { value:'62.3%',    change:-8.2,  label:'SLA Adherence',             period:'MTD',    unit:'%',   inverse:false },
  manualTimeline:         { value:'72 hrs',   change:+5.1,  label:'Manual Repositioning Time', period:'Avg',    unit:'hrs', inverse:true  },
  decisionTime:           { value:'72 hrs',   change:0,     label:'Decision Time (Manual)',    period:'Manual', unit:'hrs', inverse:true  },
  proactiveAlerts:        { value:0,          change:0,     label:'Proactive Alerts',          period:'Now',    unit:''                   },
  bookingNotifications:   { value:'0 queued', change:0,     label:'Booking Notifications',     period:'Live',   unit:''                   },
  containerLeaseCost:     { value:'$3.1B',    change:+8.5,  label:'Container Leasing Cost',    period:'Annual', unit:'USD', inverse:true  },
  coLoadSavings:          { value:'$0',       change:0,     label:'Co-load Savings Captured',  period:'Today',  unit:'USD', inverse:false },
  co2Reduction:           { value:'0%',       change:0,     label:'CO₂ Reduction YTD',         period:'YTD',    unit:'%',   inverse:false },
}

export const RESOLVED_KPIS = {
  emptyRepositioningCost: { value:'$1.20B',   change:-34,   label:'Empty Repositioning Cost',  period:'Annual',     unit:'USD', inverse:true  },
  slaAdherence:           { value:'97.8%',    change:+35.5, label:'SLA Adherence',             period:'ATLAS',      unit:'%',   inverse:false },
  manualTimeline:         { value:'<10 min',  change:-99,   label:'AI Repositioning Time',     period:'ATLAS',      unit:'',    inverse:true  },
  decisionTime:           { value:'4.2s',     change:-99,   label:'AI Decision Time',          period:'AI',         unit:'sec', inverse:true  },
  proactiveAlerts:        { value:0,          change:0,     label:'Proactive Alerts',          period:'Now',        unit:''                   },
  bookingNotifications:   { value:'132 sent', change:+594,  label:'Booking Notifications',     period:'Automated',  unit:''                   },
  containerLeaseCost:     { value:'$2.1B',    change:-32,   label:'Container Leasing Cost',    period:'Annual',     unit:'USD', inverse:true  },
  coLoadSavings:          { value:'$286K',    change:+741,  label:'Co-load Savings Captured',  period:'Today',      unit:'USD', inverse:false },
  co2Reduction:           { value:'23%',      change:+19,   label:'CO₂ Reduction YTD',         period:'YTD',        unit:'%',   inverse:false },
}

export const DASHBOARD_KPIS = PROBLEM_STATE_KPIS

// ─── COST HISTORY ────────────────────────────────────────────────────────────
export const COST_HISTORY = [
  { year:2020, cost:1820, lease:3100 },
  { year:2021, cost:2100, lease:4200 },
  { year:2022, cost:2350, lease:4850 },
  { year:2023, cost:1980, lease:3900 },
  { year:2024, cost:1620, lease:3200 },
  { year:2025, cost:1470, lease:2100 },
]

// ─── USE CASES — AI Modules ───────────────────────────────────────────────────
export const USE_CASES = [
  {
    id:'control_tower',
    title:'Control Tower',
    subtitle:'Supply Chain AI',
    icon:'🗼',
    color:'#5B8DB8',
    active:false,
    kpis:[
      '<5 min exception triage',
      '60%+ manual reduction',
      '97% on-time visibility',
      '$150M+/yr value',
      '700 vessels monitored',
      '14 data integrations',
    ],
    description:'Global shipment visibility and exception orchestration across fragmented operations.',
    annualValue:'$150M+',
    features:['Exception detection', 'Self-service visibility', 'Utilization uplift'],
  },
  {
    id:'container_sc',
    title:'Container Supply Chain',
    subtitle:'Repositioning AI',
    icon:'📦',
    color:'#00B4D8',
    active:true,
    kpis:[
      '<10 min response',
      '34% cost reduction',
      '97.8% SLA adherence',
      '$250M+/yr value',
      '72-hr advance prediction',
      '4.2s decision time',
    ],
    description:'AI-driven empty container repositioning with disruption simulation and autonomous execution.',
    annualValue:'$250M',
    features:['Demand sensing', 'Supply optimization', 'SAP auto-execution'],
    route:'/container-sc',
  },
  {
    id:'fuel_optimization',
    title:'Fuel Optimization',
    subtitle:'Voyage AI',
    icon:'⚡',
    color:'#F59E0B',
    active:false,
    kpis:[
      '10–15% fuel reduction',
      '$300M+/yr value',
      '$80M bunkering savings',
      '53% CO₂ reduction',
      'Real-time weather routing',
      'Multi-port bunker optimizer',
    ],
    description:'Weather-adaptive voyage optimization using telemetry, bunker pricing, and carbon indices.',
    annualValue:'$300M+',
    features:['Weather routing', 'Speed optimization', 'Bunker planning'],
  },
  {
    id:'pricing_intelligence',
    title:'Pricing Intelligence',
    subtitle:'Revenue AI',
    icon:'💰',
    color:'#10B981',
    active:false,
    kpis:[
      'Same-day GRI surcharges',
      '80% contract risk reduction',
      '$2.78B+/yr protection',
      '1,200+ contracts covered',
      'Automated surcharge capture',
      'Spot-contract arbitrage',
    ],
    description:'Automated surcharge recovery and contract pricing across 1,200+ contracts.',
    annualValue:'$2.78B+',
    features:['Surcharge automation', 'Contract compliance', 'Spot coordination'],
  },
  {
    id:'aiops',
    title:'AIOps & Self-Healing IT',
    subtitle:'IT Ops AI',
    icon:'🔧',
    color:'#8B5CF6',
    active:false,
    kpis:[
      '4.5 hrs → 4 min MTTR',
      '55% L1 ticket deflection',
      '$100M+/yr savings',
      '99.97% uptime achieved',
      'Graph AI dependency map',
      'Zero-touch self-healing',
    ],
    description:'Graph AI dependency mapping to prevent cascading failures across enterprise applications.',
    annualValue:'$100M+',
    features:['Dependency mapping', 'Ticket deflection', 'Self-healing workflows'],
  },
]

// ─── NEWS ITEMS — with real clickable URLs ────────────────────────────────────
export const NEWS_ITEMS = [
  {
    text:'⚓ OOCL TIANJIN departs Busan Apr 18 — 3,120 empty TEU capacity confirmed for transpacific run',
    url:'https://www.marinetraffic.com/en/ais/home/centerx:129.04/centery:35.10/zoom:8',
  },
  {
    text:'📊 Vietnam PMI 54.2 in March — six-month high; export orders +18% MoM per S&P Global',
    url:'https://www.spglobal.com/marketintelligence/en/mi/research-analysis/vietnam-manufacturing-pmi.html',
  },
  {
    text:'🌤 Suez Canal transit times normalising — Mediterranean corridor recovering after Red Sea re-routing',
    url:'https://www.suezcanal.gov.eg/English/Pages/default.aspx',
  },
  {
    text:'📦 Ane-Maersk pre-positions 830 TEU at Manila ahead of Philippines peak season — ATLAS signal confirmed',
    url:'https://www.maersk.com/news/articles/2025/09/18/maersk-increases-capacity-on-philippine-routes',
  },
  {
    text:'💰 Spot rates Asia–North Europe +3.2% WoW — Freightos Baltic Index FBX01 at 2,840 (Apr 17)',
    url:'https://fbx.freightos.com/',
  },
  {
    text:'⚠️ Port Said container shortage -420 TEU — Egyptian cotton export window Apr 22–28 at risk',
    url:'https://www.suezcanal.gov.eg/English/About/SuezCanalWaterway/Pages/PortSaid.aspx',
  },
  {
    text:'🛸 AIS Alert: MSC AURORA ETA Ho Chi Minh City Apr 19 — 3,080 empty TEU offload scheduled',
    url:'https://www.marinetraffic.com/en/ais/home/centerx:106.70/centery:10.77/zoom:10',
  },
  {
    text:'🌍 India Manufacturing PMI 58.1 — 11-year high; FY2026 auto exports on track for record USD 22B',
    url:'https://www.spglobal.com/marketintelligence/en/mi/research-analysis/india-manufacturing-pmi.html',
  },
  {
    text:'📦 Bangladesh RMG PMI 56.8 — container shortage at Chittagong; CMA CGM LIBERTY rerouting via Colombo',
    url:'https://www.bgmea.com.bd/page/Export_Performance',
  },
  {
    text:'⚡ Samsung Electronics confirms 580 TEU semiconductor booking — ATLAS co-load match in progress',
    url:'https://news.samsung.com/global/samsungs-semiconductor-division',
  },
]

// ─── IMPACT METRICS ───────────────────────────────────────────────────────────
export const IMPACT = {
  costPerTEUBefore:   412,
  costPerTEUAfter:    298,
  costReduction:      '28%',
  slaBefore:          '62.3%',
  slaAfter:           '97.8%',
  responseTimeBefore: '72 hours',
  responseTimeAfter:  '4.2 seconds',
  co2Reduction:       '53.4%',
  annualValue:        '$250M',
  roiPayback:         '6 months',
}
