FROM python:3.12-alpine
LABEL authors="neepaw"

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD alembic upgrade head && python main.py
