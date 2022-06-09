from sudoku import Sudoku
from solver import Solver
from solve_algorithms.backtrack import Backtrack
from solve_algorithms.ordered_backtrack import OrderedBacktrack
from solve_algorithms.native import Native

from tabulate import tabulate

import sys

algorithms = {
    "backtrack": Backtrack(),
    "backtrack-ordered": OrderedBacktrack(),
    "native": Native(False),
    "native-ordered": Native(True)
}


def normal_puzzle():
    return Sudoku.from_text("""
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


def hard_puzzle():
    return Sudoku.from_text("""
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


def main():
    if len(sys.argv) < 2:
        print("Usage: ")
        print("  example.py <algorithm>")
        print()
        print("  algorithms: ")
        print("    * backtrack ")
        print("    * backtrack-ordered ")
        print("    * native ")
        print("    * native-ordered ")

        return

    algorithm_name = sys.argv[1]

    if algorithm_name != "all":
        run(algorithm_name, algorithms[algorithm_name])
    else:
        results = {}

        for name, algorithm in algorithms.items():
            print(f"{name}")
            results[name] = run(name, algorithm)
            print()
            print()

        print("Done!")
        print()

        (backtrack_normal, backtrack_hard) = results["backtrack"]
        (backtrack_ordered_normal, backtrack_ordered_hard) = results["backtrack-ordered"]
        (native_normal, native_hard) = results["native"]
        (native_ordered_normal, native_ordered_hard) = results["native-ordered"]

        def calc_speed_diff(time1, time2):
            return ((time1 - time2) / time1) * 100

        def calc_iter_diff(iter1, iter2):
            return ((iter1 - iter2) / iter1) * 100

        def print_results(name1, name2, speed_diff, iter_diff=None):
            if iter_diff is not None:
                print(f"{name2} is {speed_diff:.2f}% faster and {iter_diff:.2f}% fewer iterations than {name1}.")
            else:
                print(f"{name2} is {speed_diff:.2f}% faster than {name1}. Iterations are the same.")

        # Backtrack Ordered Normal vs backtrack Normal
        speed_diff = calc_speed_diff(*[x[0] for x in [backtrack_normal, backtrack_ordered_normal]])
        iter_diff = calc_iter_diff(*[x[1] for x in [backtrack_normal, backtrack_ordered_normal]])
        print_results("Backtrack Normal", "Backtrack Ordered Normal", speed_diff, iter_diff)

        # Native Normal vs backtrack Normal
        speed_diff = calc_speed_diff(*[x[0] for x in [backtrack_normal, native_normal]])
        print_results("Cacktrack Normal", "Native Normal", speed_diff)

        # Native Hard vs Backtrack Ordered Hard
        speed_diff = calc_speed_diff(*[x[0] for x in [backtrack_ordered_hard, native_hard]])
        print_results("Backtrack Ordered Hard", "Native Hard", speed_diff)

        # Native Ordered Hard vs Native Hard
        speed_diff = calc_speed_diff(*[x[0] for x in [native_hard, native_ordered_hard]])
        iter_diff = calc_iter_diff(*[x[1] for x in [native_hard, native_ordered_hard]])
        print_results("Native Hard", "Native Ordered Hard", speed_diff, iter_diff)

        # Native Ordered Hard vs Backtrack Ordered Hard
        speed_diff = calc_speed_diff(*[x[0] for x in [backtrack_ordered_hard, native_ordered_hard]])
        print_results("Backtrack Ordered Hard", "Native Ordered Hard", speed_diff)

        print()
        print()

        def create_table_data():
            headers = ["Algorithm", "Normal Speed (s)", "Normal Iterations", "Hard Speed (s)", "Hard Iterations"]
            algorithms = ["Backtrack", "Backtrack Ordered", "Native", "Native Ordered"]
            data = []
    
            all_results = {
                "Backtrack": backtrack_normal + (),
                "Backtrack Ordered": backtrack_ordered_normal + backtrack_ordered_hard,
                "Native": native_normal + native_hard,
                "Native Ordered": native_ordered_normal + native_ordered_hard
            }
    
            for algo in algorithms:
                row = [algo] + list(all_results[algo])
                data.append(row)
    
            return headers, data

        headers, data = create_table_data()
        print(tabulate(data, headers, tablefmt="pretty", numalign="left", stralign="left"))

def run(name, algorithm):
    print("Solving normal puzzle...")
    solver = Solver(normal_puzzle())
    normal_result = solver.solve(algorithm)

    if name == "backtrack":
        print("`backtrack` takes too long on the hard puzzle (> 1 hour), so not trying")
        return (normal_result, None)
    else:
        print("Solving hard puzzle...")
        solver = Solver(hard_puzzle())
        return (normal_result, solver.solve(algorithm))


if __name__ == "__main__":
    main()
