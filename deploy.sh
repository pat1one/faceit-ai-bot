#!/bin/bash

# Собираем и запускаем сервисы
echo "🔨 Building services..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "✨ Services are ready:"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Grafana: http://localhost:3001 (admin/admin)"
echo "📈 Prometheus: http://localhost:9090"

echo "📝 Logs are available with: docker-compose logs -f"