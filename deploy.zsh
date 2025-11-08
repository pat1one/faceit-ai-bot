#!/usr/bin/env zsh
# Deployment script for Zsh

echo "🚀 Deploying Faceit AI Bot..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env exists
if [[ ! -f .env ]]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
    exit 1
fi

# Stop existing containers
echo "⏹️  Stopping existing containers..."
docker-compose down

# Start all services
echo "🐳 Starting all services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo ""
echo "✅ Deployment completed!"
echo ""
echo "Services are running:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - PostgreSQL: localhost:5432"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart"
