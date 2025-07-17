# Python 3.11 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (MySQL 클라이언트 포함)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 포트 8000 노출
EXPOSE 8000

# 환경변수 설정
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV DJANGO_ENV=prod

# 시작 스크립트 생성
RUN echo '#!/bin/bash\n\
# 환경변수 설정\n\
export PYTHONPATH=/app\n\
export DJANGO_SETTINGS_MODULE=config.settings\n\
export DJANGO_ENV=prod\n\
\n\
echo "Starting Django ASGI application..."\n\
echo "Environment: $DJANGO_ENV"\n\
echo "Settings module: $DJANGO_SETTINGS_MODULE"\n\
echo "Python path: $PYTHONPATH"\n\
\n\
# MySQL 데이터베이스 연결 대기\n\
echo "Waiting for MySQL database to be ready..."\n\
while ! DJANGO_ENV=prod DJANGO_SETTINGS_MODULE=config.settings python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" 2>/dev/null; do\n\
  echo "Waiting for database connection..."\n\
  sleep 2\n\
done\n\
echo "Database is ready!"\n\
\n\
# 마이그레이션 실행\n\
echo "Running migrations..."\n\
DJANGO_ENV=prod DJANGO_SETTINGS_MODULE=config.settings python manage.py migrate\n\
\n\
# Static 파일 수집 (필요한 경우)\n\
echo "Collecting static files..."\n\
DJANGO_ENV=prod DJANGO_SETTINGS_MODULE=config.settings python manage.py collectstatic --noinput || true\n\
\n\
# ASGI 서버 시작\n\
echo "Starting ASGI server with uvicorn..."\n\
DJANGO_ENV=prod DJANGO_SETTINGS_MODULE=config.settings uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 4\n\
' > /app/start.sh && chmod +x /app/start.sh

# 시작 스크립트 실행
CMD ["/app/start.sh"]
