FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /Network

ADD . /Network

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 000

CMD python manage.py runserver 0.0.0.0:8000