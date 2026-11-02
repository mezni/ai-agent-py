# Synthetic Data Fixtures

This directory contains synthetic JSON records used by the initial Plain Python implementation.

## Files

- `customers.json`
- `orders.json`
- `tickets.json`

Fixture records must conform to the canonical data contracts in `ai-agent-shared`.

## Expected JSON Shapes

### customers.json

A JSON array of objects containing:

- `customer_id`
- `email`

### orders.json

A JSON array of objects containing:

- `order_id`
- `customer_id`
- `order_date` — ISO 8601 calendar date (`YYYY-MM-DD`)
- `status` — canonical `OrderStatus`
- `total_amount` — numeric or string decimal amount
- `currency` — ISO currency code; defaults to CAD if omitted

### tickets.json

A JSON array of objects containing:

- `ticket_id`
- `customer_id`
- `subject`
- `description`
- `status` — canonical `TicketStatus`

## Data Rules

- Use synthetic records only.
- Do not add real customer information.
- Keep enum values aligned with the shared domain model.
- Do not store authoritative refund eligibility decisions in fixtures.
- The domain policy service computes refund eligibility.
- Keep fixture data versioned and traceable to the shared synthetic dataset.

The initial implementation is read-only. Repository adapters do not write or modify fixture files.
