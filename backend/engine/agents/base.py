from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import yaml
import uuid
from engine.llm.providers.openRouter import OpenRouterLLM

from langchain_core.messages import AIMessage

import os

class BaseAgent(ABC):
    """
    Base class for all AI Agents
    Handles:
    - Persona, goal, contraints
    - Memory (short-term)
    - LLM interactions
    """

    def __init__(self, name: str, config_path: Optional[str] = None):
        self.name = name
        self.config = self.load_config(config_path) if config_path else {}

        # self.override_with_env()

        self.persona = self.config.get("persona", [])
        self.goal = self.config.get("goal", "")
        self.constraints = self.config.get("constraints", [])
        self.knowledge_scope = self.config.get("knowledge_scope", "")

        # LLM client
        self.llm_client = OpenRouterLLM(
            model = self.config.get("model", "nvidia/nemotron-3-super-120b-a12b:free"),
            temperature = self.config.get("temperature", 0.7),
            max_tokens = self.config.get("max_tokens", 300)
        )

        # Prompt template
        self.prompt_template = self.load_prompt(self.config.get("prompt_path"))

    # prioritize using model from .env
    def override_with_env(self):
        env_model = os.getenv("MODEL")
        if env_model:
            self.config["model"] = env_model
    
    def load_config(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
    def load_prompt(self, path: Optional[str]) -> str:
        if path:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    
    @abstractmethod
    def respond(self, user_input: str, chat_history: str) -> str:
        """
        Core method to generate response
        Must be implemented by subclass
        """

        pass

    def to_node(self):
        def node(state: Dict[str, Any]):
            summary = state.get("summary", "")

            user_question = ""
            for msg in reversed(state["messages"]):
                if msg.type == "human":
                    user_question = msg.content
                    break

            context_list = []

            if summary:
                context_list.append(f"--- PREVIOUS CONTEXT SUMMARY ---\n{summary}\n--- END OF SUMMARY ---")

            for msg in state["messages"]:
                name = getattr(msg, "name", msg.type)
                if msg.content:
                    context_list.append(f"{name}: {msg.content}")

            current_context = "\n".join(context_list)

            print(f"DEBUG Agent {self.name} processing with context length: {len(context_list)}")
            response = self.respond(user_input=user_question, chat_history=current_context)

            msg_id = str(uuid.uuid4())

            if self.name.lower() == "orchestrator":
                if hasattr(response, "id"):
                    response.id = msg_id
                return {"messages": [response], "active_agent": self.name}
            else:
                new_message = AIMessage(
                    content=str(response), 
                    name=self.name, 
                    id=msg_id
                )
                return {"messages": [new_message], "active_agent": self.name}
        return node
    
