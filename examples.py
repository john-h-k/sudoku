from sudoku import Sudoku
from solver import Solver
from solve_algorithms.backtrack import Backtrack
from solve_algorithms.ordered_backtrack import OrderedBacktrack
from solve_algorithms.ordered_backtrack_native import OrderedBacktrackNative
import sys

algorithms = {
    "default": Backtrack(),
    "ordered": OrderedBacktrack(),
    "native": OrderedBacktrackNative()
}

example = Sudoku.from_text("""
0 2 0 3 5 0 0 8 4
0 0 0 4 6 0 0 5 7
0 0 0 2 0 7 0 1 0
0 0 5 0 4 0 8 0 2
0 6 9 0 2 8 0 0 0
0 0 8 0 0 0 1 0 6
7 3 0 8 0 5 4 2 0
9 0 0 7 3 0 0 6 1
0 5 0 0 9 2 0 0 8
""")

erect_puzzle = Sudoku.from_text("""
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

algorithm = algorithms[sys.argv[1] if len(sys.argv) > 1 else "default"]

solver = Solver(erect_puzzle)
solver.solve(algorithm)