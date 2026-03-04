from pathlib import Path
from typing import List, Optional, Tuple


def files_to_bytes(
    *,
    file_path: Path,
    filter_suffixes: Optional[List[str]] = None,
) -> List[Tuple[str, bytes]]:
    """
    Reads a file or directory into memory.

    Input:
        - file: File or directory to read from.
        - filter_suffixes: If set, only files with one of these suffixes (e.g. [".json", ".yaml"]) are included.

    Result:
        - List of (relative_posix_path, file_content_bytes).
    """

    if not file_path.exists():
        raise ValueError(f"File path does not exist: {file_path}")

    # Normalize filter suffixes
    suffixes: Optional[Tuple[str, ...]] = (
        tuple(filter_suffixes) if filter_suffixes else None
    )

    result: List[Tuple[str, bytes]] = []

    def is_allowed(path: Path) -> bool:
        return suffixes is None or path.name.endswith(suffixes)

    if file_path.is_dir():
        for p in file_path.rglob("*"):
            if not p.is_file():
                continue

            if not is_allowed(p):
                continue

            relative_path = p.relative_to(file_path).as_posix()
            result.append((relative_path, p.read_bytes()))

    elif file_path.is_file():
        if is_allowed(file_path):
            result.append((file_path.name, file_path.read_bytes()))

    else:
        raise ValueError(f"Invalid file input: {file_path}")

    return result