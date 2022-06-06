#define PY_SSIZE_T_CLEAN
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

struct timespec start, stop;

double to_seconds(struct timespec time) {
    double seconds = time.tv_sec;
    double nanoseconds = time.tv_nsec;

    return seconds + (nanoseconds / 1e9);
}

double elapsed_seconds() {
    struct timespec result;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &result);

    return to_seconds(result);
}

#define EMPTY_POSITION UINT8_MAX

typedef struct {
    uint8_t x;
    uint8_t y;
    uint8_t count;
} position_info;

typedef struct {
    uint8_t value;
    uint8_t is_given;
} position;

typedef uint16_t legal_values_mask;

typedef struct {
    legal_values_mask columns[9];
    legal_values_mask rows[9];
    legal_values_mask grids[9];
} legal_values_info;

typedef struct {
    position values[9 * 9];
} sudoku;

void initialize_legal_value_info(legal_values_info* legals) {
    memset(legals, 0, sizeof(*legals));
}

void make_illegal(legal_values_info* legals, uint32_t x, uint32_t y, uint8_t value) {
    legal_values_mask value_mask = (1 << value);

    legals->columns[x] |= value_mask;
    legals->rows[y] |= value_mask;
    legals->grids[(y / 3) * 3 + (x / 3)] |= value_mask;
}

void make_legal(legal_values_info* legals, uint32_t x, uint32_t y, uint8_t value) {
    legal_values_mask value_mask = (1 << value);

    legals->columns[x] &= ~value_mask;
    legals->rows[y] &= ~value_mask;
    legals->grids[(y / 3) * 3 + (x / 3)] &= ~value_mask;
}

position* position_at(sudoku* sudoku, uint32_t x, uint32_t y) {
    return &sudoku->values[(y * 9) + x];
}

void set_position(sudoku* sudoku, legal_values_info* legals, uint32_t x, uint32_t y, uint8_t value) {
    position_at(sudoku, x, y)->value = value;

    make_illegal(legals, x, y, value);
}

uint32_t is_empty(sudoku* sudoku, uint32_t x, uint32_t y) {
    return position_at(sudoku, x, y)->value == EMPTY_POSITION;
}

void set_given(sudoku* sudoku, uint32_t x, uint32_t y, uint32_t value) {
    position* pos = position_at(sudoku, x, y);

    pos->value = value;
    pos->is_given = 1;
}

bool is_legal(legal_values_info* legals, uint32_t x, uint32_t y, uint32_t value) {
    legal_values_mask row = legals->rows[y];
    legal_values_mask column = legals->columns[x];
    legal_values_mask grid = legals->grids[(y / 3) * 3 + (x / 3)];

    legal_values_mask mask = (1 << value);
    return (row & mask) == 0 && (column & mask) == 0 && (grid & mask) == 0;
}

typedef enum {
    CONSOLE_FORMAT_HEADER,
    CONSOLE_FORMAT_BLUE,
    CONSOLE_FORMAT_CYAN,
    CONSOLE_FORMAT_GREEN,
    CONSOLE_FORMAT_YELLOW,
    CONSOLE_FORMAT_RED,
    CONSOLE_FORMAT_ENDC,
    CONSOLE_FORMAT_BOLD,
    CONSOLE_FORMAT_UNDERLINE
} console_format;


void start_formatting(console_format format) {
    const char* color_map[] = {
        "\033[95m",
        "\033[94m",
        "\033[96m",
        "\033[92m",
        "\033[93m",
        "\033[91m",
        "\033[1m",
        "\033[4m"
    };
    
    printf("%s", color_map[format]);
}

void end_formatting() {
    printf("\033[0m");
}

void print_sudoku(sudoku* sudoku, console_format* new_value_format) {
    console_format format;
    if (new_value_format == NULL) {
        format = CONSOLE_FORMAT_RED;
    } else {
        format = *new_value_format;
    }

    for (uint32_t y = 0; y < 9; y++) {
        for (uint32_t x = 0; x < 9; x++) {
            position* pos = position_at(sudoku, x, y);

            if (!pos->is_given) {
                start_formatting(format);
            }

            printf("%d", pos->value == EMPTY_POSITION ? 0 : pos->value);
            
            if (!pos->is_given) {
                end_formatting();
            }

            if (x != 8) {
                printf(" ");
            }
        }
        printf("\n");
    }
}

int compare_position_info(const void* l, const void* r) {
    position_info* left = (position_info*)l;
    position_info* right = (position_info*)r;

    if (left->count > right->count) {
        return 1;
    }

    if (left->count < right->count) {
        return -1;
    }

    if (left->y > right->y) {
        return 1;
    }

    if (left->y < right->y) {
        return -1;
    }

    if (left->x > right->x) {
        return 1;
    }

    if (left->x < right->x) {
        return -1;
    }

    return 0;
}

void make_list(sudoku* sudoku, legal_values_info* legals, position_info* list, uint8_t* list_size) {
    uint32_t list_head = 0;

    for (uint32_t y = 0; y < 9; y++) {
        for (uint32_t x = 0; x < 9; x++) {
            uint32_t count = 0;

            if (position_at(sudoku, x, y)->is_given) {
                continue;
            }

            for (uint32_t i = 1; i < 10; i++) {
                if (is_legal(legals, x, y, i)) {
                    count += 1;
                }
            }

            list[list_head].x = x;
            list[list_head].y = y;
            list[list_head].count = count;

            list_head++;
        }
    }

    *list_size = (uint8_t)list_head;
}

