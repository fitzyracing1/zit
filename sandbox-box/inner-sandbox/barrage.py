"""Barrage reader for the inner-sandbox computer.

Barrage is the plain-language wrap. The machine only executes lines
from the section titled exactly:

    ## The actual code

Everything else is human reading. ## headings are not executed.
Numbered translation lines are not executed.
"""

from __future__ import annotations


CODE_HEAD = "## The actual code"


def extract_actual_code(source: str) -> str:
    lines = source.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == CODE_HEAD.lower():
            start = i + 1
            break
    if start is None:
        raise ValueError("Barrage file has no ## The actual code section")

    body: list[str] = []
    in_fence = False
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("## ") and not in_fence:
            break
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        body.append(line)
    return "\n".join(body)


def is_barrage(source: str) -> bool:
    low = source.lower()
    return CODE_HEAD.lower() in low and source.lstrip().startswith("#")
