FROM python:3.11
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y gcc python3-dev
RUN apt-get install -y libxml2-dev libxslt1-dev build-essential python3-lxml zlib1g-dev
RUN apt-get install -y default-mysql-client default-libmysqlclient-dev
RUN pip install -r requirements.txt
RUN mkdir logs