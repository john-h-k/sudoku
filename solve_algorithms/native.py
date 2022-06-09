from ctypes import cdll, POINTER, c_uint32, c_void_p


class Native:
    def __init__(self, ordered):
        self.ordered = ordered
        self.__native_library = cdll.LoadLibrary("solver")

        self.__native_library.solve_backtrack.argtypes = [
            c_void_p,
            POINTER(c_uint32),
            c_uint32
        ]

    def solve(self, sudoku, iterate):
        native_data = bytes(bytearray(self.__positions_as_bytes(sudoku)))

        iterations = c_uint32(0)
        ordered = c_uint32(1 if self.ordered else 0)
        self.__native_library.solve_backtrack(
           native_data,
           iterations,
           ordered
        )

        self.__bytes_to_positions(sudoku, native_data)

        return iterations.value

    # This is the structure we are working withL
    #
    # ```c
    # typedef struct {
    #     uint8_t value;
    #     uint8_t is_given;
    # } position;

    # #define EMPTY_POSITION UINT8_MAX

    # typedef struct {
    #     position values[9 * 9];
    # } sudoku;
    # ```

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
                    assert is_given == 1
                    assert sudoku[x, y] == value
                else:
                    assert is_given == 0
                    sudoku[x, y] = value if value != 255 else None
