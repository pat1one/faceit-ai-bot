#!/bin/bash

# Faceit AI Bot - Start All Services
echo "🚀 Starting Faceit AI Bot services..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python first."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm run install:all
fi

if [ ! -d "apps/ai/venv" ] && [ ! -f "apps/ai/.venv" ]; then
    echo "🐍 Installing Python dependencies..."
    cd apps/ai
    pip install -r requirements.txt
    cd ../..
fi

echo "✅ Dependencies ready!"
echo ""

# Start all services with concurrently
echo "🌟 Starting all services (Frontend + Backend + AI)..."
echo "📱 Frontend will be available at: http://localhost:5000"
echo "🔧 Backend API at: http://localhost:4000" 
echo "🤖 AI Service at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

npm run dev:fullstack