from pydantic import BaseModel


class LoadingError(BaseModel):
    filename: str
    message: str
