from pydantic import BaseModel, ConfigDict


class GetOrderStatusArguments(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    order_id: str


class GetCustomerArguments(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    customer_id: str


class SearchFAQArguments(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    query: str
