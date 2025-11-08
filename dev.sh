#!/bin/bash

set -e

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Faceit AI Bot - Режим разработки${NC}"
echo "=========================================="

# Проверка .env файла
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env файл не найден. Копирую из .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Отредактируйте .env файл при необходимости${NC}"
fi

# Определяем команду docker compose
if docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Запуск только базы данных
echo -e "${BLUE}🐘 Запуск PostgreSQL...${NC}"
$DOCKER_COMPOSE up -d db

echo -e "${YELLOW}⏳ Ожидание запуска базы данных...${NC}"
sleep 5

echo ""
echo -e "${GREEN}✨ База данных запущена!${NC}"
echo ""
echo -e "${BLUE}Теперь вы можете запустить:${NC}"
echo "  1. Backend API:  cd src/server && python main.py"
echo "  2. Frontend:     npm run dev"
echo ""
echo -e "${YELLOW}Или запустите оба сервиса автоматически:${NC}"
echo "  npm run dev (в одном терминале)"
echo "  python main.py (в другом терминале)"
echo ""
echo -e "${BLUE}💾 PostgreSQL доступна на:${NC} localhost:5432"
echo -e "${BLUE}📊 Credentials:${NC} faceit / faceit / faceit"
echo ""