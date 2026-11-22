GET_ORDER_STATUS_TOOL = {
    "type": "function",
    "name": "get_order_status",
    "description": (
        "Retrieve the current status of a customer order. "
        "Use this tool when the customer asks about an order "
        "and an order ID is available."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The customer order identifier.",
            },
        },
        "required": ["order_id"],
        "additionalProperties": False,
    },
    "strict": True,
}
