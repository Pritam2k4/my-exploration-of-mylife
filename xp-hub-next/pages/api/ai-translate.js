import { NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

function isUnsafe(code){
  const patterns = [/\b(exec|system|spawn|fork)\b/i, /\b(require\(['\"]child_process['\"]\)/i, /curl\s+/i, /wget\s+/i, /rm\s+-rf/i, /os\.system\(/i];
  return patterns.some(r=>r.test(code));
}

export default async function handler(req, res){
  if (req.method !== 'POST') return res.status(405).end();
  const { code, from_lang, to_lang } = req.body || {};
  if (!code || !from_lang || !to_lang) return res.status(400).json({ error: 'missing' });
  if (isUnsafe(code)) return res.json({ translation: null, explanation: null, warnings: 'unsafe code blocked' });

  const system = `You are a helpful coding assistant that translates code from ${from_lang} to ${to_lang} and explains changes in plain English for students aged 13-25. Return JSON with {translation, explanation, warnings}. Do not execute code.`;
  const user = `Translate this code:\n\n${code}\n\nRespond ONLY in JSON with keys: translation, explanation, warnings.`;

  try{
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'system', content: system }, { role: 'user', content: user }],
      max_tokens: 800,
      temperature: 0.2
    });
    const raw = completion.choices?.[0]?.message?.content || '';
    let parsed;
    try { parsed = JSON.parse(raw); } catch (e) {
      const m = raw.match(/\{[\s\S]*\}/);
      parsed = m ? JSON.parse(m[0]) : { translation: raw, explanation: '', warnings: '' };
    }
    return res.status(200).json(parsed);
  }catch(err){
    console.error(err);
    return res.status(500).json({ error: 'ai_error', details: String(err) });
  }
}
