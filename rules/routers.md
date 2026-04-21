# FastAPI Router Rules

Apply these rules to every file under `app/routers/` and when registering routers in `app/main.py`.

---

## 1. One Router Per Domain

Each business domain gets its own file. Never mix domains in a single router file.

```
app/routers/
├── health.py        # liveness/readiness endpoints
├── users.py         # user CRUD
├── orders.py        # order management
└── test.py          # deployment verification UI
```

If a router file grows beyond 300 lines, split by sub-resource or action group:

```
app/routers/
├── users_read.py    # GET /users, GET /users/{id}
└── users_write.py   # POST /users, PUT /users/{id}, DELETE /users/{id}
```

---

## 2. Mandatory Route Decorator Fields

Every `@router.get/post/put/delete/patch` must include all three:

| Field | Required | Example |
|-------|----------|---------|
| `response_model` | Yes | `response_model=UserResponse` |
| `tags` | Yes | `tags=["users"]` |
| `status_code` | Yes for non-200 | `status_code=201` |

```python
@router.get(
    "/inventory-service/items/{item_id}",
    response_model=ItemResponse,
    tags=["items"],
)
def get_item(item_id: int) -> ItemResponse:
    """Fetch a single inventory item by ID.

    Args:
        item_id (int): The unique identifier of the item.

    Returns:
        ItemResponse: The matching item data.

    Raises:
        HTTPException: 404 if the item does not exist.
    """
```

---

## 3. URL Path Convention

All routes must be prefixed with the service name. This prevents path collisions when multiple services share an Ingress controller.

```
/{service-name}/{resource}
/{service-name}/{resource}/{id}
/{service-name}/{resource}/{id}/action
```

Examples for `inventory-service`:
```
GET  /inventory-service/items
GET  /inventory-service/items/{item_id}
POST /inventory-service/items
PUT  /inventory-service/items/{item_id}
```

---

## 4. Models Belong in `app/`, Not in Routers

Pydantic request/response models must live in `app/models.py` or `app/schemas/`. Router files only import and use them.

```python
# CORRECT — router imports model from app layer
from app.schemas.items import ItemResponse, CreateItemRequest

@router.post("/inventory-service/items", response_model=ItemResponse, tags=["items"], status_code=201)
def create_item(body: CreateItemRequest) -> ItemResponse:
    ...

# WRONG — model defined inside the router file
class ItemResponse(BaseModel):
    id: int
    name: str
```

---

## 5. Use the Structured Logger

Never use `print()` or `logging.getLogger()` directly in routers. Import the shared logger.

```python
from app.logger import logger

@router.get("/inventory-service/items", response_model=list[ItemResponse], tags=["items"])
def list_items() -> list[ItemResponse]:
    """List all available inventory items.

    Args:
        None

    Returns:
        list[ItemResponse]: All items currently in inventory.
    """
    logger.info("Listing all inventory items")
    ...
```

Log the key identifiers involved in each request (IDs, counts) at `INFO` level.

---

## 6. Error Responses

Use `HTTPException` for all API errors. Always include a clear `detail` message.

```python
from fastapi import HTTPException

def get_item(item_id: int) -> ItemResponse:
    item = db.find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item
```

For validation errors, let FastAPI's built-in 422 handler work — don't catch `RequestValidationError` unless you need to transform the response shape.

---

## 7. Register All Routers in `main.py`

Every new router must be imported and registered in `app/main.py`. Never leave an unregistered router module.

```python
# app/main.py
from app.routers import health, test, items, users

api.include_router(health.router)
api.include_router(test.router)
api.include_router(items.router)
api.include_router(users.router)
```

---

## 8. CORS in Production

The current `allow_origins='*'` in `main.py` is acceptable for the template but must be replaced in derived services. Read allowed origins from an environment variable:

```python
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

api.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
