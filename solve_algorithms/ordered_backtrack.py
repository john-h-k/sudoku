class OrderedBacktrack:
    def solve(self, sudoku, iterate):
        list = self.getOptimizedList(sudoku)

        self.orderedBacktrack(list, sudoku)

    def getBasicList(self, sudoku):
        order_list = []
        for y in range(9):
            for x in range(9):
                if sudoku.is_given(x, y):
                    continue
                order_list.append((x, y))
        return order_list
    
    def getOptimizedList(self, sudoku):
        optimized_list = []
        for y in range(9):
            for x in range(9):
                count = 0
                if sudoku.is_given(x, y):
                    continue
                for i in range(1, 10):
                    if sudoku.is_legal(x, y, i):
                        if x == 2 and y == 0:
                            print(i)
                        count += 1
                optimized_list.append([count, (x, y)])
        print(optimized_list)
        optimized_list.sort(key=lambda x: x[0])
        output_list = []
        for i in optimized_list:
            output_list.append(i[1])
        return output_list

    def orderedBacktrack(self, order_list, sudoku):
        current_index = 0
        counter = 0


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
                    counter += 1
                    current_index += 1
                    if current_index < len(order_list):
                        x, y = order_list[current_index]
                    
            if current_index == len(order_list):
                print(counter)
                break
