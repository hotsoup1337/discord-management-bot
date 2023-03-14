FROM mysql

ENV MYSQL_ROOT_PASSWORD root
ADD /database/test_database.sql /docker-entrypoint-initdb.d

EXPOSE 3306

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir downloads
RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "main.py"]

