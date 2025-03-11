from pydantic import BaseModel


class CreateAccountResponse(BaseModel):
    login: int
    main_password: str
    investor_password: str
    success: bool
    message: str
