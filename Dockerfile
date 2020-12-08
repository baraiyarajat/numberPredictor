FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update 
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

RUN pip install -r requirements.txt

COPY . /code/

