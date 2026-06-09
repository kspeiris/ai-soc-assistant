import { useState } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

export default function ChatAssistant() {
  const { token } = useAuth()
  const [messages, setMessages] = useState<{role: 'user'|'assistant', content: string}[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'user' as const, content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await api.post('/chat', { message: input }, { headers: { Authorization: `Bearer ${token}` } })
      const assistantMsg = { role: 'assistant' as const, content: res.data.response }
      setMessages(prev => [...prev, assistantMsg])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error contacting AI' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 h-[calc(100vh-80px)] flex flex-col">
      <h1 className="text-2xl font-bold mb-4">AI SOC Assistant</h1>
      <div className="flex-1 overflow-y-auto bg-gray-100 rounded p-4 mb-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'}`}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && <div>AI is thinking...</div>}
      </div>
      <div className="flex gap-2">
        <input type="text" className="flex-1 border p-2 rounded" value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && sendMessage()} />
        <button onClick={sendMessage} className="bg-blue-600 text-white px-4 py-2 rounded">Send</button>
      </div>
    </div>
  )
}