import React, { useState } from 'react'
import { Code2, BookOpen, CheckSquare, Terminal, MessageCircle, Award, LogOut, User } from 'lucide-react'

export default function Navbar({ onNavigate, currentPage, onLogout, username }){
  const [showUserMenu, setShowUserMenu] = useState(false)

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Code2 },
    { id: 'lessons', label: 'Lessons', icon: BookOpen },
    { id: 'quiz', label: 'Quiz', icon: CheckSquare },
    { id: 'ide', label: 'IDE', icon: Terminal },
    { id: 'chat', label: 'Chatbot', icon: MessageCircle },
    { id: 'certs', label: 'Certificates', icon: Award },
  ]

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 border-b border-blue-500 border-opacity-20 backdrop-blur-lg">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-lg flex items-center justify-center">
              <Code2 size={24} className="text-slate-900" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                Python Edition
              </h1>
              <p className="text-xs text-gray-400">Adaptive Learning</p>
            </div>
          </div>
          
          <nav className="flex gap-1">
            {navItems.map(item => {
              const Icon = item.icon
              const isActive = currentPage === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'text-gray-300 hover:bg-white hover:bg-opacity-10 hover:text-cyan-400'
                  }`}
                >
                  <Icon size={18} />
                  <span className="hidden sm:inline">{item.label}</span>
                </button>
              )
            })}
          </nav>

          {/* User Profile Section */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white bg-opacity-10 hover:bg-opacity-20 text-cyan-400 transition-all"
            >
              <User size={18} />
              <span className="text-sm font-medium">{username || 'User'}</span>
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-slate-800 border border-blue-500 border-opacity-30 rounded-lg shadow-lg p-2 z-50">
                <button
                  onClick={() => {
                    setShowUserMenu(false)
                    onLogout()
                  }}
                  className="w-full flex items-center gap-2 px-4 py-2 text-red-400 hover:bg-white hover:bg-opacity-10 rounded-lg transition mt-2"
                >
                  <LogOut size={16} />
                  <span className="text-sm">Sign Out</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
