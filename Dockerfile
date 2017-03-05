FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code

# Gunicorn logs
RUN mkdir /srv/logs/
RUN mkdir /srv/logs/gunicorn/
RUN touch /srv/logs/gunicorn/gunicorn.log
RUN touch /srv/logs/gunicorn/access.log

ADD after_build_backend.sh .