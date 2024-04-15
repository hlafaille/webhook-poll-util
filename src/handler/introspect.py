import os
from pathlib import Path


def get_handler_paths() -> list[Path]:
    """Get a list of `Path` objects pointing to the handlers. Todo, add directory recursion.

    Returns:
        list[Path]: List of `Path` objects, pointing to the handlers.
    """
    if not os.path.exists("handlers"):
        raise RuntimeError("Directory 'handlers' does not exist; Create it and declare a handler there!")
    files = os.listdir("handlers")
    paths: list[Path] = []
    for file in files:
        if not file in ["__init__.py", "__pycache__"]:
            paths.append(Path(f"handlers/{file}"))
    if len(paths) == 0:
        raise RuntimeError("No handlers were declared")
    return paths