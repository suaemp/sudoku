from typing import final
import numpy as np
from copy import deepcopy
import random

# Generator Modes
PROGRESSIVE = "PROGRESSIVE"
RANDOM = "RANDOM"
GAME_BOARD = "GAME BOARD"
SOLVED_GAME_BOARD = "SOLVED GAME BOARD"

found_board = False
board = []
solved_board = []
numbered_board = []
final_board = []
most_difficult_board = None
highest_difficulty = 0
grid = []
grid_field_indices = []
field_indices = []
field_indices_copy = []
loop_field_indices_copy = []
removed_comb = []
invalid_combinations = []
solutions = 0
tries = 0
max_tries = 0


def initialize_board_matrix(max_t=60):
    global board
    global grid
    global numbered_board
    global max_tries

    max_tries = max_t

    for x in range(9):
        row = []
        grid_row = []
        for y in range(9):
            y_divisor = int(y / 3)
            x_divisor = 3 * int((x / 3))
            grid_num = y_divisor + x_divisor
            field_number = x * 9 + y + 10
            row.append(field_number)
            grid_row.append(grid_num)
        empty = []
        grid_field_indices.append(empty)
        board.append(row)
        numbered_board = deepcopy(board)
        grid.append(grid_row)


def initialize_grid_field_indices():
    global grid_field_indices

    for x in range(9):
        for y in range(9):
            grid_field_indices[grid[x][y]].append((x, y))


def initialize_field_indices():
    global field_indices

    for x in range(9):
        for y in range(9):
            field_indices.append((x, y))


def generate_puzzle(difficulty, mode=PROGRESSIVE):
    global board
    global solved_board
    global most_difficult_board

    create_solved_board()
    set_puzzle_difficulty(difficulty, mode)
    if most_difficult_board:
        most_difficult_board = replace_tile_numbers(most_difficult_board, 0)

    print(np.matrix(solved_board))
    print(np.matrix(most_difficult_board))
    print(highest_difficulty)


def set_puzzle_difficulty(difficulty, mode):
    global final_board
    global board
    global field_indices_copy
    global tries
    global removed_comb
    global solutions
    global max_tries

    tries = 0

    while solutions != 1 and tries < max_tries:
        tries += 1
        field_indices_copy = deepcopy(field_indices)
        board = deepcopy(solved_board)
        final_board = deepcopy(solved_board)
        if mode == PROGRESSIVE:
            progressive_remove_fields_from_puzzle(difficulty)
        elif mode == RANDOM:
            random_remove_fields_from_puzzle(difficulty)


def progressive_remove_fields_from_puzzle(difficulty):
    global board
    global found_board
    global removed_comb
    global final_board
    global field_indices_copy
    global loop_field_indices_copy
    global invalid_combinations

    global solutions
    global tries

    tried_elements_in_loop = []

    while len(removed_comb) < difficulty and tries < max_tries:
        found_board = False
        print(tried_elements_in_loop)
        loop_field_indices_copy = deepcopy(field_indices_copy)
        for tried in tried_elements_in_loop:
            loop_field_indices_copy.remove(tried)

        removed_field = loop_field_indices_copy.pop(random.choice(range(len(loop_field_indices_copy))))
        field_indices_copy.remove(removed_field)
        removed_comb.append(removed_field)
        final_board[removed_field[0]][removed_field[1]] = numbered_board[removed_field[0]][removed_field[1]]

        solutions = 0
        board = deepcopy(final_board)
        if set(removed_comb) in invalid_combinations:
            solutions = 2

        if solutions == 0:
            solve(1)
        print(np.matrix(final_board))
        print(len(removed_comb))
        print(solutions)

        if solutions > 1:
            tries += 1
            if set(removed_comb) not in invalid_combinations:
                invalid_combinations.append(set(removed_comb))
            removed_comb.remove(removed_field)
            field_indices_copy.append(removed_field)
            tried_elements_in_loop.append(removed_field)
            final_board[removed_field[0]][removed_field[1]] = solved_board[removed_field[0]][removed_field[1]]

            if len(tried_elements_in_loop) == len(field_indices_copy):
                print("no_more_elements_to_try")
                break

        elif solutions == 1:
            set_most_difficult_board(difficulty)
            progressive_remove_fields_from_puzzle(difficulty)
            if len(removed_comb) == difficulty:
                break
            if set(removed_comb) not in invalid_combinations:
                invalid_combinations.append(set(removed_comb))
            removed_comb.remove(removed_field)
            field_indices_copy.append(removed_field)
            tried_elements_in_loop.append(removed_field)
            final_board[removed_field[0]][removed_field[1]] = solved_board[removed_field[0]][removed_field[1]]

            if len(tried_elements_in_loop) == len(field_indices_copy):
                print("no_more_elements_to_try")
                break


def random_remove_fields_from_puzzle(difficulty):
    global board
    global found_board
    global final_board
    global solutions

    found_board = False
    solutions = 0
    removed_indices = random.sample(field_indices, k=difficulty)
    for index in removed_indices:
        final_board[index[0]][index[1]] = numbered_board[index[0]][index[1]]

    board = deepcopy(final_board)
    solve(1)
    print(np.matrix(final_board))
    print(solutions)

    if solutions == 1:
        set_most_difficult_board(difficulty, mode=RANDOM)


def set_most_difficult_board(diff, mode=PROGRESSIVE):
    global most_difficult_board
    global highest_difficulty

    if highest_difficulty < len(removed_comb) and mode == PROGRESSIVE:
        highest_difficulty = len(removed_comb)
        most_difficult_board = final_board
    elif mode == RANDOM:
        highest_difficulty = diff
        most_difficult_board = final_board


