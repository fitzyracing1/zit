#!/usr/bin/env python3
"""Boot the inner-sandbox computer.

Default program is the Barrage time keeper.
Pass another file path to run that instead.
"""

import sys
from pathlib import Path

from computer import SandboxComputer
from encoding import decode


def main() -> None:
    here = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = here / "programs" / "time-keeper.barrage"
    src = path.read_text()
    cpu = SandboxComputer()
    print("=== inner sandbox computer ===")
    print("native word = raw bits + bit 1 + bit 0")
    print("source language = Barrage if the file says so")
    print(f"program = {path.name}")
    print()
    print("--- source ---")
    print(src)
    print("--- trace ---")
    for line in cpu.run(src):
        print(line)
    print()
    print(f"--- clock = {cpu.clock} ---")
    print("--- registers (encoded = value) ---")
    for name, word in cpu.dump().items():
        print(f"  {name}: {word} = {decode(word)}")


if __name__ == "__main__":
    main()
