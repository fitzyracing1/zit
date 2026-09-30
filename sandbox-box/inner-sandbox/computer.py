"""A small computer that lives in the inner sandbox.

Native word format: encoding.encode(n)  — raw bits + bit 1 + bit 0.

Instruction set (one instruction per line):

  LOAD  rN  <encoded-or-decimal>
  ADD   rD  rA  rB
  SUB   rD  rA  rB
  MUL   rD  rA  rB
  MOV   rD  rS
  TICK  rN          # clock += 1, store encoded tick in rN
  KEEP  rN          # snapshot current clock into rN (no increment)
  PRINT rN
  HALT

Barrage source is accepted. Only ## The actual code is executed.

Registers r0..r7 hold encoded words. Arithmetic strips the mark,
computes, then puts bit 1 then bit 0 back on the result.
"""

from __future__ import annotations

from barrage import extract_actual_code, is_barrage
from encoding import decode, encode, is_encoded


class SandboxComputer:
    def __init__(self) -> None:
        self.regs = {f"r{i}": encode(0) for i in range(8)}
        self.clock = 0
        self.trace: list[str] = []
        self.halted = False

    def _parse_word(self, token: str) -> str:
        if is_encoded(token):
            return token
        if token.isdigit():
            return encode(int(token))
        raise ValueError(f"not a word: {token!r}")

    def _reg(self, name: str) -> str:
        if name not in self.regs:
            raise ValueError(f"no such register: {name}")
        return name

    def step(self, line: str) -> None:
        if self.halted:
            return
        line = line.strip()
        if not line or line.startswith("#"):
            return
        parts = line.replace(",", " ").split()
        op = parts[0].upper()

        if op == "LOAD":
            r = self._reg(parts[1])
            self.regs[r] = self._parse_word(parts[2])
            self.trace.append(f"LOAD {r} = {self.regs[r]} ({decode(self.regs[r])})")
        elif op == "MOV":
            d, s = self._reg(parts[1]), self._reg(parts[2])
            self.regs[d] = self.regs[s]
            self.trace.append(f"MOV {d} <- {s} {self.regs[d]}")
        elif op in {"ADD", "SUB", "MUL"}:
            d, a, b = self._reg(parts[1]), self._reg(parts[2]), self._reg(parts[3])
            va, vb = decode(self.regs[a]), decode(self.regs[b])
            if op == "ADD":
                vr = va + vb
            elif op == "SUB":
                vr = va - vb
            else:
                vr = va * vb
            if vr < 0:
                raise ValueError("negative result")
            self.regs[d] = encode(vr)
            self.trace.append(
                f"{op} {d} = {self.regs[a]} {op} {self.regs[b]} -> {self.regs[d]} ({vr})"
            )
        elif op == "TICK":
            r = self._reg(parts[1])
            self.clock += 1
            self.regs[r] = encode(self.clock)
            self.trace.append(
                f"TICK {r} clock={self.clock} word={self.regs[r]}"
            )
        elif op == "KEEP":
            r = self._reg(parts[1])
            self.regs[r] = encode(self.clock)
            self.trace.append(
                f"KEEP {r} snapshot clock={self.clock} word={self.regs[r]}"
            )
        elif op == "PRINT":
            r = self._reg(parts[1])
            self.trace.append(f"PRINT {r} {self.regs[r]} = {decode(self.regs[r])}")
        elif op == "HALT":
            self.halted = True
            self.trace.append("HALT")
        else:
            raise ValueError(f"unknown op: {op}")

    def run(self, source: str) -> list[str]:
        if is_barrage(source):
            source = extract_actual_code(source)
            self.trace.append("BARRAGE: took ## The actual code only")
        for line in source.splitlines():
            self.step(line)
            if self.halted:
                break
        return self.trace

    def dump(self) -> dict[str, str]:
        return dict(self.regs)
