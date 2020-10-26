FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./scraper_config.yaml .
COPY ./StreamingScraper.py .

CMD [ "python", "./StreamingScraper.py" ]