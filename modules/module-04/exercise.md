# Module 4 Exercise — Asynchronous Messaging

## Part A: RabbitMQ — Order → Notification

### Task
When an order is placed, publish a notification event to RabbitMQ.

Add to `services/order-service/app/infrastructure/rabbitmq_publisher.py`:
```python
import json
import aio_pika
from app.config import settings


async def publish_order_notification(order_id: str, user_id: str, total: str) -> None:
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            "shopmicro", aio_pika.ExchangeType.TOPIC, durable=True
        )
        message = aio_pika.Message(
            body=json.dumps({
                "type": "order_confirmation",
                "recipient": user_id,
                "order_id": order_id,
                "total": total,
            }).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await exchange.publish(message, routing_key="notification.order")
```

Call this from `create_order` in `order-service/app/main.py`.

### Verification
1. Place an order via POST /v1/orders
2. Check RabbitMQ management UI at http://localhost:15672
3. Watch notification-service logs: `docker logs -f <container>`
4. Check MongoDB: `docker exec -it <mongo> mongosh notification_db --eval "db.notifications.find()"`

## Part B: Kafka — Order → Inventory

The inventory-service already consumes `order.placed` Kafka events.

### Task: Trigger and verify
1. Add a product to inventory: `POST /v1/inventory`
2. Place an order referencing that product
3. Verify stock decremented: `GET /v1/inventory/{product_id}`

### Kafka CLI tools (run inside kafka container)
```bash
# List topics
kafka-topics --bootstrap-server localhost:9092 --list

# Consume messages
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic orders --from-beginning

# Check consumer group lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group inventory-service
```

## Discussion
- What happens if inventory-service is down when an order is placed?
- What is the difference between a Kafka consumer group and a RabbitMQ competing consumer?
- When would you use a Dead Letter Queue?
