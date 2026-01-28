FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# psycopg 빌드/런타임에 필요한 패키지(안전)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# requirements 먼저 복사(캐시 효율)
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 코드 복사
COPY . /code/

# 정적파일 모으기(Whitenoise 사용할 거라 추천)
RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["sh", "-c", "gunicorn mysite.wsgi:application --bind 0.0.0.0:8080"]
