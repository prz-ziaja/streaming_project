FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./producer.py .
COPY ./Jakto.jpg .
CMD [ "python", "./producer.py" ]