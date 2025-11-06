FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# start gunicorn server
CMD ["/bin/sh", "-c", "gunicorn --bind 0.0.0.0:$PORT wsgi:app"]