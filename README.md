# Backend Assignment

This is a simple RESTful API for Chat application. 
Backend servers are written in Python using Bottle framework.
The project built according to the design diagram in `docs` folder.

it uses MySQL (sqlalchemy as ORM) as database, and Redis as cache and message broker.

Project Services are:
- Notification service
  - Exposes a RESTFUL API for sending notifications to users.
  - Stores notifications in a database.

- Socket service
  - Bottle application for handling websocket connections to communicate with clients.

## Requirements
- python3.10
- Docker (optional)
- docker-compose version 1.29.2

## Installation

To run the services using docker-compose (recommended):
- execute these commands: 

```bash
  cd granulate
  docker build . -f docker/Dockerfile -t chat-app:base
  docker build . -f docker/notification/Dockerfile -t chat-notification
  docker build . -f docker/socket/Dockerfile -t chat-socket
  docker-compose -f docker/docker-compose.yml up -d
```

To run the services locally:
```bash
  cd granulate/services
  ./rebuild_env.bat
```
- open IDE from the root folder of the service
- configure python interpreter to use: `granulate/services/venv/bin/python`

```bash
  cd granulate/services/SERVICE_NAME
  python main.py
```


## Notification Service 
### API Reference

#### Send a new message

```bash
  curl --location --request POST '127.0.0.1:1337/api/notification' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "message": "test message"
    "room_name": "test_room"
}'
```

| Parameter   | Type     | Description  |
|:------------| :------- |:-------------|
| `username`  | `Str` | **Required** |
| `message`   | `Str` | **Required** |
| `room_name` | `Str` | **Optional** |


## Test Client tool

connects to the socket service and waits for messages.
it can also send messages to the socket service.

```bash
  cd granulate/services/socket
  python test_client.py
```

```bash
  cd granulate/services/tools
  python client.py --username=david --message
```
| Parameter  | Type     | Description                                    |
|:-----------| :------- |:-----------------------------------------------|
| `username` | `Str` | **Required** fetch messages for the given user |
| `message`  |  | **Optional** prompt message input              |
| `room`     |  | **Optional** room name                         |

To run the client in docker:
- execute these commands: 

```bash
  cd granulate
  docker build . -f docker/client/Dockerfile -t chat-app:client
  docker run --network="host" chat-app:client --username david
```
