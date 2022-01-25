import database_common
from psycopg2.extras import RealDictCursor, RealDictRow


@database_common.connection_handler
def create_new_user(cursor: RealDictCursor, username: str, h_password: str, email: str, reg_date: str):
    query = """
            INSERT INTO users (username, h_password, email, reg_date)
            VALUES (%(username)s, %(h_password)s, %(email)s, %(reg_date)s)
            """
    cursor.execute(query, {'username': username, 'email': email, 'h_password': h_password, 'reg_date': reg_date})


@database_common.connection_handler
def get_user_details(cursor: RealDictCursor, email: str) -> RealDictRow:
    query = """
            SELECT *
            FROM users
            WHERE email=%(email)s"""
    cursor.execute(query, {'email': email})
    return cursor.fetchone()


@database_common.connection_handler
def get_saved_games(cursor: RealDictCursor, u_id: int) -> list:
    query = """SELECT saved_games.id, user_id, board_seed_id, elapsed_time, timestamp, mistakes, difficulty, hints
                FROM saved_games
                INNER JOIN game_boards
                ON saved_games.board_seed_id = game_boards.id
                WHERE user_id=%(u_id)s
                ORDER BY timestamp DESC"""
    cursor.execute(query, {'u_id': u_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_puzzle_in_game_boards_table(cursor: RealDictCursor, difficulty: int, board: str, solved_board: str):
    query = """
            INSERT INTO game_boards (difficulty, board, solved_board, times_solved)
            VALUES (%(difficulty)s, %(board)s, %(solved_board)s, 0)
            """
    cursor.execute(query, {'difficulty': difficulty, 'board': board,
                           'solved_board': solved_board})


@database_common.connection_handler
def update_times_solved_column(cursor, board_id: int):
    query = """
            UPDATE game_boards
            SET times_solved=times_solved + 1
            WHERE id=%(board_id)s"""
    cursor.execute(query, {'board_id': board_id})


@database_common.connection_handler
def get_selected_difficulty_puzzles(cursor: RealDictCursor, sel_diff_start: int, sel_diff_end: int) -> list:
    query = """
            SELECT id, difficulty, board, solved_board
            FROM game_boards
            WHERE difficulty >= %(sel_diff_start)s AND difficulty <= %(sel_diff_end)s
            """
    cursor.execute(query, {'sel_diff_start': sel_diff_start, 'sel_diff_end': sel_diff_end})
    return cursor.fetchall()


@database_common.connection_handler
def create_game_save(cursor: RealDictCursor, u_id: int, board_seed_id: int, initial_board: str,
                     game_state: str, solved_board: str, timestamp: str, hints: bool, pencil_markups: str) -> int:
    query = """
            INSERT INTO saved_games (user_id, board_seed_id, initial_board, game_state, solved_board, elapsed_time, 
            timestamp, mistakes, hints, pencil_markups, mistake_fields)
            VALUES (%(u_id)s, %(board_seed_id)s, %(initial_board)s, %(game_state)s, %(solved_board)s,
             0, %(timestamp)s, 0, %(hints)s, %(pencil_markups)s, '[]')
            """
    cursor.execute(query, {'u_id': u_id, 'board_seed_id': board_seed_id, 'initial_board': initial_board,
                           'game_state': game_state, 'solved_board': solved_board, 'timestamp': timestamp,
                           'hints': hints, 'pencil_markups': pencil_markups})
    cursor.execute("SELECT lastval()")
    return cursor.fetchone()["lastval"]


@database_common.connection_handler
def get_save_data(cursor: RealDictCursor, u_id: int, save_id: int) -> RealDictRow:
    query = """
            SELECT saved_games.id, user_id, board_seed_id, initial_board, game_state, saved_games.solved_board, 
            elapsed_time, mistakes, difficulty, hints, pencil_markups, mistake_fields
            FROM saved_games
            INNER JOIN game_boards
            ON saved_games.board_seed_id = game_boards.id
            WHERE user_id=%(u_id)s AND saved_games.id=%(save_id)s
            """
    cursor.execute(query, {'u_id': u_id, 'save_id': save_id})
    return cursor.fetchone()


@database_common.connection_handler
def delete_save_game(cursor: RealDictCursor, u_id: int, save_id: int):
    query = """
            DELETE FROM saved_games 
            WHERE user_id=%(u_id)s AND id=%(save_id)s
            """
    cursor.execute(query, {'u_id': u_id, 'save_id': save_id})


@database_common.connection_handler
def add_new_high_score(cursor: RealDictCursor, board_seed_id: int, u_id: int, elapsed_time: int, mistakes: int,
                       difficulty: int):
    query = """
            INSERT INTO scores (board_seed_id, user_id, elapsed_time, mistakes, difficulty)
            VALUES (%(board_seed_id)s, %(u_id)s, %(elapsed_time)s, %(mistakes)s, %(difficulty)s)
            """
    cursor.execute(query, {'board_seed_id': board_seed_id,
                           'u_id': u_id,
                           'elapsed_time': elapsed_time,
                           'mistakes': mistakes,
                           'difficulty': difficulty})


@database_common.connection_handler
def get_all_scores(cursor: RealDictCursor) -> RealDictRow:
    query = """
            SELECT * FROM (
            SELECT board_seed_id, elapsed_time, mistakes, users.username, difficulty
            FROM scores
            INNER JOIN users
            ON scores.user_id=users.id
            ORDER BY elapsed_time ) AS table_sorted_by_elapsed_time
            ORDER BY table_sorted_by_elapsed_time.difficulty DESC, table_sorted_by_elapsed_time.elapsed_time
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_high_score_data_by_username(cursor: RealDictCursor, username: str):
    query = """
            SELECT * FROM (
            SELECT board_seed_id, elapsed_time, mistakes, users.username, difficulty
            FROM scores
            INNER JOIN users
            ON scores.user_id=users.id
            WHERE users.username=%(username)s
            ORDER BY elapsed_time ASC ) AS table_sorted_by_elapsed_time
            ORDER BY table_sorted_by_elapsed_time.difficulty DESC
            """
    cursor.execute(query, {'username': username})
    return cursor.fetchall()


@database_common.connection_handler
def search_high_score_data_by_board_seed(cursor: RealDictCursor, board_seed_id: int):
    query = """
            SELECT board_seed_id, elapsed_time, mistakes, users.username, difficulty
            FROM scores
            INNER JOIN users
            ON scores.user_id=users.id
            WHERE board_seed_id=%(board_seed_id)s
            ORDER BY elapsed_time 
            """
    cursor.execute(query, {'board_seed_id': board_seed_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_high_score_data_by_difficulty(cursor: RealDictCursor, sel_diff_start: int, sel_diff_end: int) -> list:
    query = """
            SELECT * FROM (
            SELECT board_seed_id, elapsed_time, mistakes, users.username, difficulty
            FROM scores
            INNER JOIN users
            ON scores.user_id=users.id
            WHERE difficulty >= %(sel_diff_start)s AND difficulty <= %(sel_diff_end)s
            ORDER BY elapsed_time ) AS table_sorted_by_elapsed_time
            ORDER BY table_sorted_by_elapsed_time.difficulty DESC
            """
    cursor.execute(query, {'sel_diff_start': sel_diff_start, 'sel_diff_end': sel_diff_end})
    return cursor.fetchall()


@database_common.connection_handler
def save_game_to_database(cursor: RealDictCursor, save_id: int, u_id: int, board_seed_id: int, initial_board: str,
                          game_state: str, solved_board: str, pencil_markups: str, mistake_fields: str,
                          elapsed_time: int, mistakes: int, hints: bool):
    query = """
            UPDATE saved_games 
            SET user_id = %(u_id)s, 
                board_seed_id = %(board_seed_id)s,
                initial_board = %(initial_board)s,
                game_state = %(game_state)s, 
                solved_board = %(solved_board)s, 
                pencil_markups = %(pencil_markups)s, 
                mistake_fields = %(mistake_fields)s,
                elapsed_time = %(elapsed_time)s,
                mistakes = %(mistakes)s,
                hints = %(hints)s
            WHERE id=%(save_id)s
            """
    cursor.execute(query, {'save_id': save_id, 'u_id': u_id, 'board_seed_id': board_seed_id,
                           'initial_board': initial_board, 'game_state': game_state, 'solved_board': solved_board,
                           'hints': hints, 'pencil_markups': pencil_markups, 'mistake_fields': mistake_fields,
                           'mistakes': mistakes, 'elapsed_time': elapsed_time})
