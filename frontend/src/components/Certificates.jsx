import React from 'react'
import { Award, Download, QrCode } from 'lucide-react'

export default function Certificates(){
  const certificates = [
    { id: 1, module: 'Python Basics', date: '2025-12-01', verified: true, status: 'Earned' },
    { id: 2, module: 'Data Types & Variables', date: '2025-12-05', verified: true, status: 'Earned' },
    { id: 3, module: 'Control Flow', date: '2025-12-10', verified: false, status: 'In Progress' },
  ]

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
            <Award size={40} className="text-yellow-400" /> Certificates
          </h2>
          <p className="text-gray-400">Your earned module certificates with digital verification</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div className="glass p-4 rounded-xl">
            <p className="text-gray-400 text-sm">Earned</p>
            <p className="text-3xl font-bold text-green-400">2</p>
          </div>
          <div className="glass p-4 rounded-xl">
            <p className="text-gray-400 text-sm">In Progress</p>
            <p className="text-3xl font-bold text-blue-400">1</p>
          </div>
          <div className="glass p-4 rounded-xl">
            <p className="text-gray-400 text-sm">Available</p>
            <p className="text-3xl font-bold text-cyan-400">23</p>
          </div>
        </div>

        {/* Certificates List */}
        <div className="space-y-4">
          {certificates.map((cert) => (
            <div key={cert.id} className="glass p-6 rounded-xl hover:bg-opacity-20 transition-all duration-200">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div className="flex-1 min-w-fit">
                  <div className="flex items-center gap-3">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      cert.verified 
                        ? 'bg-gradient-to-br from-yellow-400 to-yellow-500' 
                        : 'bg-gradient-to-br from-gray-400 to-gray-500'
                    }`}>
                      <Award size={24} className="text-white" />
                    </div>
                    <div>
                      <h4 className="text-white font-bold text-lg">{cert.module}</h4>
                      <p className="text-gray-400 text-sm">Issued on {cert.date}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    cert.verified
                      ? 'bg-green-500 bg-opacity-20 text-green-300'
                      : 'bg-blue-500 bg-opacity-20 text-blue-300'
                  }`}>
                    {cert.status}
                  </span>

                  {cert.verified && (
                    <>
                      <button className="btn-secondary text-sm flex items-center gap-2">
                        <QrCode size={16} /> Verify
                      </button>
                      <button className="btn-ghost text-sm flex items-center gap-2">
                        <Download size={16} /> Download
                      </button>
                    </>
                  )}
                </div>
              </div>

              {cert.verified && (
                <div className="mt-4 p-4 bg-white bg-opacity-5 rounded-lg border border-white border-opacity-10">
                  <p className="text-gray-400 text-xs mb-2">Certificate ID:</p>
                  <p className="text-gray-300 font-mono text-sm break-all">CERT-{cert.id}-2025-{cert.module.replace(/\s/g, '')}</p>
                  <p className="text-gray-400 text-xs mt-2">✓ Digitally signed and QR verified</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Info Card */}
        <div className="glass p-6 rounded-xl mt-8">
          <h3 className="text-white font-bold mb-3">How Certificates Work</h3>
          <ul className="space-y-2 text-gray-300 text-sm">
            <li className="flex gap-2">
              <span className="text-cyan-400">•</span> Earn by completing module assessments with ≥80% score
            </li>
            <li className="flex gap-2">
              <span className="text-cyan-400">•</span> Digitally signed with your unique credential ID
            </li>
            <li className="flex gap-2">
              <span className="text-cyan-400">•</span> QR code links to verification page for authenticity
            </li>
            <li className="flex gap-2">
              <span className="text-cyan-400">•</span> Share on LinkedIn, resume, or portfolio
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
