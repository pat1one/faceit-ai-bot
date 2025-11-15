# End-to-End (E2E) Tests

## Описание

E2E тесты проверяют полные пользовательские сценарии от начала до конца, включая фронтенд и бэкенд.

## Структура

```
tests/e2e/
├── README.md                 # Этот файл
├── __init__.py              # Инициализация пакета
├── conftest.py              # Fixtures для e2e тестов
├── test_user_flows.py       # Основные user flows
├── test_player_analysis.py  # E2E тесты анализа игроков
├── test_auth_flow.py        # Регистрация и авторизация
└── test_payments.py         # Процесс оплаты подписки
```

## Инструменты

Используем **Playwright** для автоматизации браузера:

```fish
# Установить Playwright
pip install playwright pytest-playwright

# Установить браузеры
playwright install chromium firefox webkit
```

## Запуск тестов

### Все e2e тесты (headless режим)

```fish
pytest tests/e2e/ -v
```

### С видимым браузером (для отладки)

```fish
pytest tests/e2e/ -v --headed
```

### Только в Chrome

```fish
pytest tests/e2e/ -v --browser chromium
```

### С замедленным выполнением (для наблюдения)

```fish
pytest tests/e2e/ -v --headed --slowmo 1000
```

### Параллельный запуск

```fish
pytest tests/e2e/ -n 4 --dist loadfile
```

### С записью видео при ошибках

```fish
pytest tests/e2e/ -v --video on-failure --screenshot on-failure
```

## Подготовка окружения

### 1. Запустить приложение локально

```fish
# Backend
docker compose -f docker-compose.dev.yml up -d

# Frontend (в отдельном терминале)
npm run dev
```

### 2. Настроить тестовые данные

```fish
# Создать тестового пользователя
python scripts/create_test_user.py
```

### 3. Настроить переменные окружения

```fish
set -x E2E_BASE_URL "http://localhost:3000"
set -x E2E_API_URL "http://localhost:8000"
set -x E2E_TEST_USER_EMAIL "test@example.com"
set -x E2E_TEST_USER_PASSWORD "Test123456"
```

## Правила написания

1. **Реалистичные сценарии**: Тестируйте как реальный пользователь
2. **Стабильность**: Используйте явные ожидания, избегайте sleep
3. **Изоляция**: Каждый тест должен быть независимым
4. **Page Object Pattern**: Инкапсулируйте логику страниц

## Примеры

### Простой E2E тест

```python
import pytest
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    """Тест загрузки главной страницы"""
    page.goto("http://localhost:3000")

    # Проверяем заголовок
    expect(page).to_have_title("Faceit AI Bot")

    # Проверяем наличие кнопки
    expect(page.locator("text=Начать анализ")).to_be_visible()
```

### Тест авторизации

```python
def test_user_login_flow(page: Page):
    """Тест процесса авторизации"""
    page.goto("http://localhost:3000/auth")

    # Заполняем форму
    page.fill('input[name="email"]', "test@example.com")
    page.fill('input[name="password"]', "Test123456")

    # Нажимаем кнопку входа
    page.click('button[type="submit"]')

    # Ждем редиректа на dashboard
    page.wait_for_url("**/dashboard")

    # Проверяем что вошли
    expect(page.locator("text=Мой профиль")).to_be_visible()
```

### Тест с Page Object Pattern

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.submit_button = page.locator('button[type="submit"]')

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

# test_auth_flow.py
def test_login_with_page_object(page: Page):
    login_page = LoginPage(page)
    page.goto("http://localhost:3000/auth")

    login_page.login("test@example.com", "Test123456")

    page.wait_for_url("**/dashboard")
    expect(page.locator("text=Мой профиль")).to_be_visible()
```

### Тест анализа игрока (комплексный сценарий)

```python
def test_player_analysis_full_flow(page: Page, authenticated_user):
    """Полный сценарий анализа игрока"""
    # 1. Открываем страницу анализа
    page.goto("http://localhost:3000/dashboard")
    page.click("text=Анализ игрока")

    # 2. Вводим nickname игрока
    page.fill('input[placeholder="Введите nickname"]', "s1mple")
    page.click("button:has-text('Анализировать')")

    # 3. Ждем загрузки результатов
    page.wait_for_selector(".analysis-results", timeout=30000)

    # 4. Проверяем наличие данных
    expect(page.locator(".player-stats")).to_be_visible()
    expect(page.locator(".ai-recommendations")).to_be_visible()

    # 5. Проверяем можно ли сохранить результат
    page.click("button:has-text('Сохранить')")
    expect(page.locator("text=Анализ сохранен")).to_be_visible()
```

### Тест с API моками

```python
def test_player_analysis_with_api_mock(page: Page):
    """Тест с мокированием API ответов"""
    # Мокируем API ответ
    page.route("**/api/players/*", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"player_id": "123", "nickname": "TestPlayer", "stats": {}}'
    ))

    page.goto("http://localhost:3000/dashboard")
    page.fill('input[placeholder="Введите nickname"]', "TestPlayer")
    page.click("button:has-text('Анализировать')")

    expect(page.locator("text=TestPlayer")).to_be_visible()
```

## Fixtures

Общие fixtures находятся в `conftest.py`:

- `page` - экземпляр браузера (автоматически из pytest-playwright)
- `context` - контекст браузера
- `authenticated_user` - пользователь с активной сессией
- `test_database` - чистая тестовая БД для каждого теста

## Отладка

### Playwright Inspector

```fish
# Запустить с отладчиком
PWDEBUG=1 pytest tests/e2e/test_user_flows.py -v
```

### Trace Viewer

```python
# В conftest.py
@pytest.fixture
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)
    yield context
    context.tracing.stop(path="trace.zip")
```

Просмотр trace:

```fish
playwright show-trace trace.zip
```

## CI/CD Integration

E2E тесты в GitHub Actions:

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install playwright pytest-playwright
          playwright install --with-deps chromium

      - name: Start services
        run: docker compose up -d

      - name: Run E2E tests
        run: pytest tests/e2e/ -v --video on-failure

      - name: Upload artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-screenshots
          path: test-results/
```

## Метрики успеха

- ✅ Все критичные user flows покрыты
- ✅ Тесты стабильны (нет flaky tests)
- ✅ Время выполнения полного набора < 10 минут
- ✅ Coverage основных страниц > 90%

## Лучшие практики

1. **Используйте data-testid**: Добавляйте атрибуты для стабильных селекторов

   ```html
   <button data-testid="analyze-button">Анализировать</button>
   ```

2. **Избегайте хрупких селекторов**: Не используйте CSS классы для тестов

3. **Явные ожидания**: Используйте `expect()` вместо `sleep()`

4. **Независимость тестов**: Каждый тест должен работать изолированно

5. **Очистка данных**: После каждого теста удаляйте созданные данные

## Полезные ссылки

- [Playwright документация](https://playwright.dev/python/)
- [pytest-playwright](https://playwright.dev/python/docs/test-runners)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Selectors Guide](https://playwright.dev/docs/selectors)
