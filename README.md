# URL Shortener

Сервис сокращения ссылок.

Что умеет:

- `POST /shorten` - принимает длинный URL и возвращает короткий slug.
- `GET /{slug}` - редиректит на исходный URL и увеличивает счетчик переходов.
- `GET /stats/{slug}` - возвращает количество переходов по ссылке.
- UI доступен через простой HTML-фронт.

## Структура

```text
src/
  main.py              # FastAPI routes, middleware, app startup
  service.py           # бизнес-логика генерации и поиска ссылок
  shortener.py         # генерация slug
  exceptions.py        # кастомные ошибки
  database/
    db.py              # подключение к БД
    models.py          # SQLAlchemy models
    crud.py            # запросы к БД
frontend/
  index.html           # UI
nginx/
  default.conf         # раздача UI и proxy в backend
tests/
  test_api.py
  test_service.py
docker-compose.yaml
Dockerfile
```

## Локальный запуск

Нужны Python 3.13, uv, Docker для PostgreSQL.

Запустить БД:

```bash
docker compose up -d db
```

Linux/macOS:

```bash
uv sync
uv run uvicorn src.main:app --reload
```

Windows PowerShell:

```powershell
uv sync
uv run uvicorn src.main:app --reload
```

API будет доступен здесь:

```text
http://127.0.0.1:8000/docs
```

Для локального UI без контейнера запусти static server из папки `frontend`:

Linux/macOS:

```bash
cd frontend
python -m http.server 5500
```

Windows PowerShell:

```powershell
cd frontend
python -m http.server 5500
```

UI:

```text
http://127.0.0.1:5500/index.html
```

## Запуск в контейнерах

```bash
docker compose up -d --build
```

После запуска открой:

```text
http://127.0.0.1:5500/index.html
```

Что нажать:

1. В блоке `Сократи ссылку` вставь длинный URL.
2. Нажми `Сократить`.
3. Ниже появится короткая ссылка.
4. В блоке `Статистика переходов` введи slug.
5. Нажми `Получить статистику`.

## Если заняты порты

Порты по умолчанию:

- `5500` - UI через nginx.
- `5433` - PostgreSQL на хосте.
- `8000` - локальный FastAPI при запуске без контейнера.

Если занят `5500`, поменяй в `docker-compose.yaml`:

```yaml
ports:
  - "127.0.0.1:5501:80"
```

Тогда UI будет здесь:

```text
http://127.0.0.1:5501/index.html
```

Если занят `5433`, поменяй:

```yaml
ports:
  - "127.0.0.1:5434:5432"
```

И при локальном запуске без контейнера обнови `DATABASE_URL` или строку подключения в `src/database/db.py`.

Если занят `8000` при локальном запуске:

```bash
uv run uvicorn src.main:app --reload --port 8001
```
---
## Запуск тестов

```bash
cd url_shortener
pytest -s
```