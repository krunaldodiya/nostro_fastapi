from pydantic import BaseModel, EmailStr, Field


class UserUpdateRequest(BaseModel):
    login: int
    comment: str
    color: int
