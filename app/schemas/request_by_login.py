from pydantic import BaseModel, Field


class BaseRequest(BaseModel):
    login: int = Field(..., gt=0, description="Account Login")
