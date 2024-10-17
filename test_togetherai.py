import json
import os

from deepeval.dataset import EvaluationDataset
from deepeval.metrics import SummarizationMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from pydantic import BaseModel
from together import Together


# run with:
# deepeval login --confident-api-key ${CONFIDENT_API_KEY}
# deepeval test run test_togetherai.py


TOGETHER_API_KEY = os.environ.get('TOGETHER_API_KEY', 'KEY')

client = Together(api_key=TOGETHER_API_KEY)


class TogetherLLM(DeepEvalBaseLLM):
    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        # llm = client.completions.create(model=self.model, prompt=prompt)
        # return llm.choices[0].text

        llm = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role': 'system',
                    'content': 'The following are questions about a news article. Only answer in JSON.',
                },
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            response_format={
                'type': 'json_object',
                'schema': schema.model_json_schema(),
            },
        )

        json_result = json.loads(llm.choices[0].message.content)
        return schema(**json_result)

    async def a_generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        # llm = client.completions.create(model=self.model, prompt=prompt)
        # res = await client.completions.create(model=self.model, prompt=prompt)
        # return res.choices[0].text
        res = await client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role': 'system',
                    'content': 'The following are questions about a news article. Only answer in JSON.',
                },
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            response_format={
                'type': 'json_object',
                'schema': schema.model_json_schema(),
            },
        )

        json_result = json.loads(res.choices[0].message.content)
        return schema(**json_result)

    def get_model_name(self):
        return 'Custom together.ai LLM'


custom_model = TogetherLLM(model='mistralai/Mixtral-8x7B-Instruct-v0.1')

metric = SummarizationMetric(
    threshold=0.5, model=custom_model, async_mode=False
)

dataset = EvaluationDataset()
dataset.add_test_cases_from_json_file(
    file_path='data.json',
    input_key_name='content',
    actual_output_key_name='summary',
)

evaluation_results = []

for test_case in dataset.test_cases:
    metric.measure(test_case)
    score_dict = {
        'test_case': test_case,
        'score': metric.score,
        'reason': metric.reason,
    }
    evaluation_results.append(score_dict)
    print(metric.score)
    print(metric.reason)


with open('evaluation_results.json', 'w') as file:
    file.write(json.dumps(evaluation_results, indent=4))
