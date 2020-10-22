FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app/forP.py .

CMD [ "python", "./forP.py" ]