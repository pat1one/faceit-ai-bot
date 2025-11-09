<div align="center">

# 🎮 Faceit Stats Bot

### Анализ статистики и поиск нормальных тиммейтов в CS2

[![CI/CD](https://github.com/pat1one/faceit-ai-bot/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/pat1one/faceit-ai-bot/actions/workflows/ci-cd.yml)
[![Tests](https://github.com/pat1one/faceit-ai-bot/actions/workflows/test.yml/badge.svg)](https://github.com/pat1one/faceit-ai-bot/actions/workflows/test.yml)
[![Deploy](https://github.com/pat1one/faceit-ai-bot/actions/workflows/deploy-to-vps.yml/badge.svg)](https://github.com/pat1one/faceit-ai-bot/actions/workflows/deploy-to-vps.yml)

[![Version](https://img.shields.io/github/v/release/pat1one/faceit-ai-bot?label=version)](https://github.com/pat1one/faceit-ai-bot/releases)
[![Downloads](https://img.shields.io/github/downloads/pat1one/faceit-ai-bot/total?label=downloads)](https://github.com/pat1one/faceit-ai-bot/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/next.js-15-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

[![Website](https://img.shields.io/badge/🌐-pattmsc.online-blue)](https://pattmsc.online)
[![Twitch](https://img.shields.io/badge/📺-Twitch-9146FF)](https://www.twitch.tv/pattmsc)
[![Telegram](https://img.shields.io/badge/💬-Telegram-26A5E4)](https://t.me/mscpatt)

---

[🌐 **Демо**](https://pattmsc.online) • [📚 **API Docs**](https://api.pattmsc.online/docs) • [⬇️ **Скачать**](DOWNLOAD.md) • [🗺️ **Roadmap**](ROADMAP.md)

**Автор:** [pattmsc](https://taplink.cc/mscpat)

</div>

---

## ✨ Возможности

<table>
<tr>
<td width="33%" align="center">

### 📊 Анализ статистики

Детальный анализ матчей<br/>
Отслеживание прогресса<br/>
Сравнение с другими игроками

</td>
<td width="33%" align="center">

### 👥 Поиск тиммейтов

Умные фильтры поиска<br/>
Статистика игроков<br/>
Удобная коммуникация

</td>
<td width="33%" align="center">

### 🔔 Уведомления

Новые матчи<br/>
Обновления статистики<br/>
Интеграция с Faceit

</td>
</tr>
</table>

## 🚀 Быстрый старт

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/pat1one/faceit-ai-bot.git
cd faceit-ai-bot

# Настроить окружение
cp .env.example .env
# Отредактируйте .env файл

# Запустить через Docker
docker-compose up -d
```

### 🌐 Доступные сервисы

После запуска доступны:

| Сервис | URL | Описание |
|--------|-----|----------|
| 🎨 Frontend | http://localhost:3000 | Web интерфейс |
| ⚡ API | http://localhost:8000 | Backend API |
| 📖 API Docs | http://localhost:8000/docs | Swagger документация |
| 🗄️ PostgreSQL | localhost:5432 | База данных |

## 📦 Скачать

<table>
<tr>
<td width="33%" align="center">

### 🧩 Расширение

**Для браузера**

Легкая интеграция с Faceit  
Анализ прямо на сайте  
Быстрый доступ к статистике

[![Chrome](https://img.shields.io/badge/Chrome-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)](https://github.com/pat1one/faceit-ai-bot/releases/latest)
[![Firefox](https://img.shields.io/badge/Firefox-FF7139?style=for-the-badge&logo=firefox&logoColor=white)](https://github.com/pat1one/faceit-ai-bot/releases/latest)
[![Edge](https://img.shields.io/badge/Edge-0078D7?style=for-the-badge&logo=microsoft-edge&logoColor=white)](https://github.com/pat1one/faceit-ai-bot/releases/latest)

[📖 Инструкция](DOWNLOAD.md#-расширение-для-браузера)

</td>
<td width="33%" align="center">

### 🌐 Веб-версия

**Онлайн сервис**

Все функции в одном месте  
Работает без установки  
Доступ с любого устройства

[![Website](https://img.shields.io/badge/Открыть-pattmsc.online-4CAF50?style=for-the-badge&logo=google-chrome&logoColor=white)](https://pattmsc.online)

[![API Docs](https://img.shields.io/badge/API-Документация-009688?style=for-the-badge&logo=swagger&logoColor=white)](https://api.pattmsc.online/docs)

</td>
<td width="33%" align="center">

### 🐳 Docker

**Для разработчиков**

Полная локальная установка  
Все сервисы в контейнерах  
Готово к продакшену

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://github.com/pat1one/faceit-ai-bot/releases/latest)

[📖 Инструкция](DOWNLOAD.md#-веб-приложение)

</td>
</tr>
</table>

<div align="center">

**📥 [Все релизы на GitHub](https://github.com/pat1one/faceit-ai-bot/releases)**

</div>

### 💻 Для разработчиков

Локальная установка через Docker:

```bash
# Клонировать репозиторий
git clone https://github.com/pat1one/faceit-ai-bot.git
cd faceit-ai-bot

# Настроить окружение
cp .env.example .env

# Запустить
docker-compose up -d
```

## 🛠️ Технологии

<table>
<tr>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg" width="48" height="48" alt="Next.js"/>
<br><strong>Next.js 15</strong>
<br>React 19
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="48" height="48" alt="FastAPI"/>
<br><strong>FastAPI</strong>
<br>Python 3.9+
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="48" height="48" alt="PostgreSQL"/>
<br><strong>PostgreSQL</strong>
<br>Database
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="48" height="48" alt="Docker"/>
<br><strong>Docker</strong>
<br>Deployment
</td>
</tr>
</table>

## 🔧 Основные команды

```bash
docker-compose up -d        # 🚀 Запустить все сервисы
docker-compose down         # ⏹️ Остановить сервисы
docker-compose logs -f      # 📝 Показать логи
docker-compose restart      # 🔄 Перезапустить
docker-compose ps           # 📊 Статус сервисов
```

## 📁 Структура проекта

```text
faceit-ai-bot/
├── 📱 app/                 # Next.js приложение
├── ⚙️ src/                 # Backend + Browser Extension
│   ├── api/               # FastAPI endpoints
│   ├── ai/                # ML модели
│   └── services/          # Бизнес-логика
├── 🎨 public/             # Статические файлы
├── 🐳 docker-compose.yml  # Оркестрация сервисов
└── 📚 docs/               # Документация
```

## 📖 Документация

| Документ | Описание |
|----------|----------|
| 🗺️ [ROADMAP.md](ROADMAP.md) | План развития проекта |
| ⬇️ [DOWNLOAD.md](DOWNLOAD.md) | Скачать расширение и приложение |
| 📜 [LICENSE](LICENSE) | Лицензия ([Русская версия](LICENSE.ru.md)) |

## 🎯 Как использовать

1. **Установка** - Скачайте расширение или разверните полную версию
2. **Авторизация** - Войдите через Faceit аккаунт
3. **Анализ** - Начните анализировать статистику и искать тиммейтов

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта!

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'добавил крутую фичу'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

**MIT (но с нюансами по деньгам)**

**Copyright © 2025 pattmsc (Platon)**

Короче, это платный сервис с подписками (FREE, BASIC, PRO, ELITE).

Можно:
- ✅ Форкать и менять для себя или учёбы
- ✅ Использовать в своих некоммерческих проектах
- ✅ Встраивать в свой продукт

Нельзя:
- ❌ Делать свой платный сервис на этом коде
- ❌ Продавать подписки
- ❌ Зарабатывать без разрешения
- ❌ Вырезать систему оплаты

Официальный сервис: https://pattmsc.online

Подробнее: [LICENSE](LICENSE) ([по-русски](LICENSE.ru.md))

---

<div align="center">

**Сделано с ❤️ для CS2 комьюнити**

### 💝 Поддержать проект

[⭐ Star на GitHub](https://github.com/pat1one/faceit-ai-bot) • [💰 Донат](https://taplink.cc/mscpat) • [📺 Twitch](https://www.twitch.tv/pattmsc) • [💬 Telegram](https://t.me/mscpatt)

[🐛 Сообщить об ошибке](https://github.com/pat1one/faceit-ai-bot/issues) • [💡 Предложить функцию](https://github.com/pat1one/faceit-ai-bot/issues)

---

**Если проект помог - поставь ⭐ звезду и расскажи друзьям!**

</div>
