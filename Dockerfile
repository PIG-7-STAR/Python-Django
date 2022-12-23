# FROM python:3.6
FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libaio1
RUN mkdir /backendPeti
COPY requirements.txt /backendPeti
RUN pip install -r backendPeti/requirements.txt
WORKDIR /backendPeti
COPY ./backendPeti /backendPeti