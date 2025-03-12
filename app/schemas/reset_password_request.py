from pydantic import BaseModel


class ResetPasswordRequest(BaseModel):
    login: int
