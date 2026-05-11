# Module 7 — API Design & Versioning

**Duration**: 2h in class
**Branch to submit**: `module-07/<team-name>`

---

## Objective

APIs are contracts. Once a client depends on a response shape, you cannot change it without breaking them. This module explores what versioning looks like in practice — not in theory — by building a breaking change into a live system and writing tests that prove the contract still holds.

---

## Part A — Add a v2 endpoint with a breaking change *(~40 min)*

In `game-service`, add a `/v2/games` endpoint that returns a **different shape** from `/v1/games`.

The v2 shape uses camelCase keys and no nested objects:
```json
{ "gameId": "...", "gameTitle": "...", "platform": "PC", "releaseYear": 2024 }
```

The v1 shape stays exactly as it is — do not touch it.

Both versions must appear in the OpenAPI docs at `http://localhost:8002/docs`.

Before implementing, answer these two questions for yourself (you will use them in REFLECTION.md):
- What makes this a *breaking* change? What client code would fail if you applied this shape to `/v1/games`?
- When is the right moment to bump the major version rather than adding a new optional field?

---

## Part B — Contract tests *(~45 min)*

A contract test does not test business logic — it tests that the API shape has not changed in a way that would break a caller.

Write the three tests below in `modules/module-07/test_contracts.py`. Run them against the gateway (port 8000), not the service directly — this also validates that routing still works end-to-end.

The test file skeleton is provided in `modules/module-07/test_contracts.py`. Fill in the assertions:

1. **`test_v1_games_shape`** — verify the v1 response has `items` (list) and `total` (int)
2. **`test_v2_games_shape`** — verify the v2 response items have `gameId` and `gameTitle`, and do NOT have `id`
3. **`test_v1_and_v2_same_count`** — verify both versions return the same number of games

```bash
pytest modules/module-07/test_contracts.py -v
```

All three tests must pass before you submit the branch.

---

## Discussion *(~20 min)*

- URL versioning (`/v1/games`), header versioning (`Accept: application/vnd.gamehub.v2+json`), query param versioning (`?version=2`) — what is different about each? Why does URL versioning win for most teams?
- Your tests verify the shape. What would you test if you also wanted to verify the gateway routing logic (e.g. that `/v3/games` returns 404)?
- At what point is it safe to delete `/v1/games`? What signals would tell you?

---

## Minimum to submit this branch

- [ ] `/v2/games` endpoint working and returning camelCase shape
- [ ] `/v1/games` still returns the original shape, untouched
- [ ] All 3 contract tests passing against the gateway
- [ ] `REFLECTION.md` completed and committed

---

## Optional — Version-aware gateway

If you finish early, extend the gateway to reject unsupported versions with a clear error message. Define a `SUPPORTED_VERSIONS` dictionary per resource, and return `404 "v3/games is not supported"` for unknown versions. This centralises version management in one place rather than letting each service handle it.
