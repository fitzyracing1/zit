# Sandbox Box

Outer sandbox. Everything that runs here stays inside this tree.

```
sandbox-box/
  inner-sandbox/     <- nested sandbox
    encoding.py      <- 1 then 0 mark on every binary number
    barrage.py       <- reads Barrage; runs only ## The actual code
    computer.py      <- LOAD ADD SUB MUL TICK KEEP PRINT HALT
    programs/demo.s10
    programs/time-keeper.barrage
    run.py
```

Rule of the inner machine: a value is raw binary bits with bit 1 then bit 0 stuck on the back. The mark is not part of the number.

Barrage is the human language of the machine. Headings that start with ## are not executed. Only the section called ## The actual code runs.

Time keeper: five TICK steps, then KEEP a snapshot. The count is stored encoded.
