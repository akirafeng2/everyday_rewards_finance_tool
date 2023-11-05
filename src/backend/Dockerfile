FROM python:3.11.5-bookworm

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app/backend/

WORKDIR /app/backend

EXPOSE 8000

CMD ["gunicorn", "app:app:", "--bind", "0.0.0.0:8000"]