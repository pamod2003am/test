FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g npm@latest
