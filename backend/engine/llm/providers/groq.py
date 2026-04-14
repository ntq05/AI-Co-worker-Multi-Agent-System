from langchain_core.language_models.llms import LLM
from typing import Optional, List
from engine.llm.client import LLMClient
from pydantic import PrivateAttr

class GroqLLM(LLM):
    _client: LLMClient = PrivateAttr(default=None)

    def __init__(self, model: str = "groq", temperature: float = 0.7, max_tokens = 300):
        super().__init__()
        object.__setattr__(self, "_client", LLMClient(model=model, temperature=temperature, max_tokens=max_tokens))

    @property
    def client(self) -> LLMClient:
        return self._client

    @property
    def _llm_type(self) -> str:
        return "groq"
    
    def _call(self, prompt:str, stop: Optional[List[str]] = None) -> str:
        return self.client.generate(prompt)