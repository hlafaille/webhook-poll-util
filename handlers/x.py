from handler.context import PollResponseContext, JsonWebhookPayloadContext


INTERVAL: int = 1000

async def poll() -> PollResponseContext:
    """Poll your service here.

    Returns:
        bool: True if healthy, false if not.
    """
    return PollResponseContext(True)


async def build_webhook_context(ctx: PollResponseContext) -> JsonWebhookPayloadContext:
    """Build the payload for your webhook HTTP request here.

    Args:
        ctx (PollResponseContext): `PollResponseContext` from `poll()`.

    Returns:
        JsonWebhookPayloadContext: A `JsonWebhookPayloadContext`, containing information about your payload.
        
    Todo:
        Add support for an `XmlWebhookPayloadContext`
    """
    return JsonWebhookPayloadContext({"": ""})