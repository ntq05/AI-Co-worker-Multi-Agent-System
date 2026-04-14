from pydantic import PrivateAttr
import os

from langchain_openai import ChatOpenAI

class OpenRouterLLM(ChatOpenAI):

    def __init__(self, model: str = os.getenv("MODEL", "nvidia/nemotron-3-super-120b-a12b:free"),
                 temperature: float = 0.7, max_tokens = 300):
        super().__init__(model = model,
                         temperature = temperature,
                         max_tokens = max_tokens,
                         openai_api_key = os.getenv("OPENROUTER_API_KEY"),
                         openai_api_base = "https://openrouter.ai/api/v1",
                         default_headers = {
                            "Content-Type": "application/json",
                            "HTTP-Referer": "http://localhost:3000",
                            "X-Title": "AI-Coworker-Engine"
                         })

    @property
    def _llm_type(self) -> str:
        return "nvidia/nemotron-3-super-120b-a12b:free"