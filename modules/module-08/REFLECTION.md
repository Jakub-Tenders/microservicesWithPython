# Module 8 — Reflection

**Team name**: _______________
**Branch**: `module-08/<team-name>`
**Submitted**: before the final session

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

For seven modules, services ran locally with `uvicorn` and SQLite. Now they run in Docker with PostgreSQL.

**What concrete problem does packaging a service in a container solve — that "it works on my machine" never could?**

Think about what a container actually guarantees, and what it means for a teammate who clones your repo on a different OS.

> *Your answer:*

---

## 2. Your choice

Every Python service is containerised. `notification-service` is not — it keeps running locally with Node.js.

**Why was that decision made? What does it tell you about the relationship between containerisation and polyglot architecture?**

Is this a temporary shortcut or a legitimate design choice? Defend your position.

> *Your answer:*

---

## 3. The tradeoff

Moving from SQLite to PostgreSQL in a container is not just a config change. Schema migrations, connection strings, and environment variables all need to be coordinated.

**What gets harder when you containerise a service that has a database?**

Think about the lifecycle: first deploy, schema update, rollback. Where are the new failure points?

> *Your answer:*

---

*Keep this file. You will refer back to it during the oral presentation.*
