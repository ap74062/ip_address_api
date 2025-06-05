FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./app /code/app/

RUN python3 -m pip install -r requirements.txt
