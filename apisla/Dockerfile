FROM python:alpine3.12
# FROM python:3.7 

WORKDIR /app

# RUN apt-get update && apt-get install -y python-pip python3.7 python3-setuptools autoconf libtool pkg-config python3-dev build-essential
# RUN apk-add
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        g++
COPY . /app
RUN ls
COPY ./requirements.txt /app


RUN pip3 install -r requirements.txt

CMD ["python3", "/app/main.py"]