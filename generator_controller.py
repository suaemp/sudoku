import random
import puzzle_generator_v3
import numpy as np
from copy import deepcopy
import util

board_to_solve = [[0, 8, 0, 0, 0, 0, 7, 3, 6], [0, 0, 6, 0, 0, 0, 4, 0, 0], [3, 0, 0, 4, 6, 7, 0, 2, 0], [4, 3, 2, 6, 8, 0, 0, 0, 0], [0, 0, 1, 3, 0, 5, 0, 0, 8], [8, 0, 5, 0, 1, 4, 0, 0, 0], [0, 0, 7, 5, 0, 1, 0, 0, 2], [0, 0, 3, 0, 0, 0, 9, 0, 4], [0, 0, 0, 9, 4, 0, 0, 0, 0]]
# board_to_solve = [[6, 7, 0, 5, 0, 0, 0, 0, 0], [0, 0, 8, 6, 3, 0, 9, 0, 0], [3, 0, 0, 0, 1, 0, 6, 4, 8], [0, 0, 0, 0, 0, 0, 0, 0, 4], [0, 8, 4, 3, 0, 0, 0, 0, 0], [9, 0, 0, 0, 4, 7, 3, 6, 5], [0, 0, 5, 9, 0, 0, 0, 7, 3], [8, 1, 7, 0, 0, 3, 5, 2, 0], [0, 0, 3, 0, 7, 0, 0, 0, 6]]
# board_to_solve = [[0, 0, 0, 0, 0, 0, 6, 0, 0], [0, 8, 0, 0, 3, 0, 0, 0, 2], [4, 0, 2, 9, 8, 0, 0, 0, 0], [0, 0, 0, 0, 5, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 4, 7, 0], [0, 0, 0, 6, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 9, 5, 0], [0, 1, 0, 8, 4, 0, 0, 0, 0], [6, 4, 0, 0, 0, 0, 0, 0, 0]]
# board_to_solve = [[6, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 9, 0, 2], [7, 1, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 5, 9, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 4, 0, 6, 0, 0]]
m_tries = 300
amt = 5
diff = 55


def generate_boards(difficulty=45, amount=3, max_tries=60, mode=puzzle_generator_v3.PROGRESSIVE):
    i = 0
    while i < amount:
        puzzle_generator_v3.initialize_board_matrix(max_tries)
        puzzle_generator_v3.initialize_grid_field_indices()
        puzzle_generator_v3.initialize_field_indices()
        puzzle_generator_v3.generate_puzzle(difficulty, mode)
        if puzzle_generator_v3.highest_difficulty == difficulty:
            write_board_and_solution_to_file()
            i += 1
        puzzle_generator_v3.cleanup(max_tries)


def generate_single_puzzle(difficulty, max_tries=60):
    while 1:
        puzzle_generator_v3.initialize_board_matrix(max_tries)
        puzzle_generator_v3.initialize_grid_field_indices()
        puzzle_generator_v3.initialize_field_indices()
        puzzle_generator_v3.generate_puzzle(difficulty)
        if puzzle_generator_v3.highest_difficulty == difficulty:
            value = [puzzle_generator_v3.highest_difficulty, str(puzzle_generator_v3.most_difficult_board),
                     str(puzzle_generator_v3.solved_board)]
            write_board_and_solution_to_file()
            puzzle_generator_v3.cleanup(max_tries)
            return value
        puzzle_generator_v3.cleanup(max_tries)


def write_board_and_solution_to_file():
    with open('gen_boards.txt', 'a') as the_file:
        the_file.write(f"{puzzle_generator_v3.highest_difficulty};"
                       f"{puzzle_generator_v3.most_difficult_board};"
                       f"{puzzle_generator_v3.solved_board}\n")


def solve_board(board):
    puzzle_generator_v3.initialize_board_matrix()
    puzzle_generator_v3.initialize_grid_field_indices()
    puzzle_generator_v3.initialize_field_indices()
    board_ret = puzzle_generator_v3.number_blank_fields(board)
    puzzle_generator_v3.board = deepcopy(board_ret)
    puzzle_generator_v3.solve()
    print(puzzle_generator_v3.solutions)
    print(np.matrix(puzzle_generator_v3.solved_board))
    input("waiting")


def shuffle_board(board, solved_board):
    board = util.get_board_as_array(board)
    solved_board = util.get_board_as_array(solved_board)
    shuffled_board = puzzle_generator_v3.get_shuffled(board, solved_board)

    n = random.choice(range(4))

    for i in range(n):
        board = np.rot90(shuffled_board[0]).tolist()
        solved_board = np.rot90(shuffled_board[1]).tolist()

    return board, solved_board




#solve_board(board_to_solve)
#generate_boards(diff, amt, m_tries, puzzle_generator_v3.PROGRESSIVE)
