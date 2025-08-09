import React, {useState} from 'react'
import dynamic from 'next/dynamic'
const Editor = dynamic(()=>import('@monaco-editor/react'), { ssr:false })

import { translateCode } from '../lib/api'

export default function CodingLab(){
  const [from, setFrom] = useState('Python')
  const [to, setTo] = useState('JavaScript')
  const [code, setCode] = useState("def greet(name):\n    print(f'Hello {name}')")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function doTranslate(){
    setLoading(true)
    try{
      const r = await translateCode({ code, from_lang: from, to_lang: to })
      setResult(r)
    }catch(e){ alert('Translation failed') } finally { setLoading(false) }
  }

  return (
    <div className="container">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">AI Coding Lab</h1>
        <a className="button" href="/">Back</a>
      </div>
      <div className="card">
        <div className="flex gap-2">
          <select value={from} onChange={e=>setFrom(e.target.value)} className="border p-1 rounded">
            <option>Python</option><option>JavaScript</option><option>Java</option><option>C</option><option>C++</option>
          </select>
          <div className="self-center">→</div>
          <select value={to} onChange={e=>setTo(e.target.value)} className="border p-1 rounded">
            <option>JavaScript</option><option>Python</option><option>Java</option><option>C</option><option>C++</option>
          </select>
        </div>
        <div className="mt-4">
          <Editor height='300px' defaultLanguage='python' value={code} onChange={v=>setCode(v)} />
        </div>
        <div className="mt-4">
          <button className="button" onClick={doTranslate} disabled={loading}>{loading? 'Working...':'Translate'}</button>
        </div>
        {result && (
          <div className="mt-4 card">
            <strong>Translation</strong>
            <pre className="whitespace-pre-wrap mt-2">{result.translation}</pre>
            <strong className="mt-2 block">Explanation</strong>
            <div className="small mt-2">{result.explanation}</div>
            {result.warnings && <div className="text-orange-600 mt-2">Warning: {result.warnings}</div>}
          </div>
        )}
      </div>
    </div>
  )
}
