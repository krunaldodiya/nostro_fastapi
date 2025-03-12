from pydantic import BaseModel


class CreateAccountResponse(BaseModel):
    data: dict
    success: bool
    message: str
