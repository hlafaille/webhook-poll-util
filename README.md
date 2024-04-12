# Webhook Poll Utility
A simple utility to poll services, determine if they're healthy, and call a webhook.

## Getting Started
Create a `.py` file inside of the `handlers` directory, we'll call it `api_weather_gov.py` for the US Government's Weather API.
In the file, paste this example:
```python
import httpx
from handler.context import PollResponseContext, JsonWebhookPayloadContext

INTERVAL: int = 30000
WEBHOOK_URL: str = "https://my_webhook_url.com/webhook/whatever" # this could be a discord webhook, for example

async def poll() -> PollResponseContext:
    """Poll your service here.

    Returns:
        bool: True if healthy, false if not.
    """
    url: str = "https://api.weather.gov"
    async with httpx.AsyncClient() as c:
        response = await c.get(url)
    return PollResponseContext(
        response.json().get("status") == "OK", "US Government Weather API is healthy."
    )


async def build_webhook_payload_context(
    ctx: PollResponseContext,
) -> JsonWebhookPayloadContext | None:
    """Build the payload for your webhook HTTP request here.

    Args:
        ctx (PollResponseContext): `PollResponseContext` from `poll()`.

    Returns:
        JsonWebhookPayloadContext: A `JsonWebhookPayloadContext`, containing information about your payload.

    Todo:
        Add support for an `XmlWebhookPayloadContext`
    """
    # don't send the webhook if the service is healthy
    if ctx.is_healthy:
        return

    return JsonWebhookPayloadContext({"content": "Service is unhealthy", "username": "api.weather.gov"})

```