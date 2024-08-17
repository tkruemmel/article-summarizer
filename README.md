# article-summarizer

To build and then run docker conatiner:

    docker build -t flaskapi:latest .
    docker-compose up -d
    docker exec -it article-summarizer-ollama-container-1 ollama run phi

To install requirements:

    pip install -r requirements.txt
