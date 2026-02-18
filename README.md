# FitFuel MVP

## Архитектурный обзор (MVP)
1. **Frontend**: Next.js (TypeScript) в `apps/web` — минимальные страницы регистрации, анкеты, дашборда, календаря, рецептов и логирования приемов пищи.
2. **Backend**: FastAPI в `apps/api` — REST API, JWT‑аутентификация, расчет BMR/TDEE/ИМТ и генерация планов.
3. **База данных**: PostgreSQL — хранит пользователей, планы питания, рецепты, тренировки и логи приемов пищи.
4. **Фоновая обработка**: Celery + Redis — асинхронная генерация планов/обработка фото (MVP‑задачи).
5. **Хранилище фото**: MinIO (S3‑совместимое) — хранение фото приемов пищи.
6. **AI‑адаптер**: слой `app/services/ai.py` — OpenAI Vision или Mock при отсутствии ключа.
7. **Seed‑данные**: скрипт заполнения рецептов и упражнений для MVP.
8. **Запуск**: `docker-compose.yaml` поднимает все сервисы одной командой.

## Быстрый старт

```bash
cp .env.example .env

docker compose up --build
```

API будет доступен на `http://localhost:8000/docs`, web — на `http://localhost:3000`.

## Команды и инфраструктура

- Поднять стек: `docker compose up --build`
- Остановить: `docker compose down`
- Миграции: `docker compose exec api alembic upgrade head`
- Сидирование: `docker compose exec api python -m app.seed`

## Переменные окружения
См. `.env.example`. Для локальной сети можно задать `CORS_ORIGINS=*`, чтобы OPTIONS/POST запросы от фронтенда не блокировались (в этом случае credentials отключаются автоматически).

## Создание пользователя
Используйте `/auth/register` в Swagger UI.

## Дисклеймер
Приложение не является медицинским продуктом и не дает медицинских рекомендаций.
