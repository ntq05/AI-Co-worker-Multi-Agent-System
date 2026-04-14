from typing import Optional
import os
import requests

class LLMClient:
    """
    Wrapper LLM client
    """

    def __init__(self, model: str = os.getenv("MODEL", "nvidia/nemotron-3-super-120b-a12b:free"), temperature: float = 0.7, max_tokens: int = 300):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
    def generate(self, prompt: str) -> str:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "AI-Coworker-Engine"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        # API call
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers)

            if response.status_code != 200:
                print(f"[DEBUG] Response Content: {response.text}")

            response.raise_for_status()
            result = response.json()

            return result['choices'][0]['message']['content'].strip()
        
        except Exception as e:
            return f"Error connecting to OpenRouter: {str(e)}"
