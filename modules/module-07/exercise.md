# Module 7 Exercise — API Design & Documentation

## Part A: Versioning
All ShopMicro services use URL versioning (`/v1/`).

### Task: Add v2 endpoint with breaking change
In product-service, add a `/v2/products` endpoint that returns a flattened response
(no nesting, camelCase field names) to demonstrate backward-incompatible changes.

Keep `/v1/products` working. Both versions must be documented in OpenAPI.

```python
@app.get("/v2/products", tags=["v2"])
async def list_products_v2(...):
    # Returns camelCase, different shape
    ...
```

## Part B: Generate a Python client SDK

```bash
# Install OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Start product-service
uvicorn app.main:app --port 8002

# Download spec
curl http://localhost:8002/openapi.json -o product-service-openapi.json

# Generate Python client
openapi-generator-cli generate \
  -i product-service-openapi.json \
  -g python \
  -o ./generated-clients/product-client \
  --additional-properties=packageName=product_client
```

## Part C: Contract tests
Write tests using the generated client against the live service:

```python
import pytest
from product_client import ApiClient, Configuration, ProductsApi

@pytest.fixture
def api():
    config = Configuration(host="http://localhost:8002")
    return ProductsApi(ApiClient(config))

def test_list_products_contract(api):
    products = api.list_products_v1_products_get()
    assert hasattr(products, 'items')
    assert hasattr(products, 'total')
    assert isinstance(products.items, list)
```

## Discussion
- What is the difference between API versioning strategies?
  - URL path (`/v1/`, `/v2/`)
  - Request header (`Accept: application/vnd.shopmicro.v2+json`)
  - Query parameter (`?version=2`)
- When should you bump the major version?
