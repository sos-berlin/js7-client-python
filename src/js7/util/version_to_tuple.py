from typing import Tuple


def version_to_tuple(input: str) -> Tuple[int, int, int]:
    try:
        check = input.split("-", 1)[0]
        check = ".".join(check.split(".")[:3])
    
        ep_major, ep_minor, ep_patch = input.split(".")
        return int(ep_major), int(ep_minor), int(ep_patch)
    except Exception as e:
        raise ValueError(f"Invalid version string '{input}'. Error: {e}")