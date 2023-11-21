FROM python:3.11

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY . /app

COPY .env /app/.env

ENV TELEGRAM_TOKEN=TOKEN

CMD ["python", "main.py"]
