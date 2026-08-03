# Docker Container Project

## What I Built
A containerised web application using Docker and nginx:alpine.

## Files
- [Dockerfile](Dockerfile) — instructions to build the container image
- [index.html](index.html) — the web page served by nginx inside the container

## How to Run
```bash
docker build -t bright-app .
docker run -d -p 8081:80 bright-app
```
Then visit http://localhost:8081

## What I Learned
- Containers package an app with all its dependencies
- Docker images are templates, containers are running instances
- Port mapping connects host ports to container ports
- nginx:alpine is only 5MB — containers are extremely lightweight
- Same container runs identically on any machine with Docker
