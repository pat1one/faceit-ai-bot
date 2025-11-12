#!/bin/bash
# Production deployment script

set -e

echo "🚀 Starting deployment..."

# Variables
APP_DIR="/opt/faceit-ai-bot"
REPO_URL="https://github.com/pat1one/faceit-ai-bot.git"
BRANCH="main"

# Pull latest code
echo "📥 Pulling latest code..."
cd $APP_DIR
git fetch origin
git checkout $BRANCH
git pull origin $BRANCH

# Install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-api-only.txt

# Run migrations
echo "🗄️ Running database migrations..."
alembic upgrade head

# Restart services
echo "♻️ Restarting services..."
sudo systemctl restart faceit-api
sudo systemctl restart faceit-celery-worker
sudo systemctl restart faceit-celery-beat

# Check status
echo "✅ Checking service status..."
sudo systemctl status faceit-api --no-pager
sudo systemctl status faceit-celery-worker --no-pager

echo "🎉 Deployment completed!"
