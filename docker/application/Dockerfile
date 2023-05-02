FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code /code/static /code/assets
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code/
