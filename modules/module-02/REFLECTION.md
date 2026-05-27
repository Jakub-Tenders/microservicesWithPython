# Module 2 — Reflection

**Team name**: _______________
**Branch**: `module-02/<team-name>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> *Your answer:*
Because after some time one big file becomes unreadable
With layers each part has one job so changes are safer
If we move from SQLite to PostgreSQL we mostly change repository and config, not everything

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> *Your answer:*
Game service owns the Game table
If another service writes directly, it can create invalid game states like negative scores or wrong status
Then API responses become inconsistent and bugs are hard to trace

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> *Your answer:*
For a small project the cost is more files and more boilerplate
It feels slower at first for simple CRUD
It starts paying off when features grow and more people work on the same service

---

*Keep this file. You will refer back to it during the oral presentation.*
