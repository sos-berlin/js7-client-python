from pathlib import Path
from typing import Literal, Optional, Union


def _detect_from_bytes(data: bytes) -> Optional[Literal["ZIP", "TAR_GZ"]]:
    if len(data) < 4:
        return None

    # ZIP
    if data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
        return "ZIP"

    # GZIP (tar.gz)
    if data.startswith(b"\x1f\x8b"):
        return "TAR_GZ"

    return None


def detect_archive_type(file: Union[bytes, Path]) -> Optional[Literal["ZIP", "TAR_GZ"]]:
    """Detect archive type from raw bytes or file path using magic bytes."""

    if isinstance(file, bytes):
        return _detect_from_bytes(file)

    if not file.exists() or not file.is_file():
        return None

    try:
        with file.open("rb") as f:
            head = f.read(4)
        return _detect_from_bytes(head)
    except OSError:
        return None