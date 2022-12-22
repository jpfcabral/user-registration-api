FROM python:3

WORKDIR /app

COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt


RUN pip install -r ./requirements.txt

CMD uvicorn src.main:app --host 0.0.0.0