#!/bin/bash

# Скрипт восстановления из бэкапа

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_date>"
    echo "Example: ./restore.sh 20241110_230000"
    exit 1
fi

BACKUP_DIR="/backups"
BACKUP_DATE=$1
DB_NAME="faceit"
DB_USER="faceit"

echo "Starting restore from $BACKUP_DATE..."

# Проверить что бэкапы существуют
DB_BACKUP="$BACKUP_DIR/db_$BACKUP_DATE.sql.gz"
REDIS_BACKUP="$BACKUP_DIR/redis_$BACKUP_DATE.rdb"

if [ ! -f "$DB_BACKUP" ]; then
    echo "Error: Database backup not found: $DB_BACKUP"
    exit 1
fi

if [ ! -f "$REDIS_BACKUP" ]; then
    echo "Error: Redis backup not found: $REDIS_BACKUP"
    exit 1
fi

# Остановить сервисы
echo "Stopping services..."
docker compose down

# Восстановить PostgreSQL
echo "Restoring PostgreSQL..."
gunzip < $DB_BACKUP | PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER $DB_NAME

# Восстановить Redis
echo "Restoring Redis..."
cp $REDIS_BACKUP /var/lib/redis/dump.rdb

# Запустить сервисы
echo "Starting services..."
docker compose up -d

echo "Restore completed successfully!"
