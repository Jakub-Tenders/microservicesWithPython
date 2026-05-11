# Oral Presentation — Modules 9 & 10 + Full System Review

**Format**: 15 minutes per group, live, no slides required
**Whiteboard or live demo accepted**

---

## Structure

### Part 1 — System map (3 min)

Walk us through your architecture as it stands at the end of Module 8.

- Name each service and its single responsibility
- Identify which communication is synchronous (REST) and which is asynchronous (events)
- Show where the gateway sits and what it enforces

You should be able to do this without looking at the code.

---

### Part 2 — Defend two decisions (5 min)

Pick **any two** of your REFLECTION.md answers from modules 1–8. Read your answer out loud, then defend it.

We may push back. That is expected — there is no perfect answer. What matters is that you can explain your reasoning under mild pressure.

---

### Part 3 — Observability and resilience (5 min)

Modules 9 and 10 are about what happens when the system is running in production and something goes wrong.

Answer these questions — no code required, just your understanding:

**Observability (Module 9)**
- If a user reports that "logging an activity is slow", how would you find the cause? Which tool would you open first and what would you look for?
- What is the difference between a metric, a trace, and a log? Give one concrete example of each from GameHub.

**Resilience (Module 10)**
- The circuit breaker has three states: CLOSED, OPEN, HALF_OPEN. Explain what each state means in plain English — what is the system doing and why?
- The gateway has a `/health` endpoint that checks all downstream services. Who reads that endpoint and what do they do with it?

---

### Part 4 — Q&A (2 min)

Open questions from the instructor. Expect at least one question that was not covered above.

---

## Preparation checklist

Before the session, make sure you can:

- [ ] Draw the service map from memory (or explain it without the diagram)
- [ ] Re-read all 8 of your REFLECTION.md files — they are your preparation notes
- [ ] Explain the circuit breaker state machine in your own words
- [ ] Explain the difference between Kafka and RabbitMQ in one sentence each
- [ ] Know which service owns which data (no cross-service database access)

---

## What we are not testing

- Syntax. You will not be asked to write code.
- Memorised definitions. If you can explain it in your own words, that is enough.
- Perfect answers. Honest reasoning with acknowledged tradeoffs is better than a rehearsed response.
