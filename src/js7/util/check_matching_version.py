from typing import Tuple


def _version_to_tuple(input: str) -> Tuple[int, int, int]:
    try:
        ep_major, ep_minor, ep_patch = input.split(".")
        return int(ep_major), int(ep_minor), int(ep_patch)
    except Exception as e:
        raise ValueError(f"Invalid version string '{input}'. Error: {e}")
            
def check_matching_version(*, min: str, max: str, check: str) -> bool:
    # Normalize to MAJOR.MINOR.PATCH
    check = check.split("-", 1)[0]
    check = ".".join(check.split(".")[:3])
    
    min_version:   Tuple[int, int, int] = _version_to_tuple(min)
    max_version:   Tuple[int, int, int] = _version_to_tuple(max)
    check_version: Tuple[int, int, int] = _version_to_tuple(check)

    return min_version <= check_version <= max_version