# Article Summarizer

### Deploying app through docker

TODO: Explain the two apps.

To build and then run docker conatiner of main api based app:

    docker build -t flaskapi:latest .
    LLM_HOME=api_only docker-compose --profile api_only up -d

To run (and download) the smaller local llm version of the app:

    docker build -t flaskapi:latest .
    docker pull ollama/ollama:latest
    LLM_HOME=local_llm docker-compose --profile local_llm up -d

Once deployed app can be found at `http://0.0.0.0:8501/`


Other helpful docker commands:

    docker-compose down
    docker system prune -a


### Useful commands for running evaluation

Local virtual env commands:

    python3 -m venv evalvenv
    source evalvenv/bin/activate
    
    deactivate

To install requirements:

    pip install -r requirements.txt

To update requirements:

    pip3 freeze > requirements.txt

deepeval login:

    deepeval login --confident-api-key {CONFIDENT_API_KEY}
    deepeval test run test_togetherai.py
