#!/bin/bash

# Проверяем, установлен ли gh CLI
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) не установлен. Установка..."
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update
    sudo apt install gh -y
fi

# Проверяем авторизацию в GitHub
if ! gh auth status &> /dev/null; then
    echo "Требуется авторизация в GitHub..."
    gh auth login
fi

# Получаем текущий репозиторий
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

echo "Добавление секретов в репозиторий $REPO"

# Запрашиваем данные Docker Hub
read -p "Введите ваш логин Docker Hub: " DOCKER_USERNAME
read -s -p "Введите ваш пароль/токен Docker Hub: " DOCKER_PASSWORD
echo

# Добавляем секреты
echo "Добавление DOCKER_USERNAME..."
echo "$DOCKER_USERNAME" | gh secret set DOCKER_USERNAME -R "$REPO"

echo "Добавление DOCKER_PASSWORD..."
echo "$DOCKER_PASSWORD" | gh secret set DOCKER_PASSWORD -R "$REPO"

echo "Секреты успешно добавлены!"

# Проверяем настройки Actions
gh api repos/"$REPO"/actions/permissions --jq .enabled