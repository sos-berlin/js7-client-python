from typing import List, Literal, Tuple
from io import BytesIO
import zipfile
import tarfile
import posixpath


def bytes_to_archive_bytes(
    *,
    archive_format: Literal["ZIP", "TAR_GZ"],
    files: List[Tuple[str, bytes]],  # path, content bytes
) -> bytes:

    # Validate: archive_format
    if archive_format not in ("ZIP", "TAR_GZ"):
        raise ValueError("'archive_format' must be 'ZIP' or 'TAR_GZ'.")

    # Validate: files
    if not files:
        raise ValueError("'files' is required.")

    for path, content in files:
        if not path:
            raise ValueError("File path must not be empty.")

        if not content:
            raise ValueError("File content must not be empty.")

    # Normalize paths (no leading slash, POSIX-style)
    normalized_files = [
        (posixpath.normpath(path.lstrip("/")), bytes(content))
        for path, content in files
    ]

    buffer = BytesIO()

    # Build: ZIP 
    if archive_format == "ZIP":
        with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path, content in normalized_files:
                zf.writestr(path, content)

    # Build: TAR.GZ
    elif archive_format == "TAR_GZ":
        with tarfile.open(fileobj=buffer, mode="w:gz") as tf:
            for path, content in normalized_files:
                info = tarfile.TarInfo(name=path)
                info.size = len(content)
                tf.addfile(info, BytesIO(content))

    buffer.seek(0)
    return buffer.read()
