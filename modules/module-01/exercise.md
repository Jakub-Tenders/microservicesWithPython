# Module 1 Exercise — Service Decomposition

## Scenario: Legacy E-Commerce Monolith

You are given a monolithic e-commerce application with the following capabilities bundled together:
- User registration & authentication
- Product catalogue management
- Shopping cart & order placement
- Inventory tracking
- Email & SMS notifications
- Payment processing
- Reporting & analytics

## Task 1: Identify Bounded Contexts (30 min)

For each bounded context, define:
1. **Name** — what business domain it represents
2. **Responsibilities** — what it owns
3. **Data** — which entities it owns exclusively
4. **Team ownership** — which team would own this service

Use the template below:

| Bounded Context | Responsibilities | Owned Entities | Team |
|---|---|---|---|
| Identity | ... | User, Session | Platform |
| Catalogue | ... | ... | ... |
| ... | | | |

## Task 2: Define Service Contracts (20 min)

For each pair of services that need to communicate, define:
- **Direction**: A → B
- **Trigger**: what event/action causes the call
- **Protocol**: REST / gRPC / Event
- **Payload**: key fields

Example:
```
order-service → inventory-service
Trigger: Order placed
Protocol: Kafka event (async preferred — why?)
Payload: { order_id, items: [{product_id, quantity}] }
```

## Task 3: ShopMicro Service Map

Based on the ShopMicro capstone, draw the final service map:
- List each service
- Draw communication arrows (solid = sync, dashed = async)
- Label each arrow with protocol

Reference the table in the course README for the final answer.

## Discussion Questions

1. Why does `notification-service` use MongoDB instead of PostgreSQL?
2. What is the risk of `order-service` calling `inventory-service` synchronously?
3. How does Conway's Law apply to your team structure decisions above?
4. The CAP theorem says you can't have Consistency + Availability + Partition tolerance simultaneously. For each service in ShopMicro, which two do you prioritise and why?
