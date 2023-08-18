FROM python:3.11.4-bookworm

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY src .

CMD ["python", "test_scratch.py"]