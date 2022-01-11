from collections import defaultdict
from time import time
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
        iterations = 0
        lastIterTime = time()

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

        sudoku = self.Sudoku

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
                        if self.isLegal(x, y, value):
                            sudoku[x, y] = value

                            x, y = stepForward(x, y, value)
                            iterations += 1

                            if iterations % 1_000 == 0:
                                now = time()
                                elapsed = now - lastIterTime
                                lastIterTime = now

                                print(f"{1_000 / elapsed} iterations/sec")

                            break
                        else:
                            visited[x, y].add(value)

                    else: # no legal moves
                        sudoku[x, y] = None
                        
                        x, y = stepBack(x, y)
                        while sudoku.is_given(x, y) or len(visited[x, y]) == 9:
                            x, y = stepBack(x, y)
    
    def TomBackTrack(self):
    
        def stepBack(x, y):

            if x > 0:
                return (x - 1, y)
            else:
                if y == 0:
                    return (x, y)
                return (8, y - 1)

        def stepForward(x, y):

            if x < 8:
                return (x + 1, y)
            else:
                if y >= 8:
                    return (x, y)
                return (0, y + 1)

        x = 0
        y = 0
        counter = 0

        while True:
            
            #print(self.Sudoku.highlighted())
            if self.Sudoku.is_given(x, y):
                x, y = stepForward(x, y)
            else:
                if self.Sudoku[x, y] is None:
                    start_it = 1
                else:
                    start_it = self.Sudoku[x, y] + 1
                
                failed = True
                
                for i in range(start_it, 10):
                    if self.isLegal(x, y, i):
                        failed = False
                        self.Sudoku[x, y] = i
                        break
                
                if failed:
                    self.Sudoku[x, y] = None
                    x, y = stepBack(x, y)
                    while self.Sudoku.is_given(x, y):
                        x, y = stepBack(x, y)
                else:
                    x, y = stepForward(x, y)
                    counter += 1
                    

            if (x >= 8 and y >= 8):
                print(counter)
                break

    def getBasicList(self):
        order_list = []
        for y in range(9):
            for x in range(9):
                order_list.append((x, y))
        return order_list

    def orderedBacktrack(self, order_list):
        current_index = 0

        while True:
            x, y = order_list[current_index]
            if self.Sudoku.is_given(x, y):
                current_index += 1
                x, y = order_list[current_index]
            else:
                if self.Sudoku[x, y] is None:
                    start_it = 1
                else:
                    start_it = self.Sudoku[x, y] + 1
                
                failed = True
                
                for i in range(start_it, 10):
                    if self.isLegal(x, y, i):
                        failed = False
                        self.Sudoku[x, y] = i
                        break
                
                if failed:
                    self.Sudoku[x, y] = None
                    current_index -= 1
                    x, y = order_list[current_index]
                    while self.Sudoku.is_given(x, y):
                        current_index -= 1
                        x, y = order_list[current_index]
                else:
                    current_index += 1
                    x, y = order_list[current_index]
                    
            if (x >= 8 and y >= 8):
                break

erect_puzzle = sudoku.Sudoku.from_text("""
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

erect_puzzle = sudoku.example

print(erect_puzzle.highlighted())
print(Solver(erect_puzzle).getBasicList())
Solver(erect_puzzle).orderedBacktrack(Solver(erect_puzzle).getBasicList())
print(erect_puzzle.highlighted())
