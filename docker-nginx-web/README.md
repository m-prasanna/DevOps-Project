# Docker Nginx Web Server

## Description
A simple static website hosted using Nginx inside a Docker container.

## Tools Used
- Docker
- Nginx
- HTML

## How to Run
```bash
docker build -t nginx-web .
docker run -d -p 8080:80 nginx-web
