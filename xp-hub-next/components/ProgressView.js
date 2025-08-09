import React from 'react'
export default function ProgressView({ totalXpToday=0 }){
  const goal=100; const pct = Math.min(100, Math.round((totalXpToday/goal)*100))
  return (
    <div className="card">
      <h3 className="font-semibold">Progress</h3>
      <div className="small mt-2">Daily goal: {goal} XP</div>
      <div className="h-3 bg-gray-200 rounded mt-2 overflow-hidden"><div style={{width:pct+'%'}} className="h-full bg-gradient-to-r from-indigo-600 to-teal-400"></div></div>
      <div className="small mt-2">{totalXpToday} / {goal} XP • {pct}%</div>
    </div>
  )
}
