from collections import defaultdict


class Backtrack:
    def solve(self, sudoku, iterate):
        def stepBack(x, y):
            if not sudoku.is_given(x, y):
                visited[x, y] = set()
                sudoku[x, y] = None

            if x > 0:
                return (x - 1, y)
            else:
                assert y > 0
                return (8, y - 1)

        def stepForward(x, y, value):
            if value is not None:
                visited[x, y].add(value)

            if x < 8:
                return (x + 1, y)
            else:
                assert y < 8
                return (0, y + 1)

        x = 0
        y = 0

        visited = defaultdict(set)

        sudoku = sudoku

        while True:
            x = 0
            while True:
                if x == 8 and y == 8 and sudoku.is_solved():
                    return

                if sudoku.is_given(x, y):
                    x, y = stepForward(x, y, None)
                else:
                    # get current digit if exists
                    current = sudoku[x, y] or 0

                    for i in range(current, current + 9):
                        value = i % 9 + 1
                        if sudoku.is_legal(x, y, value):
                            sudoku[x, y] = value

                            x, y = stepForward(x, y, value)
                            iterate()

                            break
                        else:
                            visited[x, y].add(value)

                    else:  # no legal moves
                        sudoku[x, y] = None

                        x, y = stepBack(x, y)
                        while sudoku.is_given(x, y) or len(visited[x, y]) == 9:
                            x, y = stepBack(x, y)
