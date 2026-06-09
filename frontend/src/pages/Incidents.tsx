import { useEffect, useState } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

interface Incident {
  id: string
  title: string
  severity: string
  status: string
  created_at: string
}

export default function Incidents() {
  const { token } = useAuth()
  const [incidents, setIncidents] = useState<Incident[]>([])

  useEffect(() => {
    api.get('/incidents', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setIncidents(res.data))
  }, [token])

  const downloadReport = async (id: string) => {
    const res = await api.get(`/incidents/${id}/report`, { headers: { Authorization: `Bearer ${token}` }, responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `incident_${id}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Incidents</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded shadow">
          <thead><tr><th>Title</th><th>Severity</th><th>Status</th><th>Created</th><th></th></tr></thead>
          <tbody>
            {incidents.map(inc => (
              <tr key={inc.id} className="border-b">
                <td className="p-3">{inc.title}</td><td>{inc.severity}</td><td>{inc.status}</td><td>{new Date(inc.created_at).toLocaleDateString()}</td>
                <td><button onClick={() => downloadReport(inc.id)} className="bg-green-600 text-white px-3 py-1 rounded text-sm">Report PDF</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}