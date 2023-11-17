FROM ultrafunk/undetected-chromedriver:latest

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY src /app/src/