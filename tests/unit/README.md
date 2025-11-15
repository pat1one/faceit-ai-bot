# Unit Tests

## Описание

Unit тесты для изолированной проверки отдельных компонентов и функций без внешних зависимостей.

## Структура

```
tests/unit/
├── README.md                 # Этот файл
├── __init__.py              # Инициализация пакета
├── conftest.py              # Общие fixtures для unit тестов
├── test_auth.py             # Тесты аутентификации
├── api/                     # Тесты API слоя
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_schemas.py
├── services/                # Тесты бизнес-логики
│   ├── __init__.py
│   ├── test_ai_service.py
│   ├── test_cache_service.py
│   └── test_player_analysis.py
├── utils/                   # Тесты утилит
│   ├── __init__.py
│   └── test_helpers.py
└── integrations/            # Мок-тесты интеграций
    ├── __init__.py
    ├── test_faceit_client.py
    └── test_groq_service.py
```

## Запуск тестов

### Все unit тесты

```fish
pytest tests/unit/ -v
```

### С покрытием кода

```fish
pytest tests/unit/ --cov=src --cov-report=html --cov-report=term
```

### Только конкретный модуль

```fish
pytest tests/unit/test_auth.py -v
```

### С параллельным выполнением

```fish
pytest tests/unit/ -n auto
```

## Правила написания

1. **Изоляция**: Каждый тест должен быть независимым
2. **Мокирование**: Используйте `unittest.mock` или `pytest-mock` для внешних зависимостей
3. **Naming**: Имена тестов должны описывать проверяемое поведение
   ```python
   def test_create_user_with_valid_data_returns_user_object():
       pass
   ```
4. **AAA Pattern**: Arrange, Act, Assert
   ```python
   def test_example():
       # Arrange - подготовка данных
       user_data = {"email": "test@example.com"}

       # Act - выполнение действия
       result = create_user(user_data)

       # Assert - проверка результата
       assert result.email == "test@example.com"
   ```

## Покрытие кода

Цель: **80%+ покрытие**

Приоритетные модули для покрытия:

- [ ] `src/server/auth/` - 90%+
- [ ] `src/server/services/` - 85%+
- [ ] `src/server/features/player_analysis/` - 85%+
- [ ] `src/server/features/ai_analysis/` - 80%+
- [ ] `src/server/integrations/` - 75%+

## Fixtures

Общие fixtures находятся в `conftest.py`:

- `mock_db_session` - мок сессии БД
- `mock_redis_client` - мок Redis клиента
- `mock_faceit_api` - мок Faceit API
- `test_user` - тестовый пользователь
- `test_token` - тестовый JWT токен

## Примеры

### Тест с мокированием внешнего API

```python
from unittest.mock import Mock, patch
import pytest

@patch('src.server.integrations.faceit_client.requests.get')
def test_fetch_player_data_success(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = {"player_id": "123", "nickname": "TestPlayer"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    result = fetch_player_data("TestPlayer")

    # Assert
    assert result["nickname"] == "TestPlayer"
    mock_get.assert_called_once()
```

### Тест с pytest fixtures

```python
import pytest

def test_user_creation(mock_db_session, test_user):
    # Act
    created_user = create_user(test_user, mock_db_session)

    # Assert
    assert created_user.email == test_user["email"]
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
```

## CI/CD Integration

Unit тесты выполняются автоматически при каждом push в GitHub Actions:

- На pull requests
- Перед деплоем
- По расписанию (nightly builds)

## Полезные ссылки

- [pytest документация](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
