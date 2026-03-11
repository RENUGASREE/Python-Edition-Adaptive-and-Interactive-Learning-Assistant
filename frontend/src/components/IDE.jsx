import React, { useState } from 'react'
import { gradeSubmission } from '../api'
import { Play, Copy, Loader } from 'lucide-react'

export default function IDE(){
  const [code, setCode] = useState('# Python Interactive IDE\n# Try writing some Python code!\n\ndef hello_world():\n    return "Hello, World!"\n\nprint(hello_world())\n')
  const [output, setOutput] = useState(null)
  const [loading, setLoading] = useState(false)

  const run = async ()=>{
    setLoading(true)
    try {
      const r = await gradeSubmission(1, 'ide-demo', code)
      setOutput(r)
    } catch (e) {
      setOutput({ passed: false, feedback: 'Connection error. Ensure backend is running.' })
    } finally {
      setLoading(false)
    }
  }

  const copyCode = () => {
    navigator.clipboard.writeText(code)
  }

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white mb-2">Interactive IDE</h2>
          <p className="text-gray-400">Write and test Python code in the browser</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Editor */}
          <div className="glass p-6 rounded-xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Code Editor</h3>
              <button onClick={copyCode} className="btn-ghost text-sm flex items-center gap-1">
                <Copy size={16} /> Copy
              </button>
            </div>
            <textarea 
              value={code} 
              onChange={e=>setCode(e.target.value)} 
              rows={16}
              className="w-full bg-slate-900 border border-white border-opacity-20 rounded-lg p-4 text-white font-mono text-sm focus:outline-none focus:border-cyan-400 focus:border-opacity-50 resize-none"
              placeholder="Write Python code..."
            />
            <button 
              onClick={run}
              disabled={loading}
              className="btn-secondary w-full mt-4 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader size={18} className="animate-spin" /> Running...
                </>
              ) : (
                <>
                  <Play size={18} /> Run Code
                </>
              )}
            </button>
          </div>

          {/* Output */}
          <div className="glass p-6 rounded-xl">
            <h3 className="text-lg font-bold text-white mb-4">Output & Feedback</h3>
            <div className="bg-slate-900 border border-white border-opacity-10 rounded-lg p-4 min-h-64 max-h-96 overflow-auto">
              {!output && (
                <p className="text-gray-500 text-sm">Run your code to see output here...</p>
              )}
              {output && (
                <div className="space-y-3">
                  <div className={`p-3 rounded-lg ${output.passed ? 'bg-green-500 bg-opacity-10 border border-green-500 border-opacity-30' : 'bg-blue-500 bg-opacity-10 border border-blue-500 border-opacity-30'}`}>
                    <p className={`font-mono text-sm ${output.passed ? 'text-green-400' : 'text-blue-400'}`}>
                      {output.feedback}
                    </p>
                  </div>
                  {output.score !== undefined && (
                    <div className="text-gray-300 text-sm">
                      <p>Score: <span className="font-bold text-cyan-400">{(output.score * 100).toFixed(0)}%</span></p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
