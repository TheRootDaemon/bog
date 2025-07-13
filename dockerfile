FROM python:3.13.5-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "10000"]
