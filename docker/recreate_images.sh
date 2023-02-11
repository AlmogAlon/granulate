docker build . -f docker/Dockerfile -t chat-app:base --no-cache
docker build . -f docker/socket/Dockerfile -t chat-socket --no-cache
docker build . -f docker/notification/Dockerfile -t chat-notification --no-cache
docker-compose -f docker/docker-compose.yml up -d
