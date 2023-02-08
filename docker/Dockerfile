FROM python:3.10.4-slim-buster
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev build-essential -y
COPY .. /reqs/

ENV VIRTUAL_ENV=/reqs/venv
RUN python3.10 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U pip && pip install -r /reqs/requirements.txt
