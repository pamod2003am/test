FROM python:3.12.6
WORKDIR /app

COPY . .

RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest
    
RUN npm install

EXPOSE 8443
EXPOSE 3000  

CMD ["/bin/sh", "-c", ". .venv/bin/activate && python start.py & node Bot/WaClient/health.js"]

# CMD ["node" ,"Bot/WaClient/health.js"]
# CMD ["python", "start.py"]

