from pydantic import BaseModel, EmailStr, Field


class LoginSymbolRequest(BaseModel):
    login: int
    symbol: str
