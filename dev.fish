#!/usr/bin/env fish
# Development mode startup script for Fish shell

echo "🚀 Starting development environment..."

# Check if Docker is running
if not docker info > /dev/null 2>&1
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
end

# Start services
echo "📦 Starting services with docker-compose..."
docker-compose up -d postgres

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
sleep 3

# Start API in development mode
echo "🔧 Starting FastAPI in development mode..."
set -x PYTHONPATH (pwd)
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Start Next.js in development mode
echo "🎨 Starting Next.js in development mode..."
npm run dev &

echo ""
echo "✅ Development environment is ready!"
echo ""
echo "Services:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
read -P ""
