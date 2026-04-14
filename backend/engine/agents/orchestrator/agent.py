from engine.agents.base import BaseAgent
from langchain.prompts import ChatPromptTemplate
from engine.tools.registry import BUSINESS_TOOLS
from langchain_core.messages import AIMessage

class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent:
    - Assign task for appropriate agent
    - Reassing task if the output of an agent is not appropriate
    """

    def __init__(self, config_path: str = None):
        super().__init__(name = "Orchestrator", config_path=config_path)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt_template),
            ("human", "{user_input}"),
        ])

        self.llm_with_tools = self.llm_client.bind_tools(BUSINESS_TOOLS)

        self.chain = self.prompt | self.llm_with_tools
    def respond(self, user_input: str, chat_history: str):

        prompt_inputs = {
            "user_input": user_input,
            "chat_history": chat_history,
        }

        response = self.chain.invoke(prompt_inputs)

        print(f"[DEBUG] {self.name}'s response: {response}")

        return response