@echo off
REM Quick setup script for Python Edition development environment (Windows)
REM Run this script after cloning the repository

echo.
echo ==========================================
echo Python Edition - Development Setup
echo ==========================================
echo.

REM Check prerequisites
echo Checking prerequisites...
python --version >nul 2>&1 || (echo Python 3.10+ required & exit /b 1)
node --version >nul 2>&1 || (echo Node.js 18+ required & exit /b 1)
git --version >nul 2>&1 || (echo Git required & exit /b 1)
echo [OK] All prerequisites met
echo.

REM Setup Backend
echo Setting up Backend...
cd backend
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..
echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo Setting up Frontend...
cd frontend
call npm install --legacy-peer-deps
cd ..
echo [OK] Frontend setup complete
echo.

REM Instructions
echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start development:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   .venv\Scripts\activate
echo   python -m uvicorn app.main:app --reload --port 8000
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:3000 in your browser
echo.
echo API Documentation: http://localhost:8000/docs
echo.
pause
