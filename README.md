# zit

Nested sandbox box with an inner sandbox computer.

Every number is raw binary bits with bit **1** then bit **0** stuck on the back. That pair is a mark, not the integer ten.

Barrage is the human language. Only `## The actual code` runs.

## Layout

```
sandbox-box/
  README.md
  inner-sandbox/
    encoding.py
    barrage.py
    computer.py
    run.py
    programs/demo.s10
    programs/time-keeper.barrage
```

## Run

```bash
python3 sandbox-box/inner-sandbox/run.py
python3 sandbox-box/inner-sandbox/run.py sandbox-box/inner-sandbox/programs/demo.s10
```

Default program is the Barrage time keeper: five `TICK`s, then `KEEP`.
