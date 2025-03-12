from pydantic import BaseModel


class ChangeGroupRequest(BaseModel):
    login: int
    group: str
