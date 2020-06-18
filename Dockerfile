FROM python:3.7.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

# install dependencies
RUN pip install --default-timeout=100 --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt

# copy project
COPY . /usr/src/app/

CMD alembic upgrade head && gunicorn --bind :8080 wsgi:app
