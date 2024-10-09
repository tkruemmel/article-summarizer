# article-summarizer

To build and then run docker conatiner:

    docker build -t flaskapi:latest .
    docker-compose up -d
    docker exec -it article-summarizer_ollama-container_1 ollama run phi

    # older commands probably no longer needed
    docker run -p 5001:5000 flaskapi:latest
    docker run --env-file .env flaskapi:latest

To install requirements:

    pip install -r requirements.txt

To update requirements:

    pip3 freeze > requirements.txt

Other helpful docker commands:

    docker-compose down
    docker system prune -a

Local virtual env commands:

    python3 -m venv myvenv
    source myvenv/bin/activate
    
    deactivate

deepeval login:

    deepeval login --confident-api-key {CONFIDENT_API_KEY}
    deepeval test run test_togetherai.py
