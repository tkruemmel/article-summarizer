from eval_utils import get_posts
import app.summarizer as summarizer
import json
import os
import re
from tenacity import retry, stop_after_attempt, wait_random_exponential


@retry(wait=wait_random_exponential(min=6, max=60), stop=stop_after_attempt(12))
def get_summary(i, post):
    summary_log = []
    summary = summarizer.summarize(post["content"], model)
    print(f"Summary: #{i}")
    print(summary)
    log = {"model": model, "title": post["title"], "content": post["content"], "summary": summary}
    summary_log.append(log)
    return summary_log


def generate_data(posts, model):
    generated_data = []
    print(f"Model: {model}")
    for i, post in enumerate(posts, start=1):
        summary_log = get_summary(i, post)
        generated_data.append(summary_log)

    file_name = f"data/data_{model}.json"
    with open(file_name, "w+") as file:
        file.write(json.dumps(generated_data, indent=4))


if __name__ == "__main__":
    os.mkdir("data")
    models = ["meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
              "mistralai/Mixtral-8x22B-Instruct-v0.1",
              #"google/gemma-2-27b-it"
            #"google/gemma-2-9b-it"
              ]
    posts = get_posts()
    for model in models:
        generate_data(posts, model)
    #with open("posts.json", "r") as file:
        #posts = json.load(file)
        #for model in models:
            #generate_data(posts, model)
