from engine.agents.base import BaseAgent
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import RemoveMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from engine.state import AgentState

class SummarizerAgent(BaseAgent):

    def __init__(self, config_path: str = None):
        super().__init__(name = "Summarizer", config_path = config_path)
        self.prompt = ChatPromptTemplate.from_messages({
            ("system", self.prompt_template),
            ("human", "{user_input}")
        })

        self.chain = self.prompt | self.llm_client | StrOutputParser()

        
    def respond(self, user_input: str, chat_history: str, existing_summary: str = "") -> str:

        prompt_inputs = {
            "user_input": user_input,
            "chat_history":  chat_history,
            "summary": existing_summary,
            "goal": self.goal,
            "constraints": ",".join(self.constraints),
        }

        response = self.chain.invoke(prompt_inputs)

        return response.strip()
    
    def to_node(self):
        async def node(state: AgentState):

            messages = state["messages"]
            existing_summary = state.get("summary", "")

            if len(messages) <= 10:
                return {}
            
            messages_to_archive = messages[:-3]
            chat_history_str = "\n".join([f"{m.type}: {m.content}" for m in messages_to_archive])

            new_summary_text = self.respond(
                user_input = "Update the summary with new information.",
                chat_history=chat_history_str,
                existing_summary=existing_summary
            )

            delete_instructions = []
            for m in messages_to_archive:
                if hasattr(m, "id") and m.id:
                    delete_instructions.append(RemoveMessage(id=m.id))

            print(f"--- [SUMMARIZER] Archiving {len(delete_instructions)} messages ---")

            return {
                "summary": new_summary_text,
                "messages": delete_instructions
            }
        return node