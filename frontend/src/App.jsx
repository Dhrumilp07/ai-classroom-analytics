import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [data, setData] = useState({ students_present: 0, engagement_score: 0 })
  const [isLive, setIsLive] = useState(false)
  const [error, setError] = useState(null)
  
  const API_URL = "http://localhost:5001"
  const API_KEY = "classroom_secure_key"

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`${API_URL}/analytics`, {
        headers: { "x-api-key": API_KEY }
      })
      if (!response.ok) throw new Error("Unauthorized or server error")
      const result = await response.json()
      setData(result)
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  // Fetch periodically if live
  useEffect(() => {
    let interval;
    if (isLive) {
      interval = setInterval(fetchAnalytics, 2000)
    }
    return () => clearInterval(interval)
  }, [isLive])

  const handleStartCamera = async () => {
    try {
      const response = await fetch(`${API_URL}/start_camera`, {
        method: "POST",
        headers: { "x-api-key": API_KEY }
      })
      if (!response.ok) throw new Error("Could not start camera")
      // Once camera started, auto start live analytics!
      setIsLive(true)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="logo-section">
          <div className="pulse-dot"></div>
          <h1>AI Classroom Hub</h1>
        </div>
        <p className="subtitle">Real-time local tracking analytics</p>
      </header>

      <main className="main-content">
        <div className="cards-grid">
          <div className="stat-card">
            <h3>Students Present</h3>
            <div className="stat-value highlight">{data.students_present}</div>
          </div>
          
          <div className="stat-card">
            <h3>Engagement Score</h3>
            <div className="stat-value">
              {data.engagement_score}%
            </div>
            <div className="progress-bar-container">
              <div 
                className="progress-bar" 
                style={{ width: `${data.engagement_score}%`, background: data.engagement_score > 60 ? 'linear-gradient(90deg, #00f2fe 0%, #4facfe 100%)' : 'linear-gradient(90deg, #ff0844 0%, #ffb199 100%)' }}
              ></div>
            </div>
          </div>
        </div>

        <div className="controls">
          <button 
            className="btn btn-primary interactive-glow" 
            onClick={handleStartCamera}
          >
            Start Camera System
          </button>
          
          <button 
            className={`btn ${isLive ? 'btn-danger' : 'btn-secondary'}`} 
            onClick={() => setIsLive(!isLive)}
          >
            {isLive ? 'Stop Live Analytics' : 'Start Live Analytics'}
          </button>
        </div>

        {error && <div className="error-badge">Backend Error: {error}. Make sure the Flask API is running!</div>}
      </main>
      
      <div className="bg-glow-1"></div>
      <div className="bg-glow-2"></div>
    </div>
  )
}

export default App
