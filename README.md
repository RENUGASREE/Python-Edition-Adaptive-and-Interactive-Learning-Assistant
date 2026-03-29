# Python Edition: Adaptive Learning Platform 🐍

A premium, AI-enhanced adaptive learning platform designed to take users from Python basics to professional mastery. The platform features a sophisticated recommendation engine, real-time code execution, and high-fidelity analytics.

![Project Preview](https://via.placeholder.com/800x400/1e293b/ffffff?text=Python+Edition+Adaptive+Learning)

---

## 🚀 Key Features

### 🧠 Adaptive Learning Engine
- **Diagnostic Placement**: A comprehensive 15-question quiz to assess baseline knowledge across 6 core modules.
- **Mastery-Based Progression**: Intelligent backend logic that tracks proficiency (0.0 - 1.0) and unlocks content dynamically.
- **Personalized Recommendations**: Automatic difficulty adjustment (Beginner, Intermediate, Pro) for every module based on user performance.

### 📚 Professional Curriculum
- **60 Deep-Dive Topics**: Covering everything from Variable Scope to Decorators and Context Managers.
- **180+ Lessons**: Each topic contains progressive lessons (Objective, Concept, Example, Takeaway).
- **Interactive Challenges**: 60 integrated coding challenges with an auto-grading sandbox.

### 📊 Performance Analytics
- **Topic Proficiency Radar**: Visual mastery breakdown across the curriculum.
- **Real-time Progress Tracking**: Granular tracking of lesson completion and quiz scores.
- **Mastery Vector Visualization**: Deep insights into the learner's knowledge profile.

### 🛠️ Developer Suite
- **Interactive IDE**: Integrated code editor with instant feedback and error diagnostics.
- **RAG-Powered Chatbot**: AI assistant trained on the curriculum for context-aware help.

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion, Recharts.
- **Backend**: Django 5.0, Django REST Framework, PostgreSQL.
- **AI/ML**: OpenAI GPT-4o (via RAG) for intelligent tutoring.
- **Execution**: Isolated sandbox for secure Python code evaluation.

---

## 🏁 Quick Start

### 1. Prerequisites
- Node.js 18+
- Python 3.12+
- PostgreSQL

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
# Activate venv: .\.venv\Scripts\activate (Windows) or source .venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
*API runs at http://127.0.0.1:8000*

### 3. Frontend Setup
```bash
cd client
npm install
npm run dev -- --port 3002
```
*Frontend runs at http://localhost:3002*

---

## 📦 Project Structure
- `backend/`: Django core, adaptive logic, and curriculum data.
- `client/`: React application, UI components, and state management.
- `assessments/`: Data models for quizzes and placement tests.
- `evaluation/`: Logic for the adaptive recommendation engine.

---

## 🤝 Contributing
Contributions are welcome! Please read the `CONTRIBUTING.md` for our code of conduct and the process for submitting pull requests.

## 📄 License
This project is licensed under the MIT License - see the `LICENSE` file for details.
