from pydantic import BaseModel, Field


class EnableAccountRequest(BaseModel):
    login: int = Field(..., gt=0, description="Account Login")
    initial_balance: float = Field(..., gt=0, description="Initial account balance")
