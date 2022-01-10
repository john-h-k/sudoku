from collections import defaultdict
import sudoku

v = sudoku.example

class Solver:
    def __init__(self, Sudoku):
        self.Sudoku = Sudoku

    def isLegal(self, x, y, n):
        return not any([n in self.Sudoku.column[x], n in self.Sudoku.row[y], n in self.Sudoku.containing_grid[x, y]])
            
    def crimeDesc(self, x, y, n):
        return list(filter(lambda x: x != None, map(lambda arr: arr[1] if n in arr[0]() else None, [
            [lambda: self.Sudoku.column[x], "Already in column"],
            [lambda: self.Sudoku.row[y], "Already in row"],
            [lambda: self.Sudoku.containing_grid[x, y], "Already in grid"],
        ])))[0]

    def SolveBackTrack(self):
        def stepBack(x, y):
            if not self.Sudoku.is_given(x, y):
                visited[x, y] = set()
                self.Sudoku[x, y] = None

            if x > 0:
                return (x - 1, y)
            else:
                assert(y > 0)
                return (8, y - 1)

        def stepForward(x, y, value):
            if value is not None:
                visited[x, y].add(value)

            if x < 8:
                return (x + 1, y)
            else:
                assert(y < 8)
                return (0, y + 1)

        x = 0
        y = 0

        visited = defaultdict(set)

        while True:
            x = 0
            while True:
                if self.Sudoku.is_solved():
                    print(self.Sudoku == sudoku.correct)
                    print("SOLVED!!!")
                    exit(0)

                if self.Sudoku.is_given(x, y):
                    x, y = stepForward(x, y, None)
                else:
                    # get current digit if exists
                    current = self.Sudoku[x, y] or 0

                    for i in range(current, current + 9):
                        value = i % 9 + 1
                        if self.isLegal(x, y, value):
                            self.Sudoku[x, y] = value

                            x, y = stepForward(x, y, value)
                            break
                        else:
                            visited[x, y].add(value)
                            print(self.crimeDesc(x, y, value))
                    else: # no legal moves
                        self.Sudoku[x, y] = None
                        
                        x, y = stepBack(x, y)
                        while self.Sudoku.is_given(x, y) or len(visited[x, y]) == 9:
                            x, y = stepBack(x, y)
                            
     

print(sudoku.example.highlighted())
Solver(sudoku.example).SolveBackTrack()
print(sudoku.example.highlighted())

