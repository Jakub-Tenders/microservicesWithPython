# Module 4 Exercise — Asynchronous Messaging

> **First Docker module!** From now on, you'll use `docker-compose.infra.yml` for Kafka and RabbitMQ. Your Python services still run locally with uvicorn.

## Setup
```bash
# Start messaging infrastructure
docker compose -f docker-compose.infra.yml up -d rabbitmq zookeeper kafka
```

## Part A: RabbitMQ — Activity → Notification

### Task
When an activity is logged, publish a notification event to RabbitMQ.

Add to `services/activity-service/app/infrastructure/rabbitmq_publisher.py`:
```python
import json
import aio_pika
from app.config import settings


async def publish_activity_notification(activity_id: str, user_id: str, action: str) -> None:
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            "gamehub", aio_pika.ExchangeType.TOPIC, durable=True
        )
        message = aio_pika.Message(
            body=json.dumps({
                "type": "activity_notification",
                "recipient": user_id,
                "activity_id": activity_id,
                "action": action,
            }).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await exchange.publish(message, routing_key="notification.activity")
```

Call this from `create_activity` in `activity-service/app/main.py`.

### Verification
1. Log an activity via POST /v1/activities
2. Check RabbitMQ management UI at http://localhost:15672
3. Watch notification-service logs (running locally with Node.js on port 8004)
4. Check notification-service SQLite DB for stored notifications

## Part B: Kafka — Activity → Logging

The logging-service consumes `activity.logged` Kafka events and records them (with GDPR consent check).

### Task: Trigger and verify
1. Ensure the user has given GDPR consent: `POST /v1/consent/{user_id}` on logging-service
2. Log an activity referencing that user
3. Verify the logging-service received and stored the event

### Kafka CLI tools (run inside kafka container)
```bash
# List topics
docker exec -it <kafka-container> kafka-topics --bootstrap-server localhost:9092 --list

# Consume messages
docker exec -it <kafka-container> kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic activities --from-beginning

# Check consumer group lag
docker exec -it <kafka-container> kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group logging-service
```

## Discussion
- What happens if logging-service is down when an activity is logged?
- What is the difference between a Kafka consumer group and a RabbitMQ competing consumer?
- When would you use a Dead Letter Queue?
