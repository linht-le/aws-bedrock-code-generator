from pydantic import BaseModel


class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


class ChatResponse(BaseModel):
    response: str | None
    usage: dict[str, int] | None
    error: str | None = None
    success: bool
