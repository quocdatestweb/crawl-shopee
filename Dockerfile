FROM python:alpine3.18

RUN mkdir -p /crawler
WORKDIR /crawler

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .