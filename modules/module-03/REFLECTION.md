# Module 3 — Reflection

**Team name**: _______________
**Branch**: `module-03/<team-name>`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:*

Without the gateway, the frontend would have to go thru a messy list of different ports for every single service, meaning any minor backend tweak would immediately break the client. Routing everything through localhost:8000 keeps life simple: the frontend only needs to know one address

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:*
An activity must belong to a real user, so that validation call is critical and worth retrying to avoid saving corrupt data the activity can still be valid even if game-service is down. "game": null is better than failing the whole request. The user can still log the activity.
---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:*
The risk is a domino effect: you're only as strong (and as fast) as your weakest link. If one service goes down, the whole request fails.

---

*Keep this file. You will refer back to it during the oral presentation.*
