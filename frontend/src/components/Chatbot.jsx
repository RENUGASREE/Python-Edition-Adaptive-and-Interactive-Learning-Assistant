import React, { useState, useRef, useEffect } from 'react'
import { chatQuery } from '../api'
import { Send, Loader, MessageCircle } from 'lucide-react'

export default function Chatbot(){
  const [q, setQ] = useState('')
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hi! 👋 I\'m your Python learning assistant. Ask me anything about Python concepts, debugging, or best practices.' }
  ])
  const [loading, setLoading] = useState(false)
  const messagesEnd = useRef(null)

  const scrollToBottom = () => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(scrollToBottom, [messages])

  const send = async ()=>{
    if (!q.trim()) return
    
    const userMsg = q
    setQ('')
    setMessages(prev => [...prev, { role: 'user', text: userMsg }])
    setLoading(true)

    try {
      const r = await chatQuery(1, userMsg)
      setMessages(prev => [...prev, { role: 'bot', text: r.answer, sources: r.sources }])
    } catch (e) {
      setMessages(prev => [...prev, { role: 'bot', text: 'Sorry, I encountered an error. Please ensure the backend is running.' }])
    } finally {
      setLoading(false)
    }
  }

  const suggestions = [
    'How do I reverse a list?',
    'What\'s the difference between lists and tuples?',
    'How do I write a recursive function?',
    'What is a lambda function?'
  ]

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8 flex flex-col">
      <div className="max-w-4xl mx-auto w-full flex flex-col h-full">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white mb-2 flex items-center gap-2">
            <MessageCircle size={36} className="text-cyan-400" /> AI Chatbot
          </h2>
          <p className="text-gray-400">Ask questions about Python, get help with debugging, or learn new concepts</p>
        </div>

        {/* Chat Container */}
        <div className="glass rounded-xl flex flex-col flex-1 overflow-hidden mb-6">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slideIn`}>
                <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-white bg-opacity-10 text-gray-100 rounded-bl-none border border-white border-opacity-20'
                }`}>
                  <p className="text-sm">{msg.text}</p>
                  {msg.sources && (
                    <div className="mt-2 pt-2 border-t border-white border-opacity-20">
                      <p className="text-xs font-semibold text-gray-300">Sources:</p>
                      {msg.sources.map((s, i) => (
                        <p key={i} className="text-xs text-gray-400">• {s}</p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white bg-opacity-10 text-gray-100 px-4 py-3 rounded-lg rounded-bl-none border border-white border-opacity-20">
                  <Loader size={18} className="animate-spin" />
                </div>
              </div>
            )}
            <div ref={messagesEnd} />
          </div>

          {/* Suggestions */}
          {messages.length <= 1 && (
            <div className="px-6 pb-4">
              <p className="text-gray-400 text-xs mb-3">Quick suggestions:</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {suggestions.map((s, i) => (
                  <button 
                    key={i}
                    onClick={() => {
                      setQ(s)
                    }}
                    className="text-left text-xs p-2 rounded-lg bg-white bg-opacity-5 hover:bg-opacity-10 border border-white border-opacity-10 text-gray-300 hover:text-cyan-400 transition-all"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="border-t border-white border-opacity-10 p-6">
            <div className="flex gap-3">
              <input 
                type="text"
                value={q}
                onChange={e=>setQ(e.target.value)}
                onKeyPress={e => e.key === 'Enter' && send()}
                placeholder="Ask me anything about Python..."
                className="flex-1 bg-slate-900 border border-white border-opacity-20 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 focus:border-opacity-50"
              />
              <button 
                onClick={send}
                disabled={loading || !q.trim()}
                className="btn-secondary p-3 rounded-lg flex items-center justify-center"
              >
                {loading ? <Loader size={18} className="animate-spin" /> : <Send size={18} />}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
