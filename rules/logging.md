# Logging Rules

Apply these rules anywhere logging is used in the codebase.

---

## 1. Always Use the Shared Logger

Never instantiate a new logger directly. Import the shared `logger` from `app.logger`:

```python
# CORRECT
from app.logger import logger

logger.info("Processing request")

# WRONG — creates an unformatted, unconfigured logger
import logging
log = logging.getLogger(__name__)
log.info("Processing request")

# WRONG — use the logger, not print
print("Processing request")
```

---

## 2. Log Levels

Use the correct level for the situation:

| Level | When to use | Example |
|-------|-------------|---------|
| `logger.debug` | Detailed internal state, not shown in production | `logger.debug(f"Parsed payload: {payload}")` |
| `logger.info` | Normal operational events | `logger.info(f"Request received for item_id={item_id}")` |
| `logger.warning` | Unexpected but recoverable state | `logger.warning(f"Retry {attempt}/3 for service call")` |
| `logger.error` | Failures that need investigation | `logger.error(f"Database unreachable: {exc}")` |

Never use `logger.info` for errors, or `logger.error` for routine events.

---

## 3. What to Log

**Do log:**
- Request identifiers (IDs, resource names) at the start of a request
- Operation outcomes at `INFO` (e.g., "item created", "record found")
- All caught exceptions at `ERROR` with the exception message
- Performance anomalies at `WARNING`

**Never log:**
- Passwords, API keys, tokens, or secrets
- Full request/response bodies containing user PII
- Card numbers, SSNs, or any regulated personal data

```python
# CORRECT
logger.info(f"Creating order for user_id={user_id}, items={len(items)}")

# WRONG — logs PII
logger.info(f"User {user.email} with card {card.number} placed order")
```

---

## 4. Log Message Format

Messages should be human-readable and include the key identifiers for traceability. Use f-strings for clarity.

```python
# CORRECT — includes traceable identifiers
logger.info(f"Health check requested from {request.client.host}")
logger.error(f"Failed to fetch item item_id={item_id}: {exc}")

# WRONG — no context, cannot trace in logs
logger.info("Request received")
logger.error("Failed")
```

---

## 5. Structured Logging in Production

The `StructuredLogger` in `app/logger.py` outputs plain text by default (local dev) and JSON when `PROFILE=pr-disabled`. This is handled automatically — do not conditionally format messages based on `PROFILE` in application code.

The `PROFILE` environment variable controls the output format:

| `PROFILE` value | Log format |
|-----------------|------------|
| `dv` (default) | Plain text with ANSI color support |
| `pr-disabled` | JSON with hostname, level, and timestamp |

---

## 6. Logger Colors (Optional)

The `StructuredLogger.create_logger()` accepts an optional `color` parameter for color-coded output in local development:

```python
from app.logger import StructuredLogger

logger = StructuredLogger.create_logger(name=__name__, color="cyan")
```

Available colors: `grey`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.

This is a local dev convenience feature — color has no effect in JSON production mode.

---

## 7. Log Level Configuration

Set the `LOG_LEVEL` environment variable to control verbosity. The default is `DEBUG`.

```bash
# Production — only INFO and above
LOG_LEVEL=INFO

# Debugging locally
LOG_LEVEL=DEBUG
```

Never hard-code the log level in application code — always read it from the environment.
