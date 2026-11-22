from pydantic import BaseModel


class ModelRequest(BaseModel):
    message: str
    instructions: str = "You are a helpful assistant."
    model: str | None = None
    max_output_tokens: int = 1000


class ModelResponse(BaseModel):
    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
