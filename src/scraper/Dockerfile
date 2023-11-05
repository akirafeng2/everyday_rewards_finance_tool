FROM ultrafunk/undetected-chromedriver:latest

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app/scraper/

WORKDIR /app/scraper

EXPOSE 8000

CMD ["gunicorn", "app:app:", "--bind", "0.0.0.0:8000"]