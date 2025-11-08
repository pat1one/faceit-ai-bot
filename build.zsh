#!/usr/bin/env zsh
# Build script for Zsh

echo "🏗️ Building Faceit AI Bot..."

# Build backend
echo "📦 Building Python backend..."
pip install -r requirements.txt

# Build frontend
echo "🎨 Building Next.js frontend..."
npm install
npm run build

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "Next steps:"
echo "  - Run 'make deploy' or './deploy.sh' to start services"
echo "  - Run 'make dev' or './dev.sh' for development mode"
