# Module 5 — Reflection

**Team name**: _______________
**Branch**: `module-05/<team-name>`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> *Your answer: sqlite is fine for writes but if you hammer it with thousands of reads it slows down. redis keeps the summary in memory so reads are instant. basically each model does what it's good at instead of one trying to do everything*

---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> *Your answer:it means your data is incomplete on purpose, if someone didn't consent you just don't have their logs. we put the check in logging-service because that's the one actually writing the logs, putting it in the gateway or activity-service makes no sense they don't care about consent*

---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> *Your answer:it matters if a user updates something and immediately sees the old data, that's just confusing. but if it's a game summary that barely changes a few seconds of lag is fine nobody notices. banking or medical stuff though you can't do eventual consistency there, stale data could cause real problems*

---

*Keep this file. You will refer back to it during the oral presentation.*
