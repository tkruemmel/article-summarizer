# Use an official Python runtime as the base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory (our Flask app) into the container at /app
COPY ./app /app
COPY requirements.txt /app/requirements.txt

# Install Flask and other dependencies
RUN apt-get update
RUN apt-get install sudo -y build-essential \
python3-pip \
python3-dev
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP /app/app-api.py

# Make port 5001 available for the app
EXPOSE 5001

# Run the command to start the Flask app
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]

# RUN apt-get clean