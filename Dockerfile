FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["sh", "-c", "gunicorn mysite.wsgi:application --bind 0.0.0.0:8080"]
