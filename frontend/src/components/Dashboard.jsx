import React from 'react'
import { TrendingUp, Flame, Award, BookOpen } from 'lucide-react'

export default function Dashboard(){
  const stats = [
    { icon: TrendingUp, label: 'Learning Progress', value: '65%', color: 'from-blue-500 to-blue-600' },
    { icon: Flame, label: 'Current Streak', value: '7 days', color: 'from-orange-500 to-red-500' },
    { icon: Award, label: 'Badges Earned', value: '12', color: 'from-yellow-500 to-orange-500' },
    { icon: BookOpen, label: 'Topics Mastered', value: '8/25', color: 'from-green-500 to-emerald-500' },
  ]

  const recentTopics = [
    { id: 1, title: 'Variables & Data Types', progress: 95, difficulty: 'Beginner' },
    { id: 2, title: 'Control Flow (if/else)', progress: 80, difficulty: 'Beginner' },
    { id: 3, title: 'Functions & Scope', progress: 60, difficulty: 'Intermediate' },
  ]

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 animate-fadeIn">
          <h2 className="text-4xl font-bold text-white mb-2">Welcome back, Learner! 👋</h2>
          <p className="text-gray-400">Continue your Python mastery journey</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, idx) => {
            const Icon = stat.icon
            return (
              <div key={idx} className="glass p-6 rounded-xl hover:bg-opacity-20 transition-all duration-300 group animate-slideIn"
                style={{ animationDelay: `${idx * 100}ms` }}>
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon size={24} className="text-white" />
                </div>
                <p className="text-gray-400 text-sm font-medium">{stat.label}</p>
                <p className="text-3xl font-bold text-white mt-1">{stat.value}</p>
              </div>
            )
          })}
        </div>

        {/* Recent Learning */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="glass p-6 rounded-xl">
              <h3 className="text-xl font-bold text-white mb-6">Recent Topics</h3>
              <div className="space-y-4">
                {recentTopics.map(topic => (
                  <div key={topic.id} className="p-4 bg-white bg-opacity-5 rounded-lg hover:bg-opacity-10 transition-all duration-200 border border-white border-opacity-10">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-white font-semibold">{topic.title}</h4>
                      <span className="text-xs px-2 py-1 rounded-full bg-blue-500 bg-opacity-20 text-blue-300">{topic.difficulty}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-cyan-400 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${topic.progress}%` }}
                      ></div>
                    </div>
                    <p className="text-gray-400 text-xs mt-2">{topic.progress}% Complete</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="glass p-6 rounded-xl">
            <h3 className="text-xl font-bold text-white mb-6">Quick Actions</h3>
            <div className="space-y-3">
              <button className="btn-primary w-full">Start Lesson</button>
              <button className="btn-secondary w-full">Take Quiz</button>
              <button className="btn-ghost w-full">Ask Chatbot</button>
              <button className="btn-ghost w-full">View Certificates</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
