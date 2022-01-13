from ctypes import cdll, POINTER, c_uint32, c_void_p
from time import time

class OrderedBacktrackNative:
    def __init__(self):
        self.__native_library = cdll.LoadLibrary("solver")
        
        self.__native_library.solver_ordered_backtrack.argtypes = [c_void_p, POINTER(c_uint32)]

    def solve(self, sudoku, iterate):
        loop = 100

        times = []
        native_data = bytearray(self.__positions_as_bytes(sudoku))

        for _ in range(100):
            copy = bytes(native_data)
            iterations = c_uint32(0)
            before = time()
            self.__native_library.solver_ordered_backtrack(copy, iterations)
            after = time()
            times.append(after - before)


        self.__bytes_to_positions(sudoku, copy)

        print(f"Average time: {sum(times) / loop}")
        

    # typedef struct {
    #     uint8_t value;
    #     uint8_t is_given;
    # } position;

    # #define EMPTY_POSITION UINT8_MAX

    # typedef struct {
    #     position values[9 * 9];
    # } sudoku;

    def __positions_as_bytes(self, sudoku):
        data = bytearray()

        def position_to_byte(x, y):
            value = sudoku[x, y]
            is_given = sudoku.is_given(x, y)

            data.append(value or 255)
            data.append(1 if is_given else 0)

        for y in range(9):
            for x in range(9):
                position_to_byte(x, y)
        
        return bytes(data)

    def __bytes_to_positions(self, sudoku, native_data):
        i = 0

        for y in range(9):
            for x in range(9):
                value = native_data[i]
                is_given = native_data[i + 1]

                i += 2

                if sudoku.is_given(x, y):
                    assert(is_given == 1)
                    assert(sudoku[x, y] == value)
                else:
                    assert(is_given == 0)
                    sudoku[x, y] = value if value != 255 else None
