from pydantic import BaseModel, Field


class TradeAccountGroupRequest(BaseModel):
    group: str = Field(..., description="Group name")
