FROM python:3.11-slim

WORKDIR /src
ENV PYTHONUNBUFFERED 1
EXPOSE 5000

COPY requirements.txt /src/requirements.txt

RUN apt-get update
RUN apt-get install sudo -y build-essential \
    python3-pip \
    python3-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src
# COPY ./data/ /src/data/
ADD app ./app
COPY serve.sh ./
RUN chmod +x /serve.sh
ENTRYPOINT ["./serve.sh"]

RUN apt-get clean
