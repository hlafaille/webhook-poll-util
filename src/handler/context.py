from typing import Any


class PollResponseContext:
    """Represents the context of a poll response."""
    is_healthy: bool
    pretty_message: str
    
    def __init__(self, is_healthy: bool, pretty_message: str) -> None:
        self.is_healthy = is_healthy
        self.pretty_message = pretty_message


class JsonWebhookPayloadContext:
    """Represents the request payload of a webhook."""
    payload: dict[Any, Any]
    
    def __init__(self, payload: dict[Any, Any]) -> None:
        self.payload = payload