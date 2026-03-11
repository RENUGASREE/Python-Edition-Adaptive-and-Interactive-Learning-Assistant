# Python Edition: Adaptive and Interactive Learning Assistant

A comprehensive AI-powered, adaptive Python learning platform that personalizes the learning journey with intelligent recommendations, auto-graded coding challenges, RAG chatbot support, gamification, and exam integrity controls.

## 🚀 Key Features

- **Adaptive Learning** - Personalized recommendations based on learner profiling and knowledge tracing
- **Interactive IDE** - Browser-based code editor with instant feedback
- **Auto-Grader** - Sandbox-isolated code execution with unit test validation
- **AI Chatbot** - Context-aware assistant for Python concepts and debugging help
- **Gamification** - Badges, streaks, leaderboards, and certificates
- **Progress Analytics** - Dashboard with learning metrics and mastery visualization

## 🛠️ Tech Stack

- Frontend: React + Vite (client at http://localhost:3002)
- Backend: Django REST API (http://127.0.0.1:8000)
- Database: PostgreSQL
- Languages: TypeScript (frontend), Python (backend)

## 🏁 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.12+
- PostgreSQL (running locally or hosted)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/RENUGASREE/Python-Edition-Adaptive-and-Interactive-Learning-Assistant-.git
    cd Python-Edition-Adaptive-and-Interactive-Learning-Assistant-
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install
    ```

3.  **Backend setup (Django):**
    ```bash
    cd backend
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```
    The API runs at http://127.0.0.1:8000

4.  **Run frontend (Vite):**
    ```bash
    npx vite --port 3002
    ```
    Open http://localhost:3002 in your browser.

### Notes
- Registration requires a strong password (min 8 chars, uppercase, lowercase, number, special char).
- If you see 401 Unauthorized on `/api/auth/user`, it means you’re not logged in yet; this is expected before login/registration.

## 📦 Build for Production

Build the frontend:

```bash
npm run build
```
Start the Node server (optional, if using the Node API):
To start the production server:

```bash
npm start
## ☁️ Deployment
- Django API can be deployed to platforms supporting Python (Render, Railway).
- Frontend can be deployed to static hosts (Vercel, Netlify) or served by Node.
3.  Set the Start Command to: `npm start`
4.  Add your `DATABASE_URL` environment variable.

## 🤝 Contributing
