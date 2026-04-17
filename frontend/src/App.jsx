import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import ContainerSC from './pages/ContainerSC'

export default function App() {
  return (
    <Routes>
      <Route path="/"             element={<Home />} />
      <Route path="/container-sc" element={<ContainerSC />} />
    </Routes>
  )
}
