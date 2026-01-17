#!/bin/bash
# Quick Start Script for AI Waste Sorting Awareness Tool
# Run this script to set up and start both frontend and backend

set -e  # Exit on error

echo "=========================================="
echo "AI Waste Sorting Awareness Tool"
echo "Quick Start Setup"
echo "=========================================="
echo ""

# Check for Python and Node.js
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 14+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo "✓ Node.js found: $(node --version)"
echo ""

# Backend setup
echo "========== Setting up Backend =========="
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Create directories
mkdir -p models logs

echo "✓ Backend setup complete"
echo ""

# Frontend setup
echo "========== Setting up Frontend =========="
cd ../frontend

# Check and create .env
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "REACT_APP_API_URL=http://localhost:5000" > .env
fi

# Install dependencies
echo "Installing Node dependencies..."
npm install

echo "✓ Frontend setup complete"
echo ""

echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Terminal 1 - Start Backend:"
echo "   cd backend && source venv/bin/activate && python app.py"
echo ""
echo "2. Terminal 2 - Start Frontend:"
echo "   cd frontend && npm start"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "For Docker:"
echo "   docker-compose up --build"
echo ""
