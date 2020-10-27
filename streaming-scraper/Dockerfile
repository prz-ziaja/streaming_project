FROM jjanzic/docker-python3-opencv

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./scraper_config.yaml .
COPY ./StreamingScraper.py .

CMD [ "python", "./StreamingScraper.py" ]