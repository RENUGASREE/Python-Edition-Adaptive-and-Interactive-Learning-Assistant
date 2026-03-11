import React, { useEffect, useState } from 'react'
import { recommend } from '../api'
import { BookOpen, Play, Clock, Zap } from 'lucide-react'

export default function Lessons(){
  const [recs, setRecs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    setLoading(true)
    recommend(1).then(r=>setRecs(r)).catch(()=>{}).finally(()=>setLoading(false))
  },[])

  const lessons = [
    { id: 1, title: 'Python Basics', duration: '2h 30m', level: 'Beginner', progress: 100, image: '📚' },
    { id: 2, title: 'Data Types & Variables', duration: '1h 45m', level: 'Beginner', progress: 80, image: '📦' },
    { id: 3, title: 'Control Flow', duration: '2h', level: 'Beginner', progress: 60, image: '🔀' },
    { id: 4, title: 'Functions & Modules', duration: '2h 15m', level: 'Intermediate', progress: 40, image: '🔧' },
  ]

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white mb-2">Learning Modules</h2>
          <p className="text-gray-400">Personalized lessons tailored to your learning pace</p>
        </div>

        {/* Recommended Section */}
        {recs.length > 0 && (
          <div className="glass p-6 rounded-xl mb-8">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Zap size={20} className="text-yellow-400" /> Recommended for You
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recs.map((r, idx)=>(
                <div key={idx} className="p-4 bg-white bg-opacity-5 rounded-lg border border-yellow-500 border-opacity-30 hover:bg-opacity-10 transition-all">
                  <p className="text-yellow-400 font-semibold">{r.title}</p>
                  <p className="text-gray-400 text-sm mt-1">{r.reason}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Lessons Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {lessons.map((lesson, idx) => (
            <div key={lesson.id} className="group cursor-pointer animate-slideIn" style={{ animationDelay: `${idx * 100}ms` }}>
              <div className="glass p-0 overflow-hidden rounded-xl transition-all duration-300 hover:scale-105 hover:bg-opacity-20">
                <div className="bg-gradient-to-br from-blue-500 to-cyan-500 h-32 flex items-center justify-center text-5xl group-hover:scale-110 transition-transform duration-300">
                  {lesson.image}
                </div>
                <div className="p-4">
                  <h4 className="text-white font-bold group-hover:text-cyan-400 transition-colors">{lesson.title}</h4>
                  <p className="text-gray-400 text-xs mt-1">{lesson.level}</p>
                  <div className="mt-3 space-y-2">
                    <div className="w-full bg-gray-700 rounded-full h-1.5">
                      <div className="bg-gradient-to-r from-blue-500 to-cyan-400 h-1.5 rounded-full" style={{ width: `${lesson.progress}%` }}></div>
                    </div>
                    <p className="text-gray-400 text-xs">{lesson.progress}% Complete</p>
                  </div>
                  <div className="flex items-center gap-2 text-gray-400 text-xs mt-3">
                    <Clock size={14} /> {lesson.duration}
                  </div>
                  <button className="btn-primary w-full mt-4">Continue</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
