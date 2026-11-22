GET_ORDER_STATUS_TOOL = {
    "type": "function",
    "name": "get_order_status",
    "description": "Retrieve the current status of a customer order.",
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


GET_CUSTOMER_TOOL = {
    "type": "function",
    "name": "get_customer",
    "description": "Retrieve customer information using a customer ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The customer identifier.",
            },
        },
        "required": ["customer_id"],
        "additionalProperties": False,
    },
    "strict": True,
}


SEARCH_FAQ_TOOL = {
    "type": "function",
    "name": "search_faq",
    "description": "Search support FAQs for relevant information.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The question or search query.",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True,
}


TOOLS = [
    GET_ORDER_STATUS_TOOL,
    GET_CUSTOMER_TOOL,
    SEARCH_FAQ_TOOL,
]
