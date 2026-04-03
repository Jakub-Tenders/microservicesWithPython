# Module 1 Exercise — Service Decomposition

## Scenario: Legacy Gamer Social Monolith

You are given a monolithic gamer social platform with the following capabilities bundled together:
- User registration & authentication
- Game library management
- Activity tracking & social feed
- Push & in-app notifications
- GDPR-compliant activity logging
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
| Game Library | ... | ... | ... |
| ... | | | |

## Task 2: Define Service Contracts (20 min)

For each pair of services that need to communicate, define:
- **Direction**: A → B
- **Trigger**: what event/action causes the call
- **Protocol**: REST / gRPC / Event
- **Payload**: key fields

Example:
```
activity-service → logging-service
Trigger: Activity logged
Protocol: Kafka event (async preferred — why?)
Payload: { activity_id, user_id, action, game_id, timestamp }
```

## Task 3: GameHub Service Map

Based on the GameHub capstone, draw the final service map:
- List each service
- Draw communication arrows (solid = sync, dashed = async)
- Label each arrow with protocol

Reference the table in the course README for the final answer.

## Discussion Questions

1. Why does `notification-service` use Node.js + SQLite instead of Python + PostgreSQL?
2. What is the risk of `activity-service` calling `logging-service` synchronously?
3. How does Conway's Law apply to your team structure decisions above?
4. The CAP theorem says you can't have Consistency + Availability + Partition tolerance simultaneously. For each service in GameHub, which two do you prioritise and why?
5. Why does the `logging-service` need a GDPR consent check before recording activity?
