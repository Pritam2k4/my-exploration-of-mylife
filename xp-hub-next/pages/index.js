import React, { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import TaskEditor from '../components/TaskEditor'
import ProgressView from '../components/ProgressView'
const CodingLabLink = () => null

export default function Home(){
  const [demoMode, setDemoMode] = useState(true)
  const [tasks, setTasks] = useState([])
  const [showEditor, setShowEditor] = useState(false)
  const [totalXp, setTotalXp] = useState(0)

  useEffect(()=>{
    if (demoMode){
      const t = JSON.parse(localStorage.getItem('demo_tasks') || 'null')
      if (t) setTasks(t)
      else {
        const seed = [{id:'t1',title:'Read 20 pages',xp_value:15,category:'Study'},{id:'t2',title:'Solve one LeetCode',xp_value:25,category:'Coding'}]
        localStorage.setItem('demo_tasks', JSON.stringify(seed))
        setTasks(seed)
      }
    }
  },[demoMode])

  function saveTask(task){
    const arr = [...tasks.filter(t=>t.id!==task.id), {...task, id: task.id||('t'+Date.now())}]
    setTasks(arr); localStorage.setItem('demo_tasks', JSON.stringify(arr)); setShowEditor(false)
  }
  function complete(t){
    const xp = t.xp_value || 10; setTotalXp(x=>x+xp)
    const comps = JSON.parse(localStorage.getItem('demo_completions')||'[]'); comps.push({task_id:t.id,xp_awarded:xp,completed_at:new Date().toISOString()}); localStorage.setItem('demo_completions', JSON.stringify(comps))
    // small animation - toast
    alert(`+${xp} XP!`)
  }

  return (
    <div className="container">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">XP Hub</h1>
        <div>
          <button className="button" onClick={()=>{ setDemoMode(d=>!d); localStorage.setItem('demoMode', String(!demoMode))}}>{demoMode? 'Exit Demo':'Enter Demo'}</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2">
          <div className="card">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-semibold">Today</h2>
                <div className="small">XP: {totalXp}</div>
              </div>
              <div><button className="button" onClick={()=>setShowEditor(true)}>New Task</button></div>
            </div>
            <div className="mt-4">
              {tasks.map(t => (
                <div key={t.id} className="flex justify-between items-center border-b py-2">
                  <div>
                    <div className="font-medium">{t.title}</div>
                    <div className="small">{t.category} • {t.xp_value} XP</div>
                  </div>
                  <div><button className="button" onClick={()=>complete(t)}>Complete</button></div>
                </div>
              ))}
            </div>
          </div>
          {showEditor && <TaskEditor onSave={saveTask} onClose={()=>setShowEditor(false)} />}
        </div>
        <div>
          <div className="card mb-4">
            <h3 className="font-semibold">AI Coding Lab</h3>
            <div className="small mt-2">Translate code between languages and get plain-English explanations.</div>
            <div className="mt-4"><a className="button" href="/coding-lab">Open Coding Lab</a></div>
          </div>
          <ProgressView totalXpToday={totalXp} />
        </div>
      </div>
    </div>
  )
}
