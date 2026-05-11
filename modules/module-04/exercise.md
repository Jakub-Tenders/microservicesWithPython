# Module 4 — Asynchronous Messaging

**Duration**: 2h in class
**Branch to submit**: `module-04/<team-name>`

---

## Objective

Until now, services communicated synchronously — one service called another and waited for a reply. This module introduces asynchronous messaging: a service drops a message into a broker and moves on, without waiting for any response.

You will wire two messaging flows into the system: one using RabbitMQ (push notifications), one using Kafka (activity logging). The infrastructure (brokers, containers) is already running — the instructor started it before the lesson.

---

## What's provided

- RabbitMQ and Kafka are running via Docker. You do not need to configure them.
- The publisher functions are scaffolded in `activity-service` — the connection logic is done, you fill in the call sites.
- `notification-service` is already built (Node.js) and running on port 8004.
- RabbitMQ management UI: http://localhost:15672 (guest / guest)

---

## Part A — RabbitMQ: activity → notification *(~40 min)*

When a user logs an activity, a notification should be sent to `notification-service` via RabbitMQ.

Open `services/activity-service/app/infrastructure/rabbitmq_publisher.py` — the publisher is already implemented. Your job is to **call it** from the right place in `create_activity`.

After wiring it up:
1. Log an activity through the gateway: `POST http://localhost:8000/v1/activities`
2. Open the RabbitMQ UI at http://localhost:15672 — find the `gamehub` exchange and confirm a message was published
3. Check the `notification-service` logs — a notification should appear

---

## Part B — Kafka: activity → logging *(~30 min)*

Every activity should also publish an event to Kafka. The `logging-service` will consume it in Module 5 — for now, verify the event is landing in the topic.

The Kafka publisher is scaffolded in `activity-service`. Wire it into `create_activity` alongside the RabbitMQ call.

Verify the event reached Kafka:
```bash
docker exec -it <kafka-container> kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic activities \
  --from-beginning
```

You should see the event your activity-service published. If the topic is empty, the publisher is not being called.

---

## Part C — Register notification-service in the gateway *(~15 min)*

`notification-service` is now part of the system. Add it to the gateway's routing table.

In `gateway/app/config.py` and `gateway/app/main.py`, follow the same pattern you used in Module 3 for the other services. `notification-service` runs on port 8004.

Verify:
```bash
curl http://localhost:8000/v1/notifications
```

---

## Discussion *(~15 min)*

- What happens to the activity request if `notification-service` is down? Should it fail or succeed?
- RabbitMQ delivers each message to one consumer. Kafka lets multiple consumers read the same message independently. Why does that distinction matter for our two flows — notifications vs. logging?
- If an event is published to Kafka but `logging-service` is down for an hour, what happens when it comes back up?

---

## Minimum to submit this branch

- [ ] Activity creation publishes a RabbitMQ message — visible in the management UI
- [ ] Activity creation publishes a Kafka event — visible via the CLI consumer
- [ ] `notification-service` registered in the gateway and reachable via port 8000
- [ ] `REFLECTION.md` completed and committed
