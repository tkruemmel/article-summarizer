from langchain_openai import AzureChatOpenAI
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import SummarizationMetric
from deepeval.dataset import EvaluationDataset
import json


# deepeval login --confident-api-key KEY
# deepeval test run test_azure.py


class AzureOpenAI(DeepEvalBaseLLM):
    def __init__(
        self,
        model
    ):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Custom Azure OpenAI Model"

# Replace these with real values
custom_model = AzureChatOpenAI(
    openai_api_version="2023-12-01-preview",
    azure_deployment="article-summarizer",
    azure_endpoint="https://article-summarizer.openai.azure.com/",
    openai_api_key="KEY",
)
# openai_api_version="2024-04-01-preview"

azure_openai = AzureOpenAI(model=custom_model)

metric = SummarizationMetric(threshold=0.5, model=azure_openai)

dataset = EvaluationDataset()
dataset.add_test_cases_from_json_file(
    file_path="data.json",
    input_key_name="content",
    actual_output_key_name="summary"
)

evaluation_results = []

for test_case in dataset.test_cases:
    metric.measure(test_case)
    score_dict = {"test_case":test_case, "score":metric.score, "reason":metric.reason}
    evaluation_results.append(score_dict)
    print(metric.score)
    print(metric.reason)

with open("evaluation_results_llama.json", 'w') as file:
    file.write(json.dumps(evaluation_results, indent=4))
