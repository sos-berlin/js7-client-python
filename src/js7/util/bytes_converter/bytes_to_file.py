from pathlib import Path


def bytes_to_file(*, data: bytes, out_path: Path) -> bool:
    """out_path: /my-file.zip"""
    
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)
        return True
    except OSError:
        return False