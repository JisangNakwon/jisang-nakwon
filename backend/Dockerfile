FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD sh -c "python manage.py migrate && \
  (python manage.py loaddata overwatch/fixtures/initial_streamers.json || true) && \
  (python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','','admin1234')\" || true) && \
  gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000}"
