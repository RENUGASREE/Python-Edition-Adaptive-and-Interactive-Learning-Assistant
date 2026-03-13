import React, { useEffect, useState } from 'react'
import api from '../api'
import { BookOpen, Play, Clock, Zap, ArrowLeft, CheckCircle, XCircle } from 'lucide-react'

export default function Lessons(){
  const [modules, setModules] = useState([])
  const [selectedLesson, setSelectedLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lessonLoading, setLessonLoading] = useState(false)

  useEffect(()=>{
    fetchModules()
  },[])

  const fetchModules = async () => {
    try {
      const response = await api.get('/modules')
      setModules(response.data)
    } catch (error) {
      console.error('Failed to fetch modules:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchLesson = async (lessonId) => {
    setLessonLoading(true)
    try {
      const response = await api.get(`/lessons/${lessonId}`)
      setSelectedLesson(response.data)
    } catch (error) {
      console.error('Failed to fetch lesson:', error)
    } finally {
      setLessonLoading(false)
    }
  }

  const submitQuiz = async (quizId, answers) => {
    try {
      const response = await api.post(`/quizzes/${quizId}/submit`, { answers })
      return response.data
    } catch (error) {
      console.error('Failed to submit quiz:', error)
      throw error
    }
  }

  if (selectedLesson) {
    return <LessonDetail lesson={selectedLesson} onBack={() => setSelectedLesson(null)} onSubmitQuiz={submitQuiz} loading={lessonLoading} />
  }

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-white mb-2">Learning Modules</h2>
          <p className="text-gray-400">Personalized lessons tailored to your learning pace</p>
        </div>

        {loading ? (
          <div className="text-center text-white">Loading modules...</div>
        ) : (
          <div className="space-y-8">
            {modules.map(module => (
              <div key={module.id} className="glass p-6 rounded-xl">
                <h3 className="text-2xl font-bold text-white mb-4">{module.title}</h3>
                <p className="text-gray-400 mb-4">{module.description}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* Assuming lessons are in module.lessons */}
                  {module.lessons?.map(lesson => (
                    <div key={lesson.id} className="p-4 bg-white bg-opacity-5 rounded-lg hover:bg-opacity-10 transition-all cursor-pointer" onClick={() => fetchLesson(lesson.id)}>
                      <h4 className="text-white font-semibold">{lesson.title}</h4>
                      <p className="text-gray-400 text-sm">{lesson.difficulty}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function LessonDetail({ lesson, onBack, onSubmitQuiz, loading }) {
  const [quizAnswers, setQuizAnswers] = useState({})
  const [quizResult, setQuizResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const handleQuizSubmit = async () => {
    if (!lesson.quizzes || lesson.quizzes.length === 0) return
    
    const quiz = lesson.quizzes[0]
    if (quiz.attempted) return

    const answers = Object.entries(quizAnswers).map(([qId, selected]) => ({
      question_id: parseInt(qId),
      selected: parseInt(selected)
    }))

    setSubmitting(true)
    try {
      const result = await onSubmitQuiz(quiz.id, answers)
      setQuizResult(result)
    } catch (error) {
      console.error('Quiz submission failed:', error)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
        <div className="max-w-4xl mx-auto text-center text-white">Loading lesson...</div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        <button onClick={onBack} className="btn-ghost mb-6 flex items-center gap-2">
          <ArrowLeft size={20} /> Back to Modules
        </button>

        <div className="glass p-8 rounded-xl">
          <h2 className="text-3xl font-bold text-white mb-4">{lesson.title}</h2>
          <div className="prose prose-invert max-w-none mb-8" dangerouslySetInnerHTML={{ __html: lesson.content }} />

          {lesson.quizzes && lesson.quizzes.length > 0 && (
            <div className="mt-8">
              <h3 className="text-xl font-bold text-white mb-4">Lesson Quiz</h3>
              {lesson.quizzes.map(quiz => (
                <div key={quiz.id} className="bg-white bg-opacity-5 p-6 rounded-lg">
                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-cyan-400 font-semibold">AI Generated Quiz</span>
                  </div>
                  
                  {quiz.attempted ? (
                    <div className="text-center">
                      <p className="text-white text-lg">Your Score: {quiz.score} / {quiz.total_questions}</p>
                    </div>
                  ) : quizResult ? (
                    <div className="text-center">
                      <p className="text-white text-lg">Your Score: {quizResult.score} / {quizResult.total}</p>
                      <p className="text-gray-400">Percentage: {quizResult.percentage}%</p>
                    </div>
                  ) : (
                    <div>
                      {/* Quiz questions would be rendered here */}
                      <p className="text-gray-400 mb-4">Quiz questions not implemented in frontend yet.</p>
                      <button 
                        onClick={handleQuizSubmit} 
                        disabled={submitting}
                        className="btn-primary"
                      >
                        {submitting ? 'Submitting...' : 'Submit Quiz'}
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
