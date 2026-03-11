#!/bin/bash
# Quick setup script for Python Edition development environment
# Run this script after cloning the repository

echo "=========================================="
echo "Python Edition - Development Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
python --version > /dev/null 2>&1 || { echo "Python 3.10+ required"; exit 1; }
node --version > /dev/null 2>&1 || { echo "Node.js 18+ required"; exit 1; }
git --version > /dev/null 2>&1 || { echo "Git required"; exit 1; }
echo "✓ All prerequisites met"
echo ""

# Setup Backend
echo "Setting up Backend..."
cd backend
python -m venv .venv
source .venv/Scripts/activate  # On Windows, use: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
echo "✓ Backend setup complete"
echo ""

# Setup Frontend
echo "Setting up Frontend..."
cd ../frontend
npm install --legacy-peer-deps
echo "✓ Frontend setup complete"
echo ""

# Instructions
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start development:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source .venv/Scripts/activate"
echo "  python -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
