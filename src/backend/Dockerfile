FROM python:3.11.5-bookworm

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app/backend/

WORKDIR /app/backend

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]