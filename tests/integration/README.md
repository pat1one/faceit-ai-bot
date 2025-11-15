# Integration Tests

## Описание

Integration тесты проверяют взаимодействие между компонентами системы (API + БД, API + Redis, API + внешние сервисы).

## Структура

```
tests/integration/
├── README.md                 # Этот файл
├── __init__.py              # Инициализация пакета
├── conftest.py              # Fixtures для integration тестов
├── test_api_endpoints.py    # Тесты API endpoints
├── test_database.py         # Тесты операций с БД
├── test_redis_cache.py      # Тесты кэширования
├── test_celery_tasks.py     # Тесты Celery задач
└── test_external_apis.py    # Тесты интеграций с внешними API
```

## Запуск тестов

### Все integration тесты

```fish
pytest tests/integration/ -v
```

### С реальной тестовой БД

```fish
set -x TEST_DATABASE_URL "postgresql://test:test@localhost:5432/faceit_test"
pytest tests/integration/ -v
```

### Только API тесты

```fish
pytest tests/integration/test_api_endpoints.py -v
```

### С дебаг выводом

```fish
pytest tests/integration/ -v -s --log-cli-level=DEBUG
```

## Подготовка окружения

### 1. Создать тестовую базу данных

```fish
# Создать тестовую БД
createdb faceit_test

# Или через psql
psql -U postgres -c "CREATE DATABASE faceit_test;"
```

### 2. Запустить зависимости (Docker Compose)

```fish
docker compose -f docker-compose.dev.yml up -d db redis
```

### 3. Применить миграции

```fish
set -x DATABASE_URL "postgresql://test:test@localhost:5432/faceit_test"
alembic upgrade head
```

## Правила написания

1. **Используйте реальные зависимости**: БД, Redis, но в тестовом окружении
2. **Изоляция транзакций**: Каждый тест должен откатывать изменения
3. **Test fixtures**: Подготовка тестовых данных в БД
4. **Cleanup**: Очистка данных после тестов

## Примеры

### Тест API endpoint с БД

```python
import pytest
from fastapi.testclient import TestClient
from src.server.main import app

client = TestClient(app)

def test_create_user_endpoint(db_session, test_user_data):
    """Тест создания пользователя через API"""
    response = client.post("/api/users", json=test_user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]

    # Проверяем что пользователь создан в БД
    user = db_session.query(User).filter_by(email=test_user_data["email"]).first()
    assert user is not None
```

### Тест с Redis кэшем

```python
import pytest
from src.server.services.cache_service import CacheService

def test_cache_player_data(redis_client):
    """Тест кэширования данных игрока"""
    cache = CacheService(redis_client)
    player_data = {"id": "123", "nickname": "TestPlayer"}

    # Сохраняем в кэш
    cache.set_player_data("123", player_data)

    # Читаем из кэша
    cached_data = cache.get_player_data("123")

    assert cached_data == player_data
```

### Тест Celery задачи

```python
import pytest
from src.server.tasks import analyze_player_task

def test_analyze_player_task(db_session, mock_faceit_api):
    """Тест асинхронной задачи анализа игрока"""
    result = analyze_player_task.apply(args=["test_player"]).get()

    assert result["status"] == "success"
    assert result["player_id"] is not None
```

### Тест интеграции с внешним API

```python
import pytest
import responses
from src.server.integrations.faceit_client import FaceitClient

@responses.activate
def test_fetch_player_from_faceit_api():
    """Тест интеграции с Faceit API (мокированный ответ)"""
    # Мокируем HTTP ответ
    responses.add(
        responses.GET,
        "https://open.faceit.com/data/v4/players",
        json={"player_id": "123", "nickname": "TestPlayer"},
        status=200
    )

    client = FaceitClient(api_key="test_key")
    player = client.get_player("TestPlayer")

    assert player["nickname"] == "TestPlayer"
```

## Fixtures

Общие fixtures находятся в `conftest.py`:

- `db_session` - сессия тестовой БД (с rollback после теста)
- `redis_client` - клиент тестового Redis
- `test_client` - FastAPI TestClient
- `test_user` - созданный тестовый пользователь в БД
- `auth_headers` - заголовки с JWT токеном для авторизации

## Настройка CI/CD

Integration тесты запускаются в GitHub Actions с использованием service containers:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    env:
      POSTGRES_PASSWORD: test
      POSTGRES_DB: faceit_test
    options: >-
      --health-cmd pg_isready
      --health-interval 10s

  redis:
    image: redis:7-alpine
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
```

## Очистка после тестов

```fish
# Удалить тестовую БД
dropdb faceit_test

# Очистить Redis
redis-cli FLUSHDB

# Остановить Docker контейнеры
docker compose -f docker-compose.dev.yml down
```

## Метрики успеха

- ✅ Все тесты проходят на чистой БД
- ✅ Нет утечек данных между тестами
- ✅ Время выполнения < 5 минут
- ✅ Coverage критичных API endpoints > 85%

## Полезные ссылки

- [FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [responses library](https://github.com/getsentry/responses)
- [pytest-docker](https://pypi.org/project/pytest-docker/)
