FROM ultrafunk/undetected-chromedriver:latest

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app/scraper/

WORKDIR /app/scraper

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]