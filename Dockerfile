# Use an official Python runtime as the base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory (our Flask app) into the container at /app
COPY . /app

# Install Flask and other dependencies
RUN apt-get update
RUN apt-get install sudo -y build-essential \
python3-pip \
python3-dev
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP /flask-app.py

# Make port 5000 available for the app
EXPOSE 5000

# Run the command to start the Flask app
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
