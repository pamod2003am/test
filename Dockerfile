FROM python:3.12.6
WORKDIR /app

COPY . .
CMD ["python", "-m" , "venv" , ".venv"]
CMD [".", ".venv/bin/activate"]

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest
    
RUN npm install -g pm2
RUN npm install

EXPOSE 8443
EXPOSE 3000  

CMD ["pm2-runtime", "start", "start.py", "--name", "python-app"] && ["pm2-runtime", "start", "Bot/WaClient/health.js", "--name", "health-check", "--interpreter", "node"]

# CMD ["node" ,"Bot/WaClient/health.js"]
# CMD ["python", "start.py"]

