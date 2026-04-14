from typing import List, Dict

class ShortTermMemory:
    """
    Store recent conversation for context
    """

    def __init__(self, agent_name: str, max_len: int = 5):
        self.agent_name = agent_name
        self.max_len = max_len
        self.entries: List[Dict[str, str]] = []

    def add_entry(self, user_input: str, agent_response: str):
        self.entries.append({"user": user_input, "agent": agent_response})
        if len(self.entries) > self.max_len:
            self.entries.pop(0)

    def get_recent_conversation(self) -> str:
        """
        Return a string of recent conversation for prompt context
        """
        if not self.entries:
            return ""
        
        conversation = ""
        for e in self.entries:
            conversation += f"User: {e['user']}\n{self.agent_name}: {e['agent']}\n"

        return conversation.strip()

