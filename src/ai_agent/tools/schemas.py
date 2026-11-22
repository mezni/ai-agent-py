from pydantic import BaseModel, ConfigDict


class GetOrderStatusArguments(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    order_id: str
