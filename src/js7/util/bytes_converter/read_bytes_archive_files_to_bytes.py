from typing import List, Optional, Tuple
import zipfile
import tarfile
from io import BytesIO

from ..detect_archive_type import detect_archive_type


def read_bytes_archive_files_to_bytes(
    file: bytes,
    filter_suffixes: Optional[List[str]] = None
) -> Optional[List[Tuple[str, bytes]]]:
    """Returns POSIX path and file as bytes or None if not an archive or no files found."""

    if not file:
        return None

    archive_type = detect_archive_type(file)
    if archive_type is None:
        return None

    # Normalize suffix filter
    suffixes = None
    if filter_suffixes:
        suffixes = tuple(s.lower() for s in filter_suffixes)

    result: List[Tuple[str, bytes]] = []

    # ZIP
    if archive_type == "ZIP":
        try:
            with zipfile.ZipFile(BytesIO(file), "r") as zf:
                for info in zf.infolist():
                    if info.is_dir():
                        continue

                    posix_path = info.filename.replace("\\", "/")

                    if suffixes and not posix_path.lower().endswith(suffixes):
                        continue

                    data = zf.read(info)
                    result.append((posix_path, data))
        except (zipfile.BadZipFile, OSError):
            return None

    # TAR.GZ
    elif archive_type == "TAR_GZ":
        try:
            with tarfile.open(fileobj=BytesIO(file), mode="r:gz") as tf:
                for member in tf.getmembers():
                    if not member.isfile():
                        continue

                    posix_path = member.name.replace("\\", "/")

                    if suffixes and not posix_path.lower().endswith(suffixes):
                        continue

                    extracted = tf.extractfile(member)
                    if extracted is None:
                        continue

                    data = extracted.read()
                    result.append((posix_path, data))
        except (tarfile.TarError, OSError):
            return None

    return result or None