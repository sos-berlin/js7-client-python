from typing import Optional


def order_id_to_order_name(s: Optional[str]) -> Optional[str]:
    return s.rsplit("#", 1)[-1].split("-", 1)[1] if s and "-" in s else None
