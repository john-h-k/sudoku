class Sudoku:
    @staticmethod
    def from_text(text):
        givens = {}

        for y, line in enumerate([line.strip() for line in text.split("\n") if len(line.strip()) > 0]):
            for x, value in enumerate(line.strip().split(" ")):
                if int(value) != 0:
                    givens[x, y] = int(value)

        return Sudoku(givens)

    def to_text(self):
        result = []

        for y in range(9):
            result.append(" ".join([str(self[x, y]) for x in range(9)]))

        return "\n".join(result)

    def __init__(self, givens={}):
        self.__grids = [Sudoku.Grid(self, index % 3, index // 3) for index in range(9)]
        self.__columns = [Sudoku.Column(self, i) for i in range(9)]
        self.__rows = [Sudoku.Row(self, i) for i in range(9)]

        self.__givens = {}

        for k, v in givens.items():
            self[k] = v
            self.__givens[k] = v
        
        assert(self.__givens == givens)

    def is_legal(self, x, y, n):
        return not any((n in self.row(y), n in self.column(x), n in self.containing_grid(x, y)))

    def grid(self, x, y):
        return self.__grids[y * 3 + x]

    def containing_grid(self, x, y):
        return self.grid(x // 3, y // 3)

    def row(self, i):
        return self.__rows[i]

    def column(self, i):
        return self.__columns[i]
        
    def is_solved(self):
        valid = lambda item: all((n + 1 in item for n in range(9))) 

        rows = all((valid(self.row(x)) for x in range(9)))
        columns = all((valid(self.column(x)) for x in range(9)))
        grids = all((valid(self.__grids[x]) for x in range(9)))

        return rows and columns and grids

    def __eq__(self, other):
        for x in range(9):
            for y in range(9):
                if self[x, y] != other[x, y]:
                    return False
        
        return True

    def is_given(self, x, y):
        return (x, y) in self.__givens

    def __grid_index(self, key):
        return (key[0] // 3, key[1] // 3)

    def __piece_index(self, key):
        return (key[0] % 3, key[1] % 3)

    def __getitem__(self, key):
        return self.grid(*self.__grid_index(key))[self.__piece_index(key)]

    def __setitem__(self, key, value):
        self.grid(*self.__grid_index(key))[self.__piece_index(key)] = value

    class __SudokuSet:
        # Row, Column, Grid
        def is_solved(self):
            return all((n in self for n in range(1, 10)))

        def is_legal(self):
            return all((self.__value_list().count(n) <= 1 for n in range(1, 10)))

        def __contains__(self, value):
            return value in self.__value_list()

        def __value_list(self):
            return [self[i] for i in range(9)]

    
    class Column(__SudokuSet):
        def __init__(self, parent, index):
            self.__parent = parent
            self.__index = index

        def __getitem__(self, key):
            return self.__parent[self.__index, key]

        def __setitem__(self, key, value):
            self.__parent[self.__index, key] = value

    class Row(__SudokuSet):
        def __init__(self, parent, index):
            self.__parent = parent
            self.__index = index

        def __getitem__(self, key):
            return self.__parent[key, self.__index]

        def __setitem__(self, key, value):
            self.__parent[key, self.__index] = value

    class Grid(__SudokuSet):
        def __init__(self, parent, x, y):
            self.__values = [None] * 3 * 3
            self.__empty_count = 9
            self.__parent = parent
            self.__x = x
            self.__y = y

        def __getitem__(self, key):
            return self.__values[key[1] * 3 + key[0]]

        def __setitem__(self, key, value):
            x = (self.__x * 3) + key[0]
            y = (self.__y * 3) + key[1]

            if self.__parent.is_given(x, y):
                raise IndexError(f"Position was given!")
            
            self.__values[key[1] * 3 + key[0]] = value

            self.__empty_count += (1 if value is None else -1)

        def __contains__(self, value):
            return value in self.__values

    class __ForwardIndexer:
        def __init__(self, getter):
            self.__getter = getter

        def __getitem__(self, key):
            return self.__getter(key)

    def highlighted(self):
        return self.__str__(True)

    def __str__(self, highlight=False):
        def cell(value, x, y):
            def color(value):
                prefix = '\033[91m'
                postfix = '\033[0m'

                return value if not highlight else prefix + value + postfix

            value = str(value) if self.is_given(x, y) else (color(str(value)) if value is not None else ' ')
            
            grid_x = x % 3 == 0
            grid_y = y % 3 != 0

            result = "-----" if grid_y else '═════'
            result += "\n"
            result += "‖" if grid_x else "|"
            result += f"  {' ' if value is None else value}  "
            result += "\n"

            return result

        result = ""
        for y in range(9):
            line = ""
            for x in range(9):
                line += cell(self[x, y], x, y)

            split = line.split("\n")
            
            result += "\n" + ("".join(split[::2]) + "\n" + "".join(split[1::2]))

        return result

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

correct = Sudoku.from_text("""
6 2 7 3 5 1 9 8 4
8 1 3 4 6 9 2 5 7
5 9 4 2 8 7 6 1 3
1 7 5 9 4 6 8 3 2
3 6 9 1 2 8 7 4 5
2 4 8 5 7 3 1 9 6
7 3 6 8 1 5 4 2 9
9 8 2 7 3 4 5 6 1
4 5 1 6 9 2 3 7 8
""")

print(correct.to_text())