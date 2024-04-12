import httpx
from handler.context import PollResponseContext, JsonWebhookPayloadContext

INTERVAL: int = 5000


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

    return JsonWebhookPayloadContext({"message": "not healthy"})
