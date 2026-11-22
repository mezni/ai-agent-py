CUSTOMERS = {
    "C100": {
        "customer_id": "C100",
        "name": "Alice",
        "email": "alice@example.com",
    },
    "C200": {
        "customer_id": "C200",
        "name": "Bob",
        "email": "bob@example.com",
    },
}


def get_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "found": False,
            "customer_id": customer_id,
        }

    return {
        "found": True,
        "customer": customer,
    }
