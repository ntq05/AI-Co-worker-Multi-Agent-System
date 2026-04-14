from engine.agents.base import BaseAgent
from langchain.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

class ManagerAgent(BaseAgent):

    def __init__(self, config_path: str = None):
        super().__init__(name = "Manager", config_path = config_path)
        self.prompt = ChatPromptTemplate.from_messages({
            ("system", self.prompt_template),
            ("human", "{user_input}")
        })

        self.chain = self.prompt | self.llm_client | StrOutputParser()

        
    def respond(self, user_input: str, chat_history: str) -> str:

        prompt_inputs = {
            "user_input": user_input,
            "chat_history":  chat_history,
            "goal": self.goal,
            "constraints": ",".join(self.constraints),
            "knowledge_scope": self.knowledge_scope
        }

        response = self.chain.invoke(prompt_inputs)

        return response.strip()