#!/bin/bash
# Скрипт очистки сервера для экономии места

echo "🧹 Начинаем очистку сервера..."

# Проверка места до очистки
echo "📊 Место до очистки:"
df -h /

echo "🐳 Очистка Docker..."
docker system prune -af --volumes
docker image prune -af

echo "📝 Очистка логов..."
sudo journalctl --vacuum-time=3d
sudo find /var/log -name "*.log" -type f -mtime +3 -delete 2>/dev/null

echo "📦 Очистка пакетов..."
sudo apt clean
sudo apt autoremove -y

echo "🗑️ Очистка временных файлов..."
sudo rm -rf /tmp/* 2>/dev/null
sudo rm -rf /var/tmp/* 2>/dev/null

echo "📊 Место после очистки:"
df -h /

echo "✅ Очистка завершена!"

# Показать самые большие папки
echo "📁 Самые большие папки:"
du -sh /* 2>/dev/null | sort -hr | head -5