def get_possible_numbers(x, y):
    possible_numbers = []
    cell = board[x][y]
    for number in range(1, 10):
        board[x][y] = number
        row_is_valid = validate_row(x)
        col_is_valid = validate_col(y)
        grid_is_valid = validate_grid(x, y)

        if row_is_valid and col_is_valid and grid_is_valid:
            possible_numbers.append(number)

    board[x][y] = cell

    return possible_numbers


def validate_row(x):
    if len(board[x]) == len(set(board[x])):
        return True
    return False


def validate_col(y):
    column = []
    for row in board:
        column.append(row[y])

    if len(column) != len(set(column)):
        return False
    return True


def validate_grid(x, y):
    grid_index = grid[x][y]
    grid_indices = grid_field_indices[grid_index]
    grid_fields = []
    for index in grid_indices:
        grid_fields.append(board[index[0]][index[1]])

    if len(grid_fields) != len(set(grid_fields)):
        return False
    return True


def create_solved_board():
    global board
    global found_board
    global solved_board

    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] not in range(1, 10):
                field_no = board[x][y]
                possible_numbers = get_possible_numbers(x, y)
                random.shuffle(possible_numbers)
                for number in possible_numbers:
                    board[x][y] = number
                    create_solved_board()
                    if found_board:
                        if not solved_board:
                            solved_board = deepcopy(board)
                        board[x][y] = field_no
                        return
                    board[x][y] = field_no
                return

    found_board = True
    for row in board:
        for i in range(1, 10):
            if i not in row:
                found_board = False


def solve(flag=0):
    global board
    global found_board
    global solutions
    global solved_board

    if found_board or solutions > 1:
        return

    possible_number_field_dict = {}
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] not in range(1, 10):
                possible_numbers = get_possible_numbers(x, y)
                possible_number_field_dict[(x, y)] = possible_numbers

    if len(possible_number_field_dict) == 0:
        found_board = True
        solutions += 1
        if flag == 0:
            print(np.matrix(board))
        found_board = False
        return

    for key in possible_number_field_dict:
        if len(possible_number_field_dict[key]) == 0:
            return

    target_field_index = get_least_possible_combination_field(possible_number_field_dict)
    original_field_value = board[target_field_index[0]][target_field_index[1]]
    for number in possible_number_field_dict[target_field_index]:
        board[target_field_index[0]][target_field_index[1]] = number
        solve(flag)

    board[target_field_index[0]][target_field_index[1]] = original_field_value


def get_least_possible_combination_field(field_dict):
    least_combination_index = None

    for key in field_dict:
        if not least_combination_index:
            least_combination_index = key
        elif len(field_dict[key]) < len(field_dict[least_combination_index]):
            least_combination_index = key

    return least_combination_index


def replace_tile_numbers(rep_board, sign):
    number = []

    for n in range(1, len(rep_board) + 1):
        number.append(n)

    for x in range(len(rep_board)):
        for y in range(len(rep_board[0])):
            if rep_board[x][y] not in number:
                rep_board[x][y] = sign

    return rep_board


def number_blank_fields(rep_board):
    for x in range(len(rep_board)):
        for y in range(len(rep_board[0])):
            if rep_board[x][y] == 0:
                rep_board[x][y] = numbered_board[x][y]

    return rep_board


def get_shuffled(game_board, solved_game_board):
    looped_game_board = game_board
    looped_solved_game_board = solved_game_board

    for i in range(2):
        triple_row_boards = get_quadrants_list(looped_game_board, looped_solved_game_board)
        random.shuffle(triple_row_boards)
        looped_game_board = get_board_from_triple_row_boards(triple_row_boards, GAME_BOARD)
        looped_solved_game_board = get_board_from_triple_row_boards(triple_row_boards, SOLVED_GAME_BOARD)

        if i == 1:
            i += 1

        looped_game_board = np.rot90(looped_game_board, k=1+i).tolist()
        looped_solved_game_board = np.rot90(looped_solved_game_board, k=1+i).tolist()

    return looped_game_board, looped_solved_game_board


def get_board_from_triple_row_boards(triple_row_boards, mode):
    single_board = []
    for element in triple_row_boards:
        if mode == GAME_BOARD:
            for row in element[0]:
                single_board.append(row)
        elif mode == SOLVED_GAME_BOARD:
            for row in element[1]:
                single_board.append(row)

    return single_board


def get_quadrants_list(game_board, solved_game_board):
    quadrants_list = []
    for i in range(3):
        triple_row_tuples = []
        game_board_row_list = []
        solved_game_board_row_list = []

        for j in range(3):
            triple_row_tuples.append((game_board[3*i+j], solved_game_board[3*i+j]))

        random.shuffle(triple_row_tuples)

        for item in triple_row_tuples:
            game_board_row_list.append(item[0])
            solved_game_board_row_list.append(item[1])

        quadrants_list.append((game_board_row_list, solved_game_board_row_list))

    return quadrants_list


def cleanup(m_tries):
    global found_board
    global board
    global solved_board
    global numbered_board
    global final_board
    global most_difficult_board
    global highest_difficulty
    global grid
    global grid_field_indices
    global invalid_combinations
    global field_indices
    global field_indices_copy
    global loop_field_indices_copy
    global removed_comb
    global solutions
    global tries
    global max_tries

    found_board = False
    board = []
    solved_board = []
    numbered_board = []
    final_board = []
    most_difficult_board = None
    highest_difficulty = 0
    grid = []
    grid_field_indices = []
    field_indices = []
    field_indices_copy = []
    loop_field_indices_copy = []
    invalid_combinations = []
    removed_comb = []
    solutions = 0
    tries = 0
    max_tries = m_tries
