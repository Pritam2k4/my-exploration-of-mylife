import React, {useState} from 'react'
export default function TaskEditor({task, onSave, onClose}){
  const [title, setTitle] = useState(task?.title||'')
  const [xp, setXp] = useState(task?.xp_value||10)
  const [category, setCategory] = useState(task?.category||'General')
  function submit(){ if(!title) return alert('Title required'); onSave({ ...task, title, xp_value: Number(xp), category }) }
  return (
    <div className="card mt-4">
      <h3 className="font-semibold">{task? 'Edit':'New'} Task</h3>
      <div className="mt-2"><input value={title} onChange={e=>setTitle(e.target.value)} className="w-full border p-2 rounded" placeholder="Task title" /></div>
      <div className="flex gap-2 mt-2">
        <input value={xp} onChange={e=>setXp(e.target.value)} className="w-24 border p-2 rounded" />
        <input value={category} onChange={e=>setCategory(e.target.value)} className="flex-1 border p-2 rounded" />
      </div>
      <div className="flex justify-end gap-2 mt-3">
        <button className="button" onClick={submit}>Save</button>
        <button onClick={onClose} className="border p-2 rounded">Cancel</button>
      </div>
    </div>
  )
}
