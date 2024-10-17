import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import SummarizationMetric
from app.kgk_controller import find_specific_post


# run with:
# deepeval login --confident-api-key ${CONFIDENT_API_KEY}
# deepeval test run test_gpt4omini.py


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'KEY')


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()


def add_content(csv_file_path, output_csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['Content'] = df['Link'].apply(
        lambda link: (clean_html(find_specific_post(link) or 'Invalid URL'))
    )
    df.to_csv(output_csv_file_path, index=False)


def convert_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path)
    summary_columns = [
        'Zusammenfassung',
        'Llama 3 Z1',
        'Llama3 Z2',
        'Llama3 Z3',
        'Qwen2 Z1',
        'Qwen2 Z2',
        'Qwen2 Z3',
        'Mistral Z1',
        'Mistral Z2',
        'Mistral Z3',
    ]
    static_columns = ['Titel', 'Link', 'Lesezeit (in min)', 'Content']

    output_directory = 'new_data'
    for summary_column in summary_columns:
        df_filtered = df[static_columns + [summary_column]]
        df_filtered = df_filtered.dropna(subset=[summary_column])
        df_filtered = df_filtered.rename(columns={summary_column: 'summary'})

        hyphenated_column = summary_column.replace(' ', '-')

        json_file = f'data_{hyphenated_column}.json'
        json_file_path = os.path.join(output_directory, json_file)
        df_filtered.to_json(json_file_path, orient='records', indent=4)


def get_dataset(path):
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_json_file(
        file_path=path,
        input_key_name='Content',
        actual_output_key_name='summary',
    )
    return dataset


def evaluate(dataset, file_name):
    evaluation_results = []
    for test_case in dataset.test_cases:
        metric = SummarizationMetric(
            threshold=0.5, model='gpt-4o-mini', verbose_mode=True
        )
        metric.measure(test_case)
        score_dict = {
            'score': metric.score,
            'score_breakdown:': metric.score_breakdown,
            'reason': metric.reason,
        }
        evaluation_results.append(score_dict)
    file_name = file_name[9:-5]
    output_file = f'results/{file_name}_eval.json'
    with open(output_file, 'w') as file:
        json.dump(evaluation_results, file, indent=4)


# add_content('KGK-Zusammenfassungen.csv', 'KGK-ZF-new.csv')
# convert_csv_to_json('KGK-ZF-new.csv')

datasets = [
    'new_data/data_Llama-3-Z1.json',
    'new_data/data_Llama3-Z2.json',
    'new_data/data_Llama3-Z3.json',
    'new_data/data_Mistral-Z1.json',
    'new_data/data_Mistral-Z2.json',
    'new_data/data_Mistral-Z3.json',
    'new_data/data_Qwen2-Z1.json',
    'new_data/data_Qwen2-Z2.json',
    'new_data/data_Qwen2-Z3.json',
    'new_data/data_Zusammenfassung.json',
]


for file in datasets:
    #dataset = get_dataset(file)
    #evaluate(dataset, file)
    print(file)
