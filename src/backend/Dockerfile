FROM python:3.11.5-bookworm

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN touch /app/__init__.py

COPY . /app/backend/

WORKDIR /app/backend