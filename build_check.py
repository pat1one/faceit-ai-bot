#!/usr/bin/env python3
"""
Скрипт проверки готовности проекта к сборке
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Проверка существования файла"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - НЕ НАЙДЕН")
        return False

def check_directory_exists(dirpath, description):
    """Проверка существования директории"""
    if Path(dirpath).exists() and Path(dirpath).is_dir():
        files = list(Path(dirpath).iterdir())
        print(f"✅ {description}: {dirpath} ({len(files)} файлов)")
        return True
    else:
        print(f"❌ {description}: {dirpath} - НЕ НАЙДЕН")
        return False

def main():
    print("=" * 60)
    print("🔍 ПРОВЕРКА ГОТОВНОСТИ ПРОЕКТА К СБОРКЕ")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # Проверка основных файлов
    print("📁 Проверка основных файлов:")
    print("-" * 60)
    
    required_files = [
        ("package.json", "Конфигурация npm"),
        ("requirements.txt", "Зависимости Python"),
        ("pytest.ini", "Конфигурация pytest"),
        ("Dockerfile", "Docker образ"),
        ("docker-compose.yml", "Docker Compose"),
        ("Makefile", "Makefile для сборки"),
        (".github/workflows/test.yml", "CI/CD workflow"),
    ]
    
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            errors.append(f"Отсутствует файл: {filepath}")
    
    print()
    
    # Проверка структуры проекта
    print("📂 Проверка структуры проекта:")
    print("-" * 60)
    
    required_dirs = [
        ("src/server", "Backend сервер"),
        ("src/server/features", "Модули функций"),
        ("src/server/models", "Модели БД"),
        ("src/config", "Конфигурация"),
        ("app", "Next.js приложение"),
        ("tests/unit", "Unit тесты"),
        ("tests/integration", "Integration тесты"),
    ]
    
    for dirpath, description in required_dirs:
        if not check_directory_exists(dirpath, description):
            warnings.append(f"Отсутствует директория: {dirpath}")
    
    print()
    
    # Проверка критичных файлов
    print("🔧 Проверка критичных файлов:")
    print("-" * 60)
    
    critical_files = [
        ("src/server/main.py", "Главный файл приложения"),
        ("src/server/config/settings.py", "Настройки"),
        ("src/server/exceptions.py", "Обработка ошибок"),
        ("src/server/database.py", "База данных"),
        ("src/config/api.ts", "Конфигурация API"),
        ("tests/conftest.py", "Фикстуры тестов"),
    ]
    
    for filepath, description in critical_files:
        if not check_file_exists(filepath, description):
            errors.append(f"Отсутствует критичный файл: {filepath}")
    
    print()
    
    # Проверка роутов
    print("🛣️  Проверка роутов:")
    print("-" * 60)
    
    routes = [
        ("src/server/features/demo_analyzer/routes.py", "Demo анализ"),
        ("src/server/features/payments/routes.py", "Платежи"),
        ("src/server/features/subscriptions/routes.py", "Подписки"),
        ("src/server/features/teammates/routes.py", "Тиммейты"),
    ]
    
    for filepath, description in routes:
        if not check_file_exists(filepath, description):
            errors.append(f"Отсутствует роут: {filepath}")
    
    print()
    
    # Итоги
    print("=" * 60)
    print("📊 ИТОГИ ПРОВЕРКИ")
    print("=" * 60)
    print()
    
    if errors:
        print(f"❌ Найдено ошибок: {len(errors)}")
        for error in errors:
            print(f"   • {error}")
        print()
    else:
        print("✅ Критичных ошибок не найдено!")
        print()
    
    if warnings:
        print(f"⚠️  Найдено предупреждений: {len(warnings)}")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    # Рекомендации
    print("💡 РЕКОМЕНДАЦИИ:")
    print("-" * 60)
    print("1. Установите Python 3.9+")
    print("2. Установите Node.js 18+")
    print("3. Установите Docker и Docker Compose")
    print("4. Создайте .env файл из .env.example")
    print("5. Запустите: pip install -r requirements.txt")
    print("6. Запустите: npm install")
    print("7. Запустите: npm run build")
    print("8. Запустите: docker-compose build")
    print()
    
    if errors:
        print("❌ Проект НЕ готов к сборке. Исправьте ошибки выше.")
        return 1
    elif warnings:
        print("⚠️  Проект готов к сборке, но есть предупреждения.")
        return 0
    else:
        print("✅ Проект готов к сборке!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

