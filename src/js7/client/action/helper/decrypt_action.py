import os
import subprocess
from pathlib import Path
from typing import Optional, Union


def decrypt_action(
    java_bin_path: Union[Path, str],
    key_file_path: Union[Path, str],
    key_password: Optional[str],
    in_string: Optional[str],
    in_file: Optional[Union[Path, str]],
    out_path: Optional[Union[Path, str]],
) -> str:

    BASE_DIR = Path(__file__).resolve().parent
    java_lib_path = (BASE_DIR.parent.parent.parent / "java" / "lib").resolve()

    java_bin_path = Path(java_bin_path)
    key_file_path = Path(key_file_path)
    in_file = Path(in_file) if in_file else None
    out_path = Path(out_path) if out_path else None

    if not java_lib_path.exists():
        raise ValueError(f"Java lib path not found: {java_lib_path}.")

    if not key_file_path.exists():
        raise ValueError(f"'key_file_path' does not exist: {key_file_path}.")

    if not in_string and not in_file:
        raise ValueError("Either 'in_string' or 'in_file' must be provided.")

    if in_file:
        if not in_file.exists():
            raise ValueError(f"'in_file' does not exist: {in_file}.")
        if in_file.is_dir():
            raise ValueError("'in_file' must be a file path, not a directory.")

    sep = ";" if os.name == "nt" else ":"

    classpath = (
        f"{java_lib_path}/patches/*{sep}"
        f"{java_lib_path}/sos/*{sep}"
        f"{java_lib_path}/3rd-party/*{sep}"
        f"{java_lib_path}/stdout"
    )

    cmd = [
        str(java_bin_path),
        "-classpath",
        classpath,
        "com.sos.commons.encryption.executable.Decrypt",
        f"--key={key_file_path}",
    ]

    if key_password:
        cmd.append(f"--key-password={key_password}")

    if in_string:
        # Removes "enc:" if present
        clean_string = in_string.removeprefix("enc:")
        cmd.append(f"--in={clean_string}")

    if in_file:
        cmd.append(f"--infile={in_file}")

    if out_path:
        if out_path.exists() and out_path.is_dir():
            raise ValueError("'out_path' must be a file path, not a directory.")
        cmd.append(f"--outfile={out_path}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Decrypt failed: {e.stderr}")

    return result.stdout.strip()