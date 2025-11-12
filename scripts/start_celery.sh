#!/bin/bash
# Start Celery worker and beat scheduler

# Activate virtual environment if needed
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start Celery worker in background
celery -A src.server.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --queues=demo_analysis,notifications,webhooks \
    --logfile=logs/celery_worker.log \
    --pidfile=logs/celery_worker.pid \
    --detach

echo "Celery worker started"

# Start Celery beat scheduler in background
celery -A src.server.celery_app beat \
    --loglevel=info \
    --logfile=logs/celery_beat.log \
    --pidfile=logs/celery_beat.pid \
    --detach

echo "Celery beat started"

# Start Flower monitoring (optional)
celery -A src.server.celery_app flower \
    --port=5555 \
    --broker=redis://localhost:6379/0 \
    &

echo "Flower monitoring started on http://localhost:5555"
echo "All Celery services started successfully!"
