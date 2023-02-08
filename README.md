# Backend Assignment

This is a simple RESTFUL API for Chat application

## Requirements
- python3.10

## Installation

To run the backend:

- execute these commands: 

```bash
  cd granulate
  python main.py
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

