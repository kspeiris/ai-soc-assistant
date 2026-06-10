import { useEffect, useState } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell } from 'recharts'

export default function Dashboard() {
  const { token } = useAuth()
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    api.get('/dashboard/stats', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setStats(res.data))
      .catch(err => console.error(err))
  }, [token])

  if (!stats) return <div>Loading...</div>

  const severityData = Object.entries(stats.alerts_by_severity).map(([name, value]) => ({ name, value }))
  const COLORS = ['#10B981', '#FBBF24', '#F97316', '#EF4444']

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded shadow">Total Alerts: {stats.total_alerts}</div>
        <div className="bg-white p-4 rounded shadow">High Severity: {stats.high_severity_alerts}</div>
        <div className="bg-white p-4 rounded shadow">Open Incidents: {stats.open_incidents}</div>
        <div className="bg-white p-4 rounded shadow">Alerts (24h): {stats.alerts_last_24h}</div>
      </div>
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="font-semibold mb-2">Severity Distribution</h2>
          <PieChart width={300} height={300}>
            <Pie data={severityData} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="value" label>
              {severityData.map((_entry, idx) => <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="font-semibold mb-2">Alerts by Severity (Bar)</h2>
          <BarChart width={400} height={300} data={severityData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </div>
      </div>
    </div>
  )
}