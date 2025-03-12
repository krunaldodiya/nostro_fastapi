from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    login: int
