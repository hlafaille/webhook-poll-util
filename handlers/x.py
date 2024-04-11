from handler.context import PollResponseContext, JsonWebhookPayloadContext


INTERVAL: int = 1000

async def poll() -> PollResponseContext:
    """Poll your service here.

    Returns:
        bool: True if healthy, false if not.
    """
    return PollResponseContext(True)


async def build_webhook_context(ctx: PollResponseContext) -> JsonWebhookPayloadContext | None:
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