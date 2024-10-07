from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import SummarizationMetric
from deepeval.dataset import EvaluationDataset
import json
from together import Together
import instructor
from pydantic import BaseModel
from openai import OpenAI



# set TOGETHER_API_KEY=key

# deepeval login --confident-api-key key
# deepeval test run test_togetherai.py

TOGETHER_API_KEY="KEY"
client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=TOGETHER_API_KEY
)

class TogetherLLM(DeepEvalBaseLLM):
    def __init__(
        self
    ):
        self.model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.client = instructor.from_openai(client, mode=instructor.Mode.JSON
        )

    def load_model(self):
        return self.model_name

    def generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        model_name = self.load_model()
        #response = self.client.completions.create(
        #    model=model_name,
        #    response_model=schema
        #)
        response = self.client.messages.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_model=schema,
        )
        return response


    async def a_generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        return self.generate(prompt, schema)


    def get_model_name(self):
        return "Custom together.ai LLM"


custom_model = TogetherLLM()

metric = SummarizationMetric(threshold=0.5, model=custom_model, async_mode=False)

dataset = EvaluationDataset()
dataset.add_test_cases_from_json_file(
    file_path="data.json",
    input_key_name="content",
    actual_output_key_name="summary")

evaluation_results = []

for test_case in dataset.test_cases:
    metric.measure(test_case)
    score_dict = {"test_case":test_case, "score":metric.score, "reason":metric.reason}
    evaluation_results.append(score_dict)
    print(metric.score)
    print(metric.reason)

with open("evaluation_results.json", "w") as file:
    file.write(json.dumps(evaluation_results, indent=4))
