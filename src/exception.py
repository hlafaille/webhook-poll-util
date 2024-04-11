class HandlerMissingAttributeException(Exception):
    """Represents the scenario in which a handler is missing a required attribute"""
    def __init__(self, handler_name: str, attribute_name: str) -> None:
        super().__init__(f"Handler '{handler_name}' is missing an attribute with name '{attribute_name}'")