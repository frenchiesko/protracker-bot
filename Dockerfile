# Базовый образ, содержащий необходимые зависимости
FROM python:3.11

# Установка зависимостей
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копирование файлов проекта в образ
COPY . /app
WORKDIR /app

COPY .env /app/.env

# Установка переменных среды
ENV TELEGRAM_TOKEN=TOKEN

# Определение команды для запуска бота
CMD ["python", "main.py"]
