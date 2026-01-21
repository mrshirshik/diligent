# Deployment Guide

## Local Development

### Quick Start
```bash
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

## Docker Deployment

### Build Docker Images

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      PINECONE_API_KEY: ${PINECONE_API_KEY}
      PINECONE_ENVIRONMENT: ${PINECONE_ENVIRONMENT}
    volumes:
      - ./backend/models:/app/models
      - ./data:/app/data
    networks:
      - jarvis-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - jarvis-network

networks:
  jarvis-network:
    driver: bridge
```

Run with: `docker-compose up -d`

## Cloud Deployment

### AWS EC2

1. Launch Ubuntu 22.04 instance (t2.xlarge recommended)
2. Install Docker and Docker Compose
3. Clone repository
4. Set environment variables
5. Run `docker-compose up -d`
6. Configure security groups for ports 80, 443, 8000

### DigitalOcean App Platform

1. Connect GitHub repository
2. Create app with:
   - Backend service (Python)
   - Frontend service (Node.js build)
3. Set environment variables
4. Deploy

### Hugging Face Spaces

Useful for sharing the Gradio interface version.

## SSL/HTTPS Setup

Using nginx with Let's Encrypt:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://frontend:80;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## Monitoring & Logging

### Application Logs
```bash
docker logs -f backend
docker logs -f frontend
```

### Metrics
Consider integrating:
- Prometheus for metrics
- Grafana for visualization
- ELK Stack for logs

## Scaling

### Multiple Backend Instances
Use nginx load balancing:
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

### Database
- Use managed Pinecone service
- Configure for production workload
- Set up backups

## Security Checklist

- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set strong Pinecone API keys
- [ ] Configure CORS properly
- [ ] Use rate limiting
- [ ] Add authentication if needed
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Backup knowledge base data
