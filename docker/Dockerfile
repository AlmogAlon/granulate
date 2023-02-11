FROM python:3.10.4-slim-buster
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev build-essential -y

COPY .. /reqs/
WORKDIR /reqs/services
RUN BUILD_ONLY=true ./rebuild_env.bat
RUN mv venv /venv
