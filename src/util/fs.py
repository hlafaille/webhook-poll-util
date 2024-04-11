from pathlib import Path


async def path_to_import_notation(path: Path) -> tuple[str, str]:
    """Convert a filesystem path to Python import notation

    Args:
        path (Path): Filesystem path

    Returns:
        str: Python import notation
    """
    prepared: str = path.as_posix().replace("/", ".").removesuffix(".py")
    split: list[str] = prepared.split(".")
    package: str = '.'.join(split[0:len(split) - 1])
    module: str = split[-1]
    return (package, module)
    


async def handler_name_from_path(path: Path) -> str:
    """Get a handlers name from its path

    Args:
        path (Path): _description_

    Returns:
        str: _description_
    """
    return path.name.replace(".py", "")
