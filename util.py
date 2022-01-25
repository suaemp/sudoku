from datetime import datetime
import numpy as np
from data_manager import *


def date_to_int(date):
    converted_date = ""
    for index, i in enumerate(date):
        if index < 19:
            converted_date += i

    return converted_date


def get_actual_date():
    actual_time = datetime.now()
    submission_time = date_to_int(str(actual_time))
    return submission_time


def read_board():
    with open('gen_boards.txt') as text_file:
        data = []
        for line in text_file:
            line = line.replace("\n", "")
            arg_list = line.split(';')
            difficulty = int(arg_list[0])
            data_row = [difficulty, arg_list[1], arg_list[2]]
            data.append(data_row)

    return data


def add_board_data_into_database():
    data = read_board()
    for row in data:
        save_puzzle_in_game_boards_table(row[0], row[1], row[2])


def get_difficulty(removed_tiles, difficulty_dict):
    for key in difficulty_dict:
        if removed_tiles in range(difficulty_dict[key][0], difficulty_dict[key][1] + 1):
            return int(key)


def get_board_as_array(board):
    return eval(board)


def init_markup_matrix():
    matrix = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append([])
        matrix.append(row)

    return matrix


def format_time(elapsed_time):
    time_text = ""
    elapsed_time = elapsed_time // 10
    hours = elapsed_time // 360000
    minutes = (elapsed_time - (hours * 360000)) // 6000
    seconds = (elapsed_time - (hours * 360000) - (minutes * 6000)) // 100
    milliseconds = elapsed_time - (hours * 360000) - (minutes * 6000) - (seconds * 100)

    if hours > 0:
        time_text = str(hours) + "h "

    if minutes == 0:
        time_text += "00:"
    elif minutes < 10:
        time_text += "0" + str(minutes) + ":"
    else:
        time_text += str(minutes) + ":"

    if seconds == 0:
        time_text += "00"
    elif seconds < 10:
        time_text += "0" + str(seconds)
    else:
        time_text += str(seconds)

    if milliseconds == 0:
        time_text += ",00"
    elif milliseconds < 10:
        time_text += ",0" + str(milliseconds)
    else:
        time_text += "," + str(milliseconds)

    return time_text


# add_board_data_into_database()
