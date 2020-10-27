FROM jjanzic/docker-python3-opencv

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app/forP.py .

CMD [ "python", "./forP.py" ]