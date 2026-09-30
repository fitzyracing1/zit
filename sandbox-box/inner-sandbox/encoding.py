"""Inner-sandbox encoding.

A value is a binary number with bit 1 then bit 0 appended.
The pair is a mark, not the integer ten, and not part of the value.
"""

MARK = "10"  # bit 1, then bit 0


def encode(n: int) -> str:
    if not isinstance(n, int) or n < 0:
        raise ValueError("encode only non-negative integers")
    return bin(n)[2:] + MARK


def decode(enc: str) -> int:
    if not isinstance(enc, str) or not enc.endswith(MARK) or len(enc) <= 2:
        raise ValueError(f"missing 1-then-0 mark: {enc!r}")
    raw = enc[:-2]
    if not raw or any(c not in "01" for c in raw):
        raise ValueError(f"not a binary payload: {enc!r}")
    return int(raw, 2)


def is_encoded(enc: str) -> bool:
    try:
        decode(enc)
        return True
    except ValueError:
        return False
