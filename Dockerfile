FROM python:3.11-slim

# create app directory
WORKDIR /app

# copy required dependecies list 
COPY requirements.txt ./

# update pip and install dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy rest of the app
COPY /app ./

# prepare port 8501
EXPOSE 8501

# set startup action
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
