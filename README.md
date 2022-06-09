# Sudoku

An extremely fast backtracking Sudoku solver, implemented in Python & C.
This was primarily for testing the algorithms involved, so the code in `example.py` is a bit janky, as it is
just handling execution + data formatting.

```sh
# Run the entire benchmark suite
make
python example.py all
```

You can also run individual algorithms:

```sh
> python example.py

Usage:
  example.py <algorithm>

  algorithms:
    * backtrack
    * backtrack-ordered
    * native
    * native-ordered
```
