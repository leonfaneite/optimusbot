FROM python:3.9.0

RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install  qrcode




COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "mainbot.py"]
