# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
MAINTAINER Alexey Sinadskiy 'alexsin@e1.ru'

WORKDIR .

COPY requirements.txt requirements.txt
COPY request_clf/server.py request_clf/server.py
COPY data/ data/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["request_clf/server.py"]
