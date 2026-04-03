# Module 5 Exercise — Data Management & CQRS

## CQRS in order-service

The order-service already implements the CQRS pattern:
- **Write side**: PostgreSQL via SQLAlchemy (commands: create order, update status)
- **Read side**: Redis projections (queries: order summary, user order list)

### Task 1: Verify the pattern
1. Create an order → it writes to PostgreSQL AND Redis
2. `GET /v1/orders/{id}/summary` — served from Redis (fast, denormalized)
3. `GET /v1/orders/{id}` — served from PostgreSQL (authoritative, full data)

Benchmark the difference:
```bash
# Install hey (HTTP load tool)
# Read model (Redis)
hey -n 1000 -c 50 http://localhost:8003/v1/orders/{id}/summary

# Write model (PostgreSQL)
hey -n 1000 -c 50 http://localhost:8003/v1/orders/{id}
```

### Task 2: Event Sourcing exploration
Instead of storing the current state, store events as the source of truth.

Add an `order_events` table:
```python
class OrderEvent(Base):
    __tablename__ = "order_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[str] = mapped_column(Text)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

Implement `replay_order_state(order_id)` that reconstructs order state from events.

### Task 3: Kafka as event log
Add a Kafka consumer in order-service that reads its own `order.placed` events and
rebuilds a separate analytics projection (e.g., daily order totals in Redis).

## Discussion
- What is the difference between CQRS and Event Sourcing?
- When does eventual consistency become a problem for the user experience?
- How would you handle schema evolution in Kafka events?
