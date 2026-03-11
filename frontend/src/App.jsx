import React, { useState, useEffect } from 'react'
import './App.css'
import api from './api'
import Navbar from './components/Navbar'
import Dashboard from './components/Dashboard'
import Lessons from './components/Lessons'
import Quiz from './components/Quiz'
import IDE from './components/IDE'
import Chatbot from './components/Chatbot'
import Certificates from './components/Certificates'
import Login from './components/Login'
import Signup from './components/Signup'

export default function App(){
  const [page, setPage] = useState('dashboard')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [authPage, setAuthPage] = useState('login') // 'login' or 'signup'
  const [username, setUsername] = useState('')

  const fetchUserProfile = async () => {
    try {
      const response = await api.get('/profile/');
      setUsername(response.data.display_name);
    } catch (error) {
      console.error("Failed to fetch user profile:", error);
      // Handle error, e.g., logout user if token is invalid
      handleLogout();
    }
  };

  // Check if user is already logged in on mount
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsLoggedIn(true)
      fetchUserProfile(); // Fetch user profile if already logged in
    }
  }, [])

  // Handle login success
  const handleLoginSuccess = () => {
    setIsLoggedIn(true)
    setPage('dashboard')
    fetchUserProfile(); // Fetch user profile after successful login
  }

  // Handle signup success
  const handleSignupSuccess = () => {
    setIsLoggedIn(true)
    setPage('dashboard')
    fetchUserProfile(); // Fetch user profile after successful signup
  }

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
    setIsLoggedIn(false)
    setPage('dashboard')
    setAuthPage('login')
    setUsername(''); // Clear username on logout
  }

  // Show login/signup if not logged in
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen w-screen">
        {authPage === 'login' ? (
          <Login 
            onLoginSuccess={handleLoginSuccess}
            onSwitchToSignup={() => setAuthPage('signup')}
          />
        ) : (
          <Signup 
            onSignupSuccess={handleSignupSuccess}
            onSwitchToLogin={() => setAuthPage('login')}
          />
        )}
        <div className="fixed bottom-4 left-4 text-white text-sm text-center">
          {authPage === 'login' ? (
            <button 
              onClick={() => setAuthPage('signup')}
              className="underline hover:no-underline"
            >
              Don't have an account? Sign up
            </button>
          ) : (
            <button 
              onClick={() => setAuthPage('login')}
              className="underline hover:no-underline"
            >
              Already have an account? Sign in
            </button>
          )}
        </div>
      </div>
    )
  }

  // Show dashboard if logged in
  return (
    <div className="flex flex-col h-screen w-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar 
        onNavigate={setPage} 
        currentPage={page} 
        onLogout={handleLogout}
        username={username}
      />
      <main className="flex-1 overflow-auto bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="min-h-full">
          {page === 'dashboard' && <Dashboard />}
          {page === 'lessons' && <Lessons />}
          {page === 'quiz' && <Quiz />}
          {page === 'ide' && <IDE />}
          {page === 'chat' && <Chatbot />}
          {page === 'certs' && <Certificates />}
        </div>
      </main>
    </div>
  )
}
