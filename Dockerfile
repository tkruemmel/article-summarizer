FROM python:3.11-slim

# create app directory
WORKDIR /app

# copy required files
COPY requirements.txt ./
COPY /app ./

# install dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]