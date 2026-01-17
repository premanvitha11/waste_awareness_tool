#!/bin/bash
# Windows Quick Start Script
# Run this in PowerShell or Git Bash

echo "=========================================="
echo "AI Waste Sorting Awareness Tool"
echo "Quick Start Setup (Windows)"
echo "=========================================="
echo ""

# Backend setup
echo "========== Setting up Backend =========="
cd backend

# Create virtual environment
if (!(Test-Path "venv")) {
    echo "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
echo "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if (!(Test-Path ".env")) {
    echo "Creating .env file..."
    Copy-Item ".env.example" ".env"
}

# Create directories
if (!(Test-Path "models")) { New-Item -ItemType Directory -Path "models" }
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" }

echo "✓ Backend setup complete"
echo ""

# Frontend setup
echo "========== Setting up Frontend =========="
cd ..\frontend

# Check and create .env
if (!(Test-Path ".env")) {
    echo "Creating .env file..."
    "REACT_APP_API_URL=http://localhost:5000" | Out-File -Encoding utf8 ".env"
}

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
echo "   cd backend"
echo "   .\venv\Scripts\Activate.ps1"
echo "   python app.py"
echo ""
echo "2. Terminal 2 - Start Frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "For Docker:"
echo "   docker-compose up --build"
echo ""
