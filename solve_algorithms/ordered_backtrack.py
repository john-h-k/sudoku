from functools import total_ordering


class OrderedBacktrack:
    def solve(self, sudoku, iterate):
        list = self.getOptimizedList(sudoku)

        self.orderedBacktrack(list, sudoku, iterate)

    def getBasicList(self, sudoku):
        order_list = []
        for y in range(9):
            for x in range(9):
                if sudoku.is_given(x, y):
                    continue
                order_list.append((x, y))
        return order_list

    def getOptimizedList(self, sudoku):
        @total_ordering
        class PositionInfo:
            def __init__(self, x, y, count):
                self.x = x
                self.y = y
                self.count = count

            def __lt__(self, other):
                return self.__compare_to(other) == -1

            def __gt__(self, other):
                return self.__compare_to(other) == 1

            def __eq__(self, other):
                return self.__compare_to(other) == 0

            def __compare_to(self, other):
                if self.count > other.count:
                    return 1

                if self.count < other.count:
                    return -1

                if self.y > other.y:
                    return 1

                if self.y < other.y:
                    return -1

                if self.x > other.x:
                    return 1

                if self.x < other.x:
                    return -1

                return 0

            def __str__(self):
                return f"(x: {self.x}, y: {self.y}, count: {self.count})"

        optimized_list = []
        for y in range(9):
            for x in range(9):
                count = 0
                if sudoku.is_given(x, y):
                    continue
                for i in range(1, 10):
                    if sudoku.is_legal(x, y, i):
                        count += 1

                optimized_list.append(PositionInfo(x, y, count))

        optimized_list.sort()

        return [(o.x, o.y) for o in optimized_list]

    def orderedBacktrack(self, order_list, sudoku, iterate):
        iterations = 0
        current_index = 0

        while True:
            x, y = order_list[current_index]

            if sudoku.is_given(x, y):
                current_index += 1
                x, y = order_list[current_index]
            else:
                if sudoku[x, y] is None:
                    start_it = 1
                else:
                    start_it = sudoku[x, y] + 1

                failed = True

                for i in range(start_it, 10):
                    if sudoku.is_legal(x, y, i):
                        failed = False
                        sudoku[x, y] = i

                        break

                if failed:
                    sudoku[x, y] = None
                    current_index -= 1
                    x, y = order_list[current_index]
                    while sudoku.is_given(x, y):
                        current_index -= 1
                        x, y = order_list[current_index]
                else:
                    current_index += 1
                    iterate()
                    iterations += 1
                    if current_index < len(order_list):
                        x, y = order_list[current_index]

            if current_index == len(order_list):
                break
