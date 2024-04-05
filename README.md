# Webhook Poll Util

An asynchronous polling utility that calls webhooks when events occur.

## Quick Start

Handlers are responsible for processing the responses from your services. Handlers are written in Python. Utilizing `pyo3`, we can integrate deeply with
the Python interpreter. A handler declaration should look like this.

```python
import json

SERVICE_URL: str = "https://jellyfin.hlafaille.xyz/healthcheck"
WEBHOOK_URL: str = "https://discordapp.com/webhook"
INTERVAL: int = 1000

def handle_response(response: str) -> bool:
    """
    Handle the response from the specified service. You can handle JSON, XML, TOML, etc.
    This function must return a bool, indicating if this service is alive or not.
    """
    parsed = json.loads(response)
    return parsed["message"] == "api is here"


def build_webhook_payload(is_alive: bool) -> dict:
    """
    Create a JSON webhook payload. This function is optional, and will use the Discord payload schema if not defined.
    """
    return {
        "message": "healthy"
    }
```
