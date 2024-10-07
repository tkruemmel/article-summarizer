import json
from deepeval.metrics import SummarizationMetric
from deepeval.dataset import EvaluationDataset


# run with:
# deepeval login --confident-api-key KEY
# set OPENAI_API_KEY=KEY
# deepeval test run test_deepeval_gpt.py


def convert_txt_to_json(txt_file_path, json_file_path):
    with open(txt_file_path, 'r') as txt_file:
        content = txt_file.read()

    data = json.loads(content)

    filtered_data = [
        {
            "title": item.get("title"),
            "content": item.get("content"),
            "summary": item.get("summary")
        }
        for item in data
    ]

    with open(json_file_path, 'w') as json_file:
        json.dump(filtered_data, json_file, indent=4)


# convert_txt_to_json("scores.txt", "data.json") # reusing this file for now


def get_dataset(path):
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_json_file(file_path=path, input_key_name="content", actual_output_key_name="summary")
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
    with open("evaluation_results_llama.json", 'w') as file:
        file.write(json.dumps(evaluation_results, indent=4))


datasets = ["data/data_Meta-Llama-3.1-70B-Instruct-Turbo_ref.json",
            "data/data_Mixtral-8x22B-Instruct-v0.1_ref.json",
            "data/data_gpt-4o-mini_ref.json"]

for dat in datasets:
    ds = get_dataset(dat)
    print(ds)
    evaluate(ds)
# ds = get_dataset("data_Meta-Llama-3.1-70B-Instruct-Turbo_ref.json")
# evaluate(ds)
