from pydantic.v1 import BaseModel, Field
from typing import Literal, List

class RouterDecision(BaseModel):
    next_agent: List[Literal["CEO", "CHRO"]] = Field(
        default_factory = list,
        description="List of agents that should respond. Empty list means FINISH"
    )

    reasoning: str = Field(description = "Brief explanation of why these agents were chosen")