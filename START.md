# Запуск всех сервисов из корня репозитория

1. Установите зависимости для всех пакетов:
   npm run install:all

2. Запустите одновременно frontend, backend и desktop:
   npm run dev:all

3. Для AI-сервиса:
   cd apps/ai
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. Для базы данных:
   cd docker
   docker compose up -d

---

- Для расширения: cd apps/extension, npm run build, затем загрузить public в Chrome.
- Для остановки всех сервисов: остановите процессы в терминале.
