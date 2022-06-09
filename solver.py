from time import time
import sudoku
from enum import Enum


class SolveStrategy(Enum):
    BACKTRACK = "solveBackTrack"
    BACKTRACK_SORTED = "solveBackTrackSorted"


class Solver:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def crimeDesc(self, x, y, n):
        return list(filter(lambda x: x is not None, map(lambda arr: arr[1] if n in arr[0]() else None, [
            [lambda: self.sudoku.column(x), "Already in column"],
            [lambda: self.sudoku.row(y), "Already in row"],
            [lambda: self.sudoku.containing_grid(x, y), "Already in grid"],
        ])))[0]

    def solve(self, solver):
        iterations = 0
        start = time()
        lastIterTime = time()

        def iterate():
            nonlocal lastIterTime, iterations

            iterations += 1

            # if iterations % 1_000 == 0:
            #     now = time()
            #     elapsed = now - lastIterTime
            #     lastIterTime = now

            #     print(f"{1_000 / elapsed} iterations/sec")

        ret = solver.solve(self.sudoku, iterate)

        # because passing the function to native is impractical,
        # native instead returns iteration count
        if ret is not None:
            iterations = ret

        end = time()
        elapsed = end - start
        print(f"Took {elapsed}s, with {iterations} iterations")

        assert self.sudoku.is_solved()

        return (elapsed, iterations)


hard_puzzle = sudoku.Sudoku.from_text("""
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 8 5
0 0 1 0 2 0 0 0 0
0 0 0 5 0 7 0 0 0
0 0 4 0 0 0 1 0 0
0 9 0 0 0 0 0 0 0
5 0 0 0 0 0 0 7 3
0 0 2 0 1 0 0 0 0
0 0 0 0 4 0 0 0 9
""")

# hard_puzzle = sudoku.example