FROM python:3.10.13

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools wheel

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

ADD . /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:8080", "run:app"]