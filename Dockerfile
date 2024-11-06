FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 3421

CMD ["fastapi", "run", "main.py", "--reload", "--port", "3421", "--host", "0.0.0.0"]