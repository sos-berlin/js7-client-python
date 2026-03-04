# Release: October 14, 2019 | URL: https://hub.docker.com/_/python
FROM python:3.8-bookworm

RUN apt update && apt upgrade -y

RUN pip install \
    --upgrade pip \
    build