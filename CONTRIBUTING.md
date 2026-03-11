# Contributing to Python Edition

Thank you for contributing to **Python Edition: Adaptive and Interactive Learning Assistant**! This guide helps team members set up the project and contribute effectively.

## Project Overview

Python Edition is an AI-powered, adaptive Python learning platform with:
- **Frontend:** React + Tailwind CSS (modern, responsive UI)
- **Backend:** FastAPI (REST APIs for all learning features)
- **AI Layer:** RAG chatbot, knowledge tracing, auto-grader
- **Database:** PostgreSQL (production) / SQLite (dev)

## Setup Instructions

### Prerequisites
- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (for version control)
- **Docker** (optional, for sandbox grading and production)

### 1. Clone the Repository
```bash
git clone https://github.com/RENUGASREE/Python-Edition-Adaptive-and-Interactive-Learning-Assistant-.git
cd Python-Edition-Adaptive-and-Interactive-Learning-Assistant-
```

### 2. Setup Backend

```powershell
# Windows PowerShell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Setup Frontend

```powershell
# In another terminal
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 4. Run Both Servers

Use separate terminals or terminal tabs:
1. **Terminal 1 (Backend):** `python -m uvicorn app.main:app --reload --port 8000`
2. **Terminal 2 (Frontend):** `npm run dev`

Then open `http://localhost:3000` in your browser.

## Project Structure

```
python_edition/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── api/               # API route handlers
│   │   │   ├── auth.py        # Authentication (login, register)
│   │   │   ├── profile.py     # User profile management
│   │   │   ├── recommend.py   # Adaptive recommendations
│   │   │   ├── grade.py       # Auto-grader endpoint
│   │   │   └── chat.py        # RAG chatbot
│   │   ├── models.py          # SQLAlchemy DB models
│   │   ├── schemas.py         # Pydantic request/response schemas
│   │   ├── database.py        # Database configuration
│   │   └── main.py            # FastAPI app initialization
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Container image
│
├── frontend/                   # React + Vite application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Lessons.jsx
│   │   │   ├── Quiz.jsx
│   │   │   ├── IDE.jsx
│   │   │   ├── Chatbot.jsx
│   │   │   └── Certificates.jsx
│   │   ├── api.js             # API client (axios)
│   │   ├── App.jsx            # Main app component
│   │   ├── App.css            # Tailwind + global styles
│   │   └── main.jsx           # React entry point
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS config
│   └── index.html             # HTML entry point
│
├── ai/                         # AI/ML features (WIP)
│   ├── index_docs.py          # Document indexing for RAG
│   ├── rag_service.py         # RAG retrieval pipeline
│   └── notebooks/             # Jupyter notebooks for experiments
│
├── infra/                      # Infrastructure & deployment
│   ├── docker-compose.yml     # Multi-container setup (Postgres + Backend)
│   └── k8s/                   # Kubernetes manifests (optional)
│
├── docs/                       # Documentation
│   ├── architecture.md        # System design
│   ├── api.md                 # API documentation
│   └── deployment.md          # Deployment guide
│
└── README.md                  # Project overview
```

## Key Endpoints (Backend)

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login (returns JWT token)

### Profile
- `GET /profile/{user_id}` - Get user profile

### Recommendations
- `POST /recommend/next` - Get personalized next topics

### Grading
- `POST /grade/run` - Submit code for grading

### Chat
- `POST /chat/query` - Query the RAG chatbot

### Health
- `GET /health` - Server health check

Full API docs: `http://localhost:8000/docs` (Swagger UI)

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# e.g., feature/knowledge-tracing, feature/gamification
```

### 2. Make Changes
- Write code following the existing style
- Add tests if applicable
- Update documentation

### 3. Commit Changes
```bash
git add .
git commit -m "Description of changes"
# Use clear, descriptive commit messages
```

### 4. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a PR on GitHub for code review.

### 5. Code Review & Merge
- Address feedback from reviewers
- Ensure all tests pass
- Merge to `main` when approved

## Tech Stack

### Frontend
- **React 18** - UI components
- **Vite** - Fast build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **JWT** - Authentication

### Database
- **PostgreSQL** (production)
- **SQLite** (development)

### Deployment (Future)
- **Docker** - Containerization
- **Kubernetes** / **Railway** / **Render** - Hosting

## Common Tasks

### Run Tests
```bash
cd backend
python -m pytest
```

### Build Frontend for Production
```bash
cd frontend
npm run build
# Output in dist/
```

### Format Code
```bash
# Backend (Python)
black backend/app

# Frontend (JavaScript)
cd frontend && npm run format
```

### Update Dependencies
```bash
# Backend
cd backend && pip install -r requirements.txt --upgrade

# Frontend
cd frontend && npm update
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed
- Check if port 8000 is already in use
- Verify all dependencies in requirements.txt

### Frontend shows blank page
- Open DevTools (F12) and check console for errors
- Ensure backend is running on port 8000
- Clear browser cache and hard refresh (Ctrl+Shift+R)

### Database errors
- Delete `dev.db` (SQLite) and restart backend
- Run migrations if using PostgreSQL

### CORS errors
- Backend CORS is configured for `http://localhost:3000`
- Update `app/main.py` if frontend runs on different port

## Project Phases (Milestones)

### Phase 1 (Current): MVP
- ✅ Basic scaffolding
- ✅ Frontend UI with Tailwind
- ✅ Backend REST APIs (stubs)
- 🔄 Auto-grader sandbox
- 🔄 Knowledge tracing

### Phase 2: AI Features
- RAG chatbot with semantic search
- Adaptive recommendation engine
- Code plagiarism detection

### Phase 3: Gamification & Engagement
- Badges and streaks system
- Leaderboards
- Certificate generation with QR codes

### Phase 4: Analytics & Admin
- Learner progress analytics
- Admin dashboard
- Content management system

### Phase 5: Production Deployment
- Docker & Kubernetes setup
- CI/CD pipelines
- Monitoring & logging
- Security hardening

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8
- Use type hints
- Docstrings for functions and classes
- Meaningful variable names

### JavaScript (Frontend)
- Use ES6+ syntax
- Functional components with hooks
- Clear prop names
- Comments for complex logic

## Questions or Issues?

- Create an **Issue** on GitHub for bugs or feature requests
- Discuss in **Discussions** tab for general questions
- Contact the maintainer directly for urgent matters

## License

This project is private and proprietary. All contributors must sign a CLA.

---

Happy coding! 🚀
