import os
from pathlib import Path


def get_handler_paths() -> list[Path]:
    """Get a list of `Path` objects pointing to the handlers. Todo, add directory recursion.

    Returns:
        list[Path]: List of `Path` objects, pointing to the handlers.
    """
    files = os.listdir("handlers")
    paths: list[Path] = []
    for file in files:
        if not file in ["__init__.py", "__pycache__"]:
            paths.append(Path(f"handlers/{file}"))
    return paths