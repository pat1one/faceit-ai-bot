# 🚀 Быстрое развертывание на 79.174.93.21

## 1. Подключение к серверу
```bash
ssh root@79.174.93.21
```

## 2. Установка Docker (одной командой)
```bash
curl -fsSL https://get.docker.com | sh && \
systemctl enable docker && \
systemctl start docker && \
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
chmod +x /usr/local/bin/docker-compose
```

## 3. Клонирование и запуск
```bash
cd /opt && \
git clone https://github.com/pat1one/faceit-ai-bot.git && \
cd faceit-ai-bot && \
chmod +x deploy.sh && \
./deploy.sh
```

## 4. Настройка SSL (после настройки DNS)
```bash
# DNS должен указывать: A pattmsc.online -> 79.174.93.21
certbot certonly --standalone -d pattmsc.online -d www.pattmsc.online
```

## 5. Проверка
```bash
# Проверить статус
docker-compose -f docker-compose.prod.yml ps

# Проверить API
curl -k https://pattmsc.online/api/health

# Проверить сайт
curl -k https://pattmsc.online
```

## 🎯 Результат
- **Сайт:** https://pattmsc.online
- **API:** https://pattmsc.online/docs  
- **Мониторинг:** https://pattmsc.online/flower

## 📋 Полезные команды
```bash
# Логи
docker-compose -f docker-compose.prod.yml logs -f

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Обновление
git pull && ./deploy.sh
```

---

✅ **Готово!** После выполнения этих команд ваше приложение будет работать на pattmsc.online
