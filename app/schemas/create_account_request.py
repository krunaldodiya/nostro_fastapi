from pydantic import BaseModel, EmailStr, Field


class CreateAccountRequest(BaseModel):
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    group: str = Field(..., description="Trading account group")
    initial_balance: float = Field(..., gt=0, description="Initial account balance")
    initial_target: float = Field(..., gt=0, description="Initial target amount")
    leverage: int = Field(..., gt=0, description="Account leverage")
