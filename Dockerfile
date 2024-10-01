FROM python:3.12.6
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g npm@latest
