import React, { useState } from 'react'
import { gradeSubmission } from '../api'
import { CheckCircle2, AlertCircle, Loader } from 'lucide-react'

export default function Quiz(){
  const [code, setCode] = useState('# Complete the function\ndef solve(n):\n    # Your code here\n    pass\n')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const submit = async ()=>{
    setLoading(true)
    try {
      const res = await gradeSubmission(1, 'demo-problem', code)
      setResult(res)
    } catch (e) {
      setResult({ passed: false, feedback: 'Error submitting code. Ensure backend is running.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white mb-2">Coding Quiz</h2>
          <p className="text-gray-400">Write Python code and get instant feedback</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Problem */}
          <div className="glass p-6 rounded-xl">
            <h3 className="text-lg font-bold text-white mb-4">Problem</h3>
            <div className="space-y-4 text-gray-300">
              <div>
                <p className="font-semibold text-cyan-400">Problem #1: Simple Function</p>
                <p className="text-sm mt-2">Write a function that checks if a number is even.</p>
              </div>
              <div className="bg-white bg-opacity-5 p-4 rounded-lg border border-white border-opacity-10">
                <p className="text-xs font-mono">Input: n = 10</p>
                <p className="text-xs font-mono">Output: True</p>
              </div>
              <div className="text-xs text-gray-500">
                <p>Difficulty: <span className="text-yellow-400">Beginner</span></p>
                <p>Time Limit: 5 minutes</p>
              </div>
            </div>
          </div>

          {/* Code Editor */}
          <div className="lg:col-span-2">
            <div className="glass p-6 rounded-xl">
              <h3 className="text-lg font-bold text-white mb-4">Your Solution</h3>
              <textarea 
                value={code} 
                onChange={e=>setCode(e.target.value)} 
                rows={14}
                className="w-full bg-slate-900 border border-white border-opacity-20 rounded-lg p-4 text-white font-mono text-sm focus:outline-none focus:border-cyan-400 focus:border-opacity-50 resize-none"
                placeholder="Write your Python code here..."
              />
              <button 
                onClick={submit} 
                disabled={loading}
                className="btn-primary w-full mt-4 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader size={18} className="animate-spin" /> Evaluating...
                  </>
                ) : (
                  <>
                    Submit Solution
                  </>
                )}
              </button>

              {/* Result */}
              {result && (
                <div className={`mt-4 p-4 rounded-lg border ${result.passed ? 'bg-green-500 bg-opacity-10 border-green-500 border-opacity-30' : 'bg-red-500 bg-opacity-10 border-red-500 border-opacity-30'}`}>
                  <div className="flex items-center gap-2 mb-2">
                    {result.passed ? (
                      <>
                        <CheckCircle2 size={20} className="text-green-400" />
                        <span className="font-bold text-green-400">Passed!</span>
                      </>
                    ) : (
                      <>
                        <AlertCircle size={20} className="text-red-400" />
                        <span className="font-bold text-red-400">Not Passed</span>
                      </>
                    )}
                  </div>
                  <p className="text-gray-300">{result.feedback}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
