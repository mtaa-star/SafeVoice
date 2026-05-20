# Dockerfile for Railway fullstack deployment of SafeVoice Django app
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py seed_admin && gunicorn SafeVoice.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
