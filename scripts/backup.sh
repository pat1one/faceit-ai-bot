#!/bin/bash

# Скрипт резервного копирования БД

set -e

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="faceit"
DB_USER="faceit"

echo "Starting backup at $DATE..."

# Создать директорию для бэкапов
mkdir -p $BACKUP_DIR

# Бэкап PostgreSQL
echo "Backing up PostgreSQL..."
PGPASSWORD=$DB_PASSWORD pg_dump -h localhost -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Бэкап Redis
echo "Backing up Redis..."
redis-cli SAVE
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Удалить старые бэкапы (старше 30 дней)
echo "Cleaning old backups..."
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete
find $BACKUP_DIR -name "redis_*.rdb" -mtime +30 -delete

echo "Backup completed successfully!"
echo "Database backup: $BACKUP_DIR/db_$DATE.sql.gz"
echo "Redis backup: $BACKUP_DIR/redis_$DATE.rdb"
