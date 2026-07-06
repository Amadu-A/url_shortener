# Dockerfile

FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir \
    fastapi>=0.139.0 \
    uvicorn>=0.50.0 \
    sqlalchemy>=2.0.51 \
    asyncpg>=0.31.0 \
    greenlet>=3.5.3

COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]