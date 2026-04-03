# Module 7 Exercise — API Design & Documentation

## Part A: Versioning
All GameHub services use URL versioning (`/v1/`).

### Task: Add v2 endpoint with breaking change
In game-service, add a `/v2/games` endpoint that returns a flattened response
(no nesting, camelCase field names) to demonstrate backward-incompatible changes.

Keep `/v1/games` working. Both versions must be documented in OpenAPI.

```python
@app.get("/v2/games", tags=["v2"])
async def list_games_v2(...):
    # Returns camelCase, different shape
    ...
```

## Part B: Generate a Python client SDK

```bash
# Install OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Start game-service
uvicorn app.main:app --port 8002

# Download spec
curl http://localhost:8002/openapi.json -o game-service-openapi.json

# Generate Python client
openapi-generator-cli generate \
  -i game-service-openapi.json \
  -g python \
  -o ./generated-clients/game-client \
  --additional-properties=packageName=game_client
```

## Part C: Contract tests
Write tests using the generated client against the live service:

```python
import pytest
from game_client import ApiClient, Configuration, GamesApi

@pytest.fixture
def api():
    config = Configuration(host="http://localhost:8002")
    return GamesApi(ApiClient(config))

def test_list_games_contract(api):
    games = api.list_games_v1_games_get()
    assert hasattr(games, 'items')
    assert hasattr(games, 'total')
    assert isinstance(games.items, list)
```

## Discussion
- What is the difference between API versioning strategies?
  - URL path (`/v1/`, `/v2/`)
  - Request header (`Accept: application/vnd.gamehub.v2+json`)
  - Query parameter (`?version=2`)
- When should you bump the major version?
