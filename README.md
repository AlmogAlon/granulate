# Backend Assignment

This is a simple RESTFUL API for Chat application

## Requirements
- python3.10
- Docker (optional)

## Installation

To run the backend locally:

- execute these commands: 

```bash
  cd granulate
  python main.py
```

To run the backend in docker:
- execute these commands: 

```bash
  cd granulate
  docker docker build . -f docker/Dockerfile -t chat-app
  docker run -p 1337:1337 chat-app
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
}'
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `Str` | **Required** |
| `message` | `Str` | **Required** |


## Client usage

```bash
  cd granulate
  python client.py --username=david --message

```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `Str` | **Required** fetch messages for the given user|
| `message` |  | **Optional** prompt message input |
