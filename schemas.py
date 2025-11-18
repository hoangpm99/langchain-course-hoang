from typing import List

from pydantic import BaseModel, Field


class Source(BaseModel):
    """Schema for the source used by the model"""

    """This is Pydantic model field declaration syntax. 
    It defines a field called url whose type is str, and it uses Field() to attach metadata or constraints."""
    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for the agent response with answer and sources"""

    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list,
        description="List of sources used by the agent to generate the answer",
    )
