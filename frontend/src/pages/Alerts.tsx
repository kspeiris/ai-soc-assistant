import { useEffect, useState } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'
import toast from 'react-hot-toast'

interface Alert {
  id: string
  timestamp: string
  severity: string
  description: string
  source: string
  status: string
}

export default function Alerts() {
  const { token } = useAuth()
  const [alerts, setAlerts] = useState<Alert[]>([])

  useEffect(() => {
    api.get('/alerts', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setAlerts(res.data))
  }, [token])

  const resolveAlert = async (id: string) => {
    await api.post(`/alerts/${id}/resolve`, {}, { headers: { Authorization: `Bearer ${token}` } })
    toast.success('Alert resolved')
    setAlerts(alerts.map(a => a.id === id ? { ...a, status: 'resolved' } : a))
  }

  const severityColor = (sev: string) => {
    switch(sev) {
      case 'high': return 'text-red-600'
      case 'medium': return 'text-yellow-600'
      case 'low': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Security Alerts</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded shadow">
          <thead>
            <tr className="border-b">
              <th className="p-3 text-left">Time</th><th>Severity</th><th>Description</th><th>Source</th><th>Status</th><th></th>
            </tr>
          </thead>
          <tbody>
            {alerts.map(alert => (
              <tr key={alert.id} className="border-b hover:bg-gray-50">
                <td className="p-3">{new Date(alert.timestamp).toLocaleString()}</td>
                <td className={`font-semibold ${severityColor(alert.severity)}`}>{alert.severity}</td>
                <td>{alert.description.slice(0, 80)}...</td>
                <td>{alert.source}</td>
                <td>{alert.status}</td>
                <td>{alert.status === 'new' && <button onClick={() => resolveAlert(alert.id)} className="bg-blue-500 text-white px-3 py-1 rounded text-sm">Resolve</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}