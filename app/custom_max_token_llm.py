from langchain.llms.base import LLM
from pydantic import Field
from typing import Optional


class CustomMaxTokenLLM(LLM):
    llm: LLM
    max_tokens: int = Field(
        ..., description='Maximum number of tokens for the output'
    )

    def __init__(self, llm: LLM, max_tokens: int):
        # Initialize the LLM with given parameters
        super().__init__(llm=llm, max_tokens=max_tokens)

    def _call(self, prompt: str, stop: Optional[list] = None) -> str:
        # This method is deprecated; use invoke instead
        response = self.invoke(prompt, stop=stop)
        return self._trim_to_punctuation(response)

    def _trim_to_punctuation(self, text: str) -> str:
        # Find the last punctuation mark within the max_tokens length
        punctuation_marks = ['.', '!', '?']
        trimmed_text = text[: self.max_tokens]

        # Reverse the string to find the last punctuation
        last_punctuation_index = max(
            trimmed_text.rfind(punc) for punc in punctuation_marks
        )

        if last_punctuation_index != -1:
            return trimmed_text[: last_punctuation_index + 1]
        else:
            return (
                trimmed_text  # Return the full text if no punctuation is found
            )

    def invoke(self, input: str, stop: Optional[list] = None) -> str:
        # Ensure max_tokens is passed to the LLM invoke method
        response = self.llm.invoke(
            input=input, stop=stop, max_tokens=self.max_tokens
        )
        return self._trim_to_punctuation(response)

    @property
    def _llm_type(self) -> str:
        return 'custom_max_token_llm'

    async def _acall(self, prompt: str, stop: Optional[list] = None) -> str:
        raise NotImplementedError('This LLM does not support async operations.')
