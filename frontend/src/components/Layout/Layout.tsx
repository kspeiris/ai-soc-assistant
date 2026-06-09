import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

export default function Layout() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const handleLogout = () => { logout(); navigate('/login') }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-gray-800 text-white p-4 flex justify-between">
        <div className="space-x-4">
          <Link to="/">Dashboard</Link>
          <Link to="/alerts">Alerts</Link>
          <Link to="/incidents">Incidents</Link>
          <Link to="/chat">Chat Assistant</Link>
          <Link to="/settings">Settings</Link>
        </div>
        <button onClick={handleLogout} className="bg-red-600 px-3 py-1 rounded">Logout</button>
      </nav>
      <main><Outlet /></main>
    </div>
  )
}