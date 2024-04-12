import logging
import sys

_LOGGERS: dict[str, logging.Logger] = {}

def get_logger(name: str) -> logging.Logger:
    """Get a logger by name

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Logger instance
    """
    # return a preconfigured logger if it exists
    if name in _LOGGERS:
        return _LOGGERS[name]

    # else, create it
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    _LOGGERS[name] = logger
    return logger