# Module 7 — Reflection

**Team name**: _______________
**Branch**: `module-07/<team-name>`
**Submitted**: before Module 8 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You now have `/v1/games` and `/v2/games` running side by side, returning different shapes.

**Why does API versioning exist at all?** What breaks for a real client if you just change the response shape in place without versioning?

Think about a mobile app that was built against `/v1/games` six months ago and is still running on users' phones.

> *Your answer:*

---

## 2. Your choice

The course uses URL versioning: `/v1/`, `/v2/`. Other strategies exist — request headers (`Accept: application/vnd.gamehub.v2+json`) or query parameters (`?version=2`).

**Why does URL versioning win in practice for most teams?**

Think about who has to use the API: a developer writing a curl command, a browser making a fetch request, a gateway trying to route by path. Which strategy is easiest for all of them?

> *Your answer:*

---

## 3. The tradeoff

Keeping `/v1/` alive while building `/v2/` means you are maintaining two versions of the same logic indefinitely — until you decide to delete the old one.

**How do you decide when it is safe to delete `/v1/`?** What signals would you look for?

And what is the cost of keeping it around too long?

> *Your answer:*

---

*Keep this file. You will refer back to it during the oral presentation.*
