# use an official python runtime as the base image
FROM python:3.11-slim

# force stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1

# set the working dir to /app
WORKDIR /app

# copy app dir and requirements to working dir
COPY ./app /app
COPY requirements.txt /app/requirements.txt
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# install dependencies in requirements.txt
RUN apt-get update
RUN apt-get install sudo -y build-essential \
python3-pip \
python3-dev
RUN pip install --no-cache-dir -r requirements.txt

# set the location of the flask app
ENV FLASK_APP /app/app_api.py

# make port 5001 available for app use
EXPOSE 5001
EXPOSE 8501 

ENTRYPOINT [ "./start.sh" ]

# RUN apt-get clean