from pydantic import BaseModel, EmailStr, Field


class LoginBalanceRequest(BaseModel):
    login: int
    initial_balance: float
