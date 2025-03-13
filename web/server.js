const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml'
};

const server = http.createServer((req, res) => {
    console.log(`Request received: ${req.method} ${req.url}`);
    
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // Handle OPTIONS request
    if (req.method === 'OPTIONS') {
        res.statusCode = 204;
        res.end();
        return;
    }
    
    // Ignore favicon requests
    if (req.url === '/favicon.ico') {
        res.statusCode = 204;
        res.end();
        return;
    }
    
    // Handle the request for the root path
    let filePath = req.url === '/' 
        ? path.join(__dirname, 'index.html')
        : path.join(__dirname, req.url);
    
    console.log(`Looking for file: ${filePath}`);
    
    // Check if the file exists
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
            console.error(`File not found: ${filePath}`);
            
            // Try to serve graph.json from the root directory if it's not in web/
            if (req.url === '/graph.json') {
                const rootGraphPath = path.join(__dirname, '..', 'output', 'graph.json');
                console.log(`Trying alternative path: ${rootGraphPath}`);
                
                fs.access(rootGraphPath, fs.constants.F_OK, (err2) => {
                    if (err2) {
                        res.statusCode = 404;
                        res.end(`File ${req.url} not found!`);
                    } else {
                        fs.readFile(rootGraphPath, (err3, content) => {
                            if (err3) {
                                res.statusCode = 500;
                                res.end(`Server Error: ${err3.code}`);
                            } else {
                                res.statusCode = 200;
                                res.setHeader('Content-Type', 'application/json');
                                res.end(content, 'utf-8');
                            }
                        });
                    }
                });
                return;
            }
            
            res.statusCode = 404;
            res.end(`File ${req.url} not found!`);
            return;
        }

        // Get the file extension
        const extname = path.extname(filePath);
        const contentType = MIME_TYPES[extname] || 'application/octet-stream';

        // Read and serve the file
        fs.readFile(filePath, (err, content) => {
            if (err) {
                console.error(`Error reading file: ${err.code}`);
                res.statusCode = 500;
                res.end(`Server Error: ${err.code}`);
            } else {
                console.log(`Serving file: ${filePath} as ${contentType}`);
                res.statusCode = 200;
                res.setHeader('Content-Type', contentType);
                res.end(content, 'utf-8');
            }
        });
    });
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
}); 