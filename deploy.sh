#!/bin/bash

# Production deployment script for Faceit AI Bot
# Run this on your production server

set -e

echo "🚀 Starting Faceit AI Bot deployment..."

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Copy production environment file
echo "⚙️ Setting up environment..."
cp .env.production .env

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Test API
echo "🧪 Testing API..."
if curl -f http://localhost/api/health; then
    echo "✅ API is healthy!"
else
    echo "❌ API health check failed"
    exit 1
fi

# Test web
echo "🧪 Testing web..."
if curl -f http://localhost; then
    echo "✅ Web is healthy!"
else
    echo "❌ Web health check failed"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "🌐 Your site is available at: https://pattmsc.online"
echo "📊 Flower monitoring: https://pattmsc.online:5555"
echo "📋 Logs: docker-compose -f docker-compose.prod.yml logs -f"
