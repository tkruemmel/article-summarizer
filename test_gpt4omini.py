import json
import pandas as pd
import os
from deepeval.metrics import SummarizationMetric
from deepeval.dataset import EvaluationDataset
from app.kgk_controller import search_posts, create_full_text
from app.html_segmenter import HTMLSegmenter
from bs4 import BeautifulSoup

# run with:
# deepeval login --confident-api-key API_KEY
# set OPENAI_API_KEY=API_KEY
# deepeval test run test_gpt4omini.py


def extract_search_string(link):
    base_url = "https://www.klassegegenklasse.org/"
    if link.startswith(base_url):
        return link[len(base_url):]


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()


def add_content(csv_file_path, output_csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['Content'] = df['Link'].apply(lambda link: clean_html(
                                        search_posts("https://klassegegenklasse.org/wp-json/wp/v2/posts",
                                                     extract_search_string(link))
                                      ) if extract_search_string(link) else "Invalid URL")
    df.to_csv(output_csv_file_path, index=False)


def convert_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path)
    summary_columns = ["Zusammenfassung", "Llama 3 Z1", "Llama3 Z2", "Llama3 Z3",
                       "Qwen2 Z1", "Qwen2 Z2", "Qwen2 Z3", "Mistral Z1", "Mistral Z2", "Mistral Z3"]
    static_columns = ["Titel", "Link", "Lesezeit (in min)", "Content"]

    output_directory = "new_data"
    for summary_column in summary_columns:
        df_filtered = df[static_columns + [summary_column]]
        df_filtered = df_filtered.dropna(subset=[summary_column])
        df_filtered = df_filtered.rename(columns={summary_column: "summary"})

        hyphenated_column = summary_column.replace(" ", "-")

        json_file = f"data_{hyphenated_column}.json"
        json_file_path = os.path.join(output_directory, json_file)
        df_filtered.to_json(json_file_path, orient='records', indent=4)
        print(f"File '{json_file_path}' created successfully!")


def get_dataset(path):
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_json_file(file_path=path, input_key_name="Content", actual_output_key_name="summary")
    return dataset


def evaluate(dataset):
    evaluation_results = []
    for test_case in dataset.test_cases:
        metric = SummarizationMetric(threshold=0.5, model="gpt-4o-mini", verbose_mode=True)
        metric.measure(test_case)
        score_dict = {"test_case": test_case, "score": metric.score, "reason": metric.reason}
        evaluation_results.append(score_dict)
        print(metric.score)
        # print(metric.reason)
        print(metric.score_breakdown)
    #base_name = dataset[9:-5]
    base_name = dataset[5:-5]
    output_file = f"{base_name}_eval.json"
    with open(output_file, 'w') as file:
        file.write(json.dumps(evaluation_results, indent=4))

#add_content("KGK-Zusammenfassungen.csv", "KGK-ZF-new.csv")
#convert_csv_to_json("KGK-ZF-new.csv")

datasets = ["new_data/data_Llama3-Z1.json", "new_data/data_Llama3-Z2.json", "new_data/data_Llama3-Z3.json",
            "new_data/data_Mistral-Z1.json", "new_data/data_Mistral-Z2.json", "new_data/data_Mistral-Z3.json",
            "new_data/data_Qwen2-Z1.json", "new_data/data_Qwen2-Z2.json", "new_data/data_Qwen2-Z3.json",
            "new_data/data_Zusammenfassung.json"]


ds = get_dataset("new_data/data_Llama3-Z2.json") # test
evaluate(ds)

#evaluate(ds)
#for dat in datasets:
    #ds = get_dataset(dat)
    #print(ds)
    #evaluate(ds)
