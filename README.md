# Techcrush Node.js-App

A Node.js app containerized with Docker and published to Docker Hub.

## Run locally
npm install && npm start

## Docker
docker build -t jaegarp/nodejs-app:1.0 .
docker run -d -p 3000:3000 jaegarp/nodejs-app:1.0

## Screenshots
### 1. Docker Build
![Docker Build](screenshots/docker_build.png)
### 2. Docker Hub Image
![Docker Hub](screenshots/docker_hub.png)
### 3. Running Container
![docker ps](screenshots/docker_ps.png)
### 4. Live Application
![Live App](screenshots/live_app.png)
