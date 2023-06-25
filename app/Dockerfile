FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY arial.ttf .
COPY bot.py .
COPY app_logger.py .
COPY users_data.db .

CMD ["python", "bot.py"]