void make_optimized_list(sudoku* sudoku, legal_values_info* legals, position_info* list, uint8_t* list_size) {
    make_list(sudoku, legals, list, list_size);    

    qsort(list, *list_size, sizeof(*list), compare_position_info);
}

void solver_ordered_backtrack(sudoku* sudoku, uint32_t* iterations) {
    position_info order_list[9 * 9];
    uint8_t order_list_size = 0;

    legal_values_info legals;
    initialize_legal_value_info(&legals);

    for (uint32_t y = 0; y < 9; y++) {
        for (uint32_t x = 0; x < 9; x++) {
            position* pos = position_at(sudoku, x, y);
            if (pos->is_given) {
                make_illegal(&legals, x, y, pos->value);
            }
        }
    }

    make_optimized_list(sudoku, &legals, order_list, &order_list_size);

    // printf("[");
    // for (size_t i = 0; i < order_list_size; i++) {
    //     printf("(x: %d, y: %d, count: %d), ", order_list[i].x, order_list[i].y, order_list[i].count);
    // }

    // printf("]\n");

    uint32_t current_index = 0;
    uint32_t counter = 0;

    while (true) {
        uint8_t x = order_list[current_index].x;
        uint8_t y = order_list[current_index].y;

        uint8_t guess;
        if (is_empty(sudoku, x, y)) {
            guess = 1;
        } else {
            uint8_t last_guess = position_at(sudoku, x, y)->value;

            assert(!is_legal(&legals, x, y, last_guess));
            make_legal(&legals, x, y, last_guess);

            guess = last_guess + 1;
        }
        
        uint8_t failed = 1;
        
        for (; guess < 10; guess++) {
            position* position = position_at(sudoku, x, y);
            
            if (is_legal(&legals, x, y, guess)) {
                failed = 0;
                position_at(sudoku, x, y)->value = guess;

                break;
            }
        }
        
        if (failed) {
            position_at(sudoku, x, y)->value = EMPTY_POSITION;

            current_index -= 1;
            x = order_list[current_index].x;
            y = order_list[current_index].y;
        } else {
            (*iterations)++;
            current_index += 1;
            make_illegal(&legals, x, y, guess);

            if (current_index < order_list_size) {
                x = order_list[current_index].x;
                y = order_list[current_index].y;
            }
        }
                
        if (current_index == order_list_size) {
            break;
        }
    }

    print_sudoku(sudoku, NULL);
    printf("\n\n\n");
}

int main() {
    sudoku* sudoku = malloc(sizeof(*sudoku));

    for (uint8_t i = 0; i < 81; i++) {
        sudoku->values[i].value = EMPTY_POSITION;
        sudoku->values[i].is_given = 0;
    }

    print_sudoku(sudoku, NULL);

    set_given(sudoku, 1, 0, 2);
    set_given(sudoku, 3, 0, 3);
    set_given(sudoku, 4, 0, 5);
    set_given(sudoku, 7, 0, 8);
    set_given(sudoku, 8, 0, 4);
    set_given(sudoku, 3, 1, 4);
    set_given(sudoku, 4, 1, 6);
    set_given(sudoku, 7, 1, 5);
    set_given(sudoku, 8, 1, 7);
    set_given(sudoku, 3, 2, 2);
    set_given(sudoku, 5, 2, 7);
    set_given(sudoku, 7, 2, 1);
    set_given(sudoku, 2, 3, 5);
    set_given(sudoku, 4, 3, 4);
    set_given(sudoku, 6, 3, 8);
    set_given(sudoku, 8, 3, 2);
    set_given(sudoku, 1, 4, 6);
    set_given(sudoku, 2, 4, 9);
    set_given(sudoku, 4, 4, 2);
    set_given(sudoku, 5, 4, 8);
    set_given(sudoku, 2, 5, 8);
    set_given(sudoku, 6, 5, 1);
    set_given(sudoku, 8, 5, 6);
    set_given(sudoku, 0, 6, 7);
    set_given(sudoku, 1, 6, 3);
    set_given(sudoku, 3, 6, 8);
    set_given(sudoku, 5, 6, 5);
    set_given(sudoku, 6, 6, 4);
    set_given(sudoku, 7, 6, 2);
    set_given(sudoku, 0, 7, 9);
    set_given(sudoku, 3, 7, 7);
    set_given(sudoku, 4, 7, 3);
    set_given(sudoku, 7, 7, 6);
    set_given(sudoku, 8, 7, 1);
    set_given(sudoku, 1, 8, 5);
    set_given(sudoku, 4, 8, 9);
    set_given(sudoku, 5, 8, 2);
    set_given(sudoku, 8, 8, 8);

    printf("\n\n");

    print_sudoku(sudoku, NULL);

    uint32_t iterations = 0;
    solver_ordered_backtrack(sudoku, &iterations);

    print_sudoku(sudoku, NULL);
}

// for y, line in enumerate(text.split("\n")):
//     for x, char in enumerate(line.split(" ")):
//         if char != "0":
//             print(f"set_given(sudoku, {x}, {y}, {char});")

// 0 2 0 3 5 0 0 8 4
// 0 0 0 4 6 0 0 5 7
// 0 0 0 2 0 7 0 1 0
// 0 0 5 0 4 0 8 0 2
// 0 6 9 0 2 8 0 0 0
// 0 0 8 0 0 0 1 0 6
// 7 3 0 8 0 5 4 2 0
// 9 0 0 7 3 0 0 6 1
// 0 5 0 0 9 2 0 0 8