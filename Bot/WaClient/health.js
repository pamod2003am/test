const http = require('http');
const healthCheckPort = 8443; 

const healthCheckServer = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('OK\n');
    } else {
        res.writeHead(404);
        res.end();
    }
});

healthCheckServer.listen(healthCheckPort, () => {
    console.log(`Health check server running on port ${healthCheckPort}`);
});
