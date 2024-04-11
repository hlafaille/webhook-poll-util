from typing import Any


class PollResponseContext:
    """Represents the context of a poll response."""
    is_healthy: bool
    
    def __init__(self, is_healthy: bool) -> None:
        self.is_healthy = is_healthy


class JsonWebhookPayloadContext:
    """Represents the request payload of a webhook."""
    payload: dict[Any, Any]
    
    def __init__(self, payload: dict[Any, Any]) -> None:
        self.payload = payload