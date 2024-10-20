# Article Summarizer

### Deploying app through docker

To build and then run docker conatiner of main API-based app:

    docker build -t flaskapi:latest .
    LLM_HOME=api_only docker-compose --profile api_only up -d

Once deployed app can be found at `http://0.0.0.0:8501/`

Initially our application leveraged a locally downloaded, smaller LLM to generate summaries. Although this approach was abandoned fairly quickly due to the model's poor performance in favor of an API-based LLM, it is still available to run with the following commands:

    docker build -t flaskapi:latest .
    docker pull ollama/ollama:latest
    LLM_HOME=local_llm docker-compose --profile local_llm up -d


Docker commands for clean up:

> :warning: system prune command will **delete all** unused containers, networks, and images, **not just those from this project!**

    docker-compose down
    docker system prune -a


### Running the evaluation code

Create local virtual environment and install required packages:

    python3 -m venv evalvenv
    source evalvenv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
Login to deepeval and run test:

    deepeval login --confident-api-key {CONFIDENT_API_KEY}
    deepeval test run app/eval/test_gpt4omini.py

Shut down virtual environment with:

    deactivate

