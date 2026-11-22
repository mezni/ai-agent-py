ORDERS = {
    "4821": {
        "order_id": "4821",
        "status": "shipped",
        "tracking_number": "TRK-10001",
    },
    "4822": {
        "order_id": "4822",
        "status": "processing",
        "tracking_number": None,
    },
    "4823": {
        "order_id": "4823",
        "status": "delivered",
        "tracking_number": "TRK-10003",
    },
}


def get_order_status(order_id: str) -> dict:
    order = ORDERS.get(order_id)

    if order is None:
        return {
            "found": False,
            "order_id": order_id,
        }

    return {
        "found": True,
        "order": order,
    }
