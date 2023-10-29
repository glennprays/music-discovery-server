FROM python:3.13.0a1-alpine3.18

WORKDIR /app

ADD . /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]