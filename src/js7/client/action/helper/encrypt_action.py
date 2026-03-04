import os
import subprocess
from pathlib import Path
from typing import Optional, Union


def encrypt_action(
    java_bin_path: Union[Path, str],
    cert_file_path: Union[Path, str],
    in_string: Optional[str] = None,
    in_file: Optional[Union[Path, str]] = None,
    out_path: Optional[Union[Path, str]] = None,
) -> str:

    BASE_DIR = Path(__file__).resolve().parent
    java_lib_path = (BASE_DIR.parent.parent.parent / "java" / "lib").resolve()

    java_bin_path = Path(java_bin_path)
    cert_file_path = Path(cert_file_path)
    in_file = Path(in_file) if in_file else None
    out_path = Path(out_path) if out_path else None

    # --- Validate ---
    if not java_lib_path.exists():
        raise ValueError(f"Java lib path not found: {java_lib_path}.")

    if not cert_file_path.exists():
        raise ValueError(f"'cert_file_path' does not exist: {cert_file_path}.")

    if not in_string and not in_file:
        raise ValueError("Either 'in_string' or 'in_file' must be provided.")

    if in_string and in_file:
        raise ValueError("Only one of 'in_string' or 'in_file' may be provided.")

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
        "com.sos.commons.encryption.executable.Encrypt",
        f"--cert={cert_file_path}",
    ]

    # --- Input ---
    if in_string:
        cmd.append(f"--in={in_string}")

    if in_file:
        cmd.append(f"--infile={in_file}")

    # --- Output ---
    if out_path:
        if out_path.exists() and out_path.is_dir():
            raise ValueError("'out_path' must be a file path, not a directory.")
        cmd.append(f"--outfile={out_path}")

    # --- Execution ---
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Encrypt failed:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        )

    output = result.stdout.strip().split()[0]

    return "enc:" + output