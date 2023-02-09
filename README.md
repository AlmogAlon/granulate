# Backend Assignment

This is a simple RESTFUL API for Chat application

## Requirements
- python3.10
- Docker (optional)
- docker-compose version 1.29.2

## Installation

To run the backend locally:

- execute these commands: 

```bash
  cd granulate
  python main.py
```

To run the backend using docker-compose:
- execute these commands: 

```bash
  cd granulate
  docker build . -f docker/Dockerfile -t chat-app:base
  docker build . -f docker/app/Dockerfile -t chat-app
  docker-compose -f docker/docker-compose.yml up -d
```


## API Reference

#### Get all messages

```bash
  curl --location --request GET '127.0.0.1:1337/chat'
```

#### Send a new message

```bash
  curl --location --request POST '127.0.0.1:1337/chat' \
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

#### Get rooms

```bash
  curl --location --request GET '127.0.0.1:1337/chat/room/<OPTIONAL_ID>'
```


## Client usage

```bash
  cd granulate
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