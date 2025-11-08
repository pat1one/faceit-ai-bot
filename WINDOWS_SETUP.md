# 🪟 Установка на Windows

Руководство по установке и запуску Faceit AI Bot на Windows.

## 📋 Требования

- Windows 10/11
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js 18+](https://nodejs.org/)
- [Python 3.9+](https://www.python.org/)
- Git

## 🛠️ Выбор оболочки

На Windows вы можете использовать разные оболочки для запуска скриптов:

### Вариант 1: PowerShell (рекомендуется для Windows)

PowerShell установлен по умолчанию в Windows 10/11.

```powershell
# Проверка версии
$PSVersionTable.PSVersion

# Разрешить выполнение скриптов (от администратора)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Вариант 2: Git Bash

Устанавливается вместе с [Git for Windows](https://git-scm.com/download/win).

```bash
# Использовать .sh скрипты
./build.sh
./deploy.sh
./dev.sh
```

### Вариант 3: WSL (Windows Subsystem for Linux)

Полноценный Linux в Windows.

```bash
# Установка WSL
wsl --install

# После установки используйте .sh скрипты
./build.sh
./deploy.sh
```

### Вариант 4: Zsh (Z Shell)

Мощная оболочка с плагинами и темами.

```bash
# Установка через WSL
sudo apt install zsh

# Установить Oh My Zsh (опционально)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Использовать .zsh скрипты
./build.zsh
./deploy.zsh
./dev.zsh
```

### Вариант 5: Fish Shell

Современная оболочка с автодополнением.

```bash
# Установка через WSL
sudo apt install fish

# Использовать .fish скрипты
./build.fish
./deploy.fish
./dev.fish
```

## 🚀 Быстрый старт

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/pat1one/faceit-ai-bot.git
cd faceit-ai-bot
```

### Шаг 2: Настройка окружения

```bash
# Копировать пример конфигурации
copy .env.example .env

# Отредактировать .env в любом текстовом редакторе
notepad .env
```

### Шаг 3: Установка зависимостей

**PowerShell:**
```powershell
# Установить Node.js зависимости
npm install

# Установить Python зависимости
pip install -r requirements.txt
```

**Bash/Fish:**
```bash
./build.sh
# или
./build.fish
```

### Шаг 4: Запуск

**PowerShell:**
```powershell
# Запустить Docker Desktop сначала!

# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

**Bash:**
```bash
./deploy.sh
```

**Fish:**
```fish
./deploy.fish
```

## 🔧 Режим разработки

### PowerShell

```powershell
# Запустить PostgreSQL
docker-compose up -d postgres

# В одном терминале - Backend
$env:PYTHONPATH = (Get-Location).Path
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# В другом терминале - Frontend
npm run dev
```

### Bash/Fish

```bash
./dev.sh
# или
./dev.fish
```

## 📦 Доступные команды

### Make (если установлен)

```bash
make help          # Показать все команды
make install       # Установить зависимости
make build         # Собрать проект
make deploy        # Запустить все сервисы
make dev           # Режим разработки
make logs          # Показать логи
make stop          # Остановить сервисы
make clean         # Очистить временные файлы
```

### Docker Compose

```bash
docker-compose up -d              # Запустить все сервисы
docker-compose down               # Остановить все сервисы
docker-compose logs -f            # Показать логи
docker-compose ps                 # Статус сервисов
docker-compose restart            # Перезапустить
docker-compose build              # Пересобрать образы
```

## 🐛 Решение проблем

### Docker Desktop не запускается

1. Включите виртуализацию в BIOS
2. Включите WSL 2:
   ```powershell
   wsl --install
   wsl --set-default-version 2
   ```
3. Перезагрузите компьютер

### Порты уже заняты

```powershell
# Проверить какой процесс использует порт
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Убить процесс (замените PID на номер из предыдущей команды)
taskkill /PID <PID> /F
```

### Python не найден

```powershell
# Добавить Python в PATH
# Панель управления → Система → Дополнительные параметры системы
# → Переменные среды → Path → Добавить путь к Python
```

### npm не найден

```powershell
# Установить Node.js с официального сайта
# https://nodejs.org/

# Проверить установку
node --version
npm --version
```

### Ошибки прав доступа

```powershell
# Запустить PowerShell от администратора
# Правый клик на PowerShell → Запуск от имени администратора
```

## 🔒 Безопасность

### Настройка .env

Никогда не коммитьте `.env` файл в Git!

```bash
# .env уже в .gitignore
# Проверить:
git status
```

### Генерация секретных ключей

```powershell
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

```bash
# Bash
openssl rand -hex 32
```

## 📚 Дополнительные ресурсы

- [Docker Desktop для Windows](https://docs.docker.com/desktop/install/windows-install/)
- [WSL документация](https://docs.microsoft.com/en-us/windows/wsl/)
- [Git for Windows](https://gitforwindows.org/)
- [Node.js установка](https://nodejs.org/en/download/)
- [Python для Windows](https://www.python.org/downloads/windows/)

## 💡 Советы

1. **Используйте WSL** для лучшей совместимости с Linux-инструментами
2. **Docker Desktop** должен быть запущен перед выполнением команд
3. **Антивирус** может блокировать Docker - добавьте в исключения
4. **Firewall** может блокировать порты - разрешите доступ
5. **Обновляйте** Docker Desktop и Node.js регулярно

## 🆘 Помощь

Если возникли проблемы:

- 📖 [Документация проекта](README.md)
- 🐛 [Сообщить об ошибке](https://github.com/pat1one/faceit-ai-bot/issues)
- 💬 [Обсуждения](https://github.com/pat1one/faceit-ai-bot/discussions)
- 📧 Email: [support@pattmsc.online](mailto:support@pattmsc.online)

---

<div align="center">

**Успешной работы! 🚀**

[⬅️ Назад к README](README.md)

</div>
