import axios from 'axios'
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || '/api'
export async function translateCode(body){ return axios.post(`${API_BASE}/ai-translate`, body).then(r=>r.data) }
