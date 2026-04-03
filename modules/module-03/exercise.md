# Module 3 Exercise — Synchronous Communication

## Part A: REST (httpx)

The order-service needs to validate that a user exists before creating an order.

### Task 1: Add user validation in order-service
In `services/order-service/app/main.py`, before creating an order:

```python
import httpx
from app.config import settings

async def validate_user_exists(user_id: str) -> bool:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{settings.user_service_url}/v1/users/{user_id}")
            return resp.status_code == 200
        except httpx.RequestError:
            return False
```

Add a 404 response if the user doesn't exist.

### Task 2: Add timeout + retry with tenacity
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(httpx.TransientError),
)
async def validate_user_exists(user_id: str) -> bool:
    ...
```

## Part B: gRPC (Bonus)

Rewrite the user validation call using gRPC.

### Step 1: Define the protobuf contract
Create `services/user-service/proto/user.proto`:
```protobuf
syntax = "proto3";
package user;

service UserService {
  rpc GetUser (GetUserRequest) returns (UserReply);
}

message GetUserRequest {
  string user_id = 1;
}

message UserReply {
  string id = 1;
  string email = 2;
  bool is_active = 3;
}
```

### Step 2: Generate Python stubs
```bash
python -m grpc_tools.protoc -I./proto --python_out=./app/grpc_generated \
  --grpc_python_out=./app/grpc_generated proto/user.proto
```

### Step 3: Add gRPC server to user-service
Add a gRPC server running alongside FastAPI on port 50051.

## Discussion
- When would you choose gRPC over REST?
- What are the trade-offs in terms of schema evolution?
