# Python Edition: Adaptive & Interactive Learning Assistant 🐍

A premium, AI-enhanced adaptive learning platform designed to take users from Python basics to professional mastery. The platform features a sophisticated recommendation engine, real-time code execution, and high-fidelity analytics.

---

## 🚀 Key Features

### 🧠 Adaptive Learning Engine
- **Diagnostic Placement**: A comprehensive 15-question quiz to assess baseline knowledge across 6 core modules.
- **Mastery-Based Progression**: Intelligent backend logic that tracks proficiency (0.0 – 1.0) and unlocks content dynamically.
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

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion, Recharts |
| **Backend** | Django 5.0, Django REST Framework, PostgreSQL |
| **AI / ML** | OpenAI GPT-4o (via RAG) for intelligent tutoring |
| **Execution** | Isolated sandbox for secure Python code evaluation |

---

## 📦 Project Structure

```
Python_Edition/
├── backend/            # Django core, adaptive logic, and curriculum data
│   ├── ai_engine/      # RAG-powered AI tutoring engine
│   ├── analytics/      # Performance tracking and analytics
│   ├── assessments/    # Quizzes, placement tests, and challenges
│   ├── core/           # Shared models and utilities
│   ├── evaluation/     # Adaptive recommendation engine
│   ├── gamification/   # Badges, streaks, and rewards
│   ├── lessons/        # Lesson content management
│   ├── recommendation/ # Personalized learning path suggestions
│   └── users/          # User authentication and profiles
├── client/             # React frontend application
│   ├── public/         # Static assets
│   └── src/            # Components, pages, hooks, and state management
```

---

## 🏁 Prerequisites

- **Node.js** 18+
- **Python** 3.12+
- **PostgreSQL**

---

## 📄 License

This project is licensed under the MIT License.
