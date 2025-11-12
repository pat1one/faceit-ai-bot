#!/bin/bash
python /app/scripts/init_db.py
exec uvicorn src.server.main:app --host 0.0.0.0 --port 8000
