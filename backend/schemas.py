from pydantic import BaseModel


class URLRequest(BaseModel):
    url: str


class MessageRequest(BaseModel):
    message: str