## Лабораторная работа Docker
#### Поглазов Никита 2384

---

В качестве приложения для развертывания был взят простой веб-сервер, написанный в рамках одной из ЛР по дисциплине "Базы Данных".

БД - PostgreSQL

Backend – Flask

Dockerfile
```dockerfile
FROM python:3.12-alpine
LABEL authors="neepaw"

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD alembic upgrade head && python main.py
```

Используется легковесный образ Python 3.12 на базе Alpine. Перед запуском проводятся миграции с помощью alembic. Поскольку сервер не требует наличия записей в БД, она заполняется случайно сгенерированными данными с помощью faker во время миграции.

docker-compose.yml
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: neepaw
      POSTGRES_PASSWORD: nekson
      POSTGRES_DB: clinic
    ports:
      - "5433:5432"
    healthcheck:
      test: pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB
      interval: 5s
      timeout: 3s
      retries: 5

  web:
    build: .
    environment:
      POSTGRES_URL: postgresql+psycopg2://neepaw:nekson@db:5432/clinic
    ports:
      - "5001:5000"
    depends_on:
      db:
        condition: service_healthy
```

Для БД используется легковесный образ PostgreSQL15 на базе Alpine.
Для проверки работы БД с хоста проброшен порт 5433 на 5432 порт контейнера. В качестве healthcheck используется команда pg_isready для текущего пользователя и БД. 

В сервисе сервера опредеена переменная окружения для URL БД. Также проброшен порт 5001 на 5000 (по каким-то причинам при пробросе 5000 порта сервер не отвечал, возможно на этом порте на моем ПК уже работало что-то). Этот сервис зависит от сервиса БД и не запустится до тех пор, пока db не будет "_healthy_".

В качестве проверки работы развернутого приложения можно запустить HTTP запросы из `requests.http`. Большинства из них завязаны на реальные данные, из-за чего могут выдать пустой ответ, но последние из них содержат SQL-инъекции, и выдают все данные из отношения (либо усыпляют БД на несколько секунд).
