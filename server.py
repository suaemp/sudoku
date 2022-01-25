import time
from flask import Flask, render_template, request, redirect, session
import data_manager
import util
import bcrypt
from datetime import timedelta, datetime
import random
import generator_controller as gen_ctrl

app = Flask(__name__)
app.secret_key = "super secret key"
app.permanent_session_lifetime = timedelta(days=5)

DIFFICULTY_DICT = {'1': (30, 35), '2': (36, 45), '3': (46, 49), '4': (50, 53), '5': (54, 60)}
DIFFICULTY_NAME_DICT = {'1': 'EASY', '2': 'MEDIUM', '3': 'HARD', '4': 'EXPERT', '5': 'EVIL'}
DIFFICULTY_NAME_SCORES_DICT = {'1': 'select difficulty', '2': 'EASY', '3': 'MEDIUM', '4': 'HARD', '5': 'EXPERT', '6': 'EVIL'}


@app.route("/")
def main_menu():
    logged_in = False
    if 'logged-user' in session:
        logged_in = True

    return render_template('index.html', logged_in=logged_in)


@app.route("/login", methods=["GET"])
def login():
    if 'logged-user' in session:
        return redirect('/')
    return render_template('login.html', invalid='False')


@app.route("/login", methods=["POST"])
def login_post():
    if request.form.get('perm_session') == 'on':
        session.permanent = True

    email = request.form.get('email')
    password = request.form.get('password')
    user_details = data_manager.get_user_details(email)

    if user_details:
        hashed_pass = user_details['h_password']
        hashed_pass = bytes.fromhex(hashed_pass)

        if bcrypt.checkpw(password.encode('utf-8'), hashed_pass):
            session['logged-user'] = user_details  # need to validate for repeating username
            return redirect('/')
        else:
            return render_template('login.html', invalid=True)
    else:
        return render_template('login.html', invalid=True)


@app.route("/register", methods=["GET"])
def register():
    return render_template('register.html', missmatch='False')


@app.route("/register", methods=["POST"])
def register_post():
    password = request.form.get('password')
    c_password = request.form.get('c_password')
    if password == c_password:
        username = request.form.get('username')
        h_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        h_password = h_password.hex()
        email = request.form.get('email')
        reg_date = util.get_actual_date()
        data_manager.create_new_user(username, h_password, email, reg_date)
        return redirect('/login')
    else:
        return render_template('register.html', missmatch=True)


@app.route("/game", methods=["GET"])
def play():
    if 'logged-user' in session:
        new_game = None
        return render_template('game.html', load_menu=False, game=new_game)
    return redirect('/')


@app.route("/game/load", methods=["GET"])
def load():
    if 'logged-user' in session:
        u_id = session['logged-user']['id']
        saved_games = data_manager.get_saved_games(u_id)
        for saved_game in saved_games:
            for key in DIFFICULTY_DICT:
                if saved_game['difficulty'] in range(DIFFICULTY_DICT[key][0], DIFFICULTY_DICT[key][1] + 1):
                    saved_game['difficulty'] = DIFFICULTY_NAME_DICT[key]
            saved_game['elapsed_time'] = util.format_time(saved_game['elapsed_time'])

        return render_template('game.html', load_menu=True, saved_games=saved_games)
    return redirect('/')


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect('/')


@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')


@app.route("/new_game", methods=["POST"])
def start_new_game():
    if 'logged-user' in session:
        difficulty = request.form.get('difficulty')
        if request.form.get('hints') == 'on' and not request.form.get('ranked'):
            hints = True
        else:
            hints = False

        diff_range = DIFFICULTY_DICT[difficulty]
        if difficulty in ['1', '2']:
            diff = random.choice(range(diff_range[0], diff_range[1] + 1))
            board_seed = gen_ctrl.generate_single_puzzle(diff)
            data_manager.save_puzzle_in_game_boards_table(int(board_seed[0]), board_seed[1], board_seed[2])

        boards_list = data_manager.get_selected_difficulty_puzzles(diff_range[0], diff_range[1])
        board_seed = random.choice(boards_list)
        boards = gen_ctrl.shuffle_board(board_seed['board'], board_seed['solved_board'])

        game_data = {'difficulty': int(difficulty) - 1,
                     'game_state': boards[0],
                     'initial_board': boards[0],
                     'elapsed_time': 0,
                     'mistakes': 0,
                     'mistake_fields': [],
                     'pencil_markups': util.init_markup_matrix(),
                     'hints': hints,
                     'ranked': request.form.get('ranked')}

        if not request.form.get('ranked'):
            save_id = data_manager.create_game_save(session['logged-user']['id'],
                                                    board_seed['id'],
                                                    str(boards[0]),
                                                    str(boards[0]),
                                                    str(boards[1]),
                                                    util.get_actual_date(),
                                                    hints,
                                                    str(util.init_markup_matrix()))

            saved_games = data_manager.get_saved_games(session['logged-user']['id'])
            if len(saved_games) > 5:
                data_manager.delete_save_game(session['logged-user']['id'],
                                              saved_games[len(saved_games)-1]['id'])
        else:
            save_id = None

        session['game_data'] = {'save_id': save_id,
                                'seed': board_seed['id'],
                                'game_state': str(boards[0]),
                                'initial_board': str(boards[0]),
                                'solved_game_board': str(boards[1]),
                                'game_start_timestamp': time.time() * 1000.0,
                                'pencil_markups': str(util.init_markup_matrix()),
                                'mistake_fields': str([]),
                                'elapsed_time': 0,
                                'mistakes': 0,
                                'difficulty': board_seed['difficulty'],
                                'hints': hints,
                                'ranked': request.form.get('ranked')}

        return render_template('game.html', start_game=True, game_data=game_data)

    else:
        return redirect('/')


@app.route("/game/save", methods=["GET"])
def save_game():
    logged_in = False
    if 'logged-user' in session:
        logged_in = True

        cookie = session['game_data']
        new_elapsed_time = cookie['elapsed_time'] + (time.time() * 1000.0 - cookie['game_start_timestamp'])
        data_manager.save_game_to_database(cookie['save_id'],
                                           session['logged-user']['id'],
                                           cookie['seed'],
                                           cookie['initial_board'],
                                           cookie['game_state'],
                                           cookie['solved_game_board'],
                                           cookie['pencil_markups'],
                                           cookie['mistake_fields'],
                                           new_elapsed_time,
                                           cookie['mistakes'],
                                           cookie['hints'])

    return render_template('index.html', logged_in=logged_in)


@app.route("/game/load/<save_id>", methods=["POST"])
def load_saved_game(save_id):
    if 'logged-user' in session:
        save_data = data_manager.get_save_data(session['logged-user']['id'], save_id)

        if save_data:
            difficulty = util.get_difficulty(save_data['difficulty'], DIFFICULTY_DICT)
            game_state = util.get_board_as_array(save_data['game_state'])
            initial_board = util.get_board_as_array(save_data['initial_board'])
            pencil_markups = util.get_board_as_array(save_data['pencil_markups'])
            mistake_fields = util.get_board_as_array(save_data['mistake_fields'])

            game_data = {'difficulty': difficulty - 1,
                         'game_state': game_state,
                         'initial_board': initial_board,
                         'elapsed_time': save_data['elapsed_time']//1000,
                         'mistakes': save_data['mistakes'],
                         'hints': save_data['hints'],
                         'pencil_markups': pencil_markups,
                         'mistake_fields': mistake_fields,
                         'ranked': None}

            session['game_data'] = {'save_id': save_id,
                                    'seed': save_data['board_seed_id'],
                                    'initial_board': save_data['initial_board'],
                                    'game_state': save_data['game_state'],
                                    'solved_game_board': save_data['solved_board'],
                                    'game_start_timestamp': time.time() * 1000,
                                    'pencil_markups': save_data['pencil_markups'],
                                    'mistake_fields': save_data['mistake_fields'],
                                    'elapsed_time': save_data['elapsed_time'],
                                    'mistakes': save_data['mistakes'],
                                    'difficulty': save_data['difficulty'],
                                    'hints': save_data['hints'],
                                    'ranked': None}

            return render_template('game.html', start_game=True, game_data=game_data)

        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route("/game/update_game_state", methods=["POST"])
def update_game_state():
    pencil_markups = str(request.json['pencil_markups']).replace(",", ", ")
    game_state = str(request.json['game_state']).replace(",", ", ")
    field_index = eval(request.json['field_index'])

    if game_state == session['game_data']['solved_game_board']:
        data_manager.delete_save_game(session['logged-user']['id'],
                                      session['game_data']['save_id'])

        game_time = session['game_data']['elapsed_time'] + \
                    (time.time() * 1000.0 - session['game_data']['game_start_timestamp'])

        if session['game_data']['ranked']:
            data_manager.add_new_high_score(session['game_data']['seed'],
                                            session['logged-user']['id'],
                                            game_time,
                                            session['game_data']['mistakes'],
                                            session['game_data']['difficulty'])

        data_manager.update_times_solved_column(session['game_data']['seed'])

        return {'won': True,
                'mistakes': session['game_data']['mistakes'],
                'mistake_fields': eval(session['game_data']['mistake_fields'])}

    else:
        session.modified = True

        if eval(game_state)[field_index[0]][field_index[1]] != 0 and \
           eval(session['game_data']['solved_game_board'])[field_index[0]][field_index[1]] != \
           eval(game_state)[field_index[0]][field_index[1]]:

            session['game_data']['mistakes'] += 1
            mistake_fields = eval(session['game_data']['mistake_fields'])
            if field_index not in mistake_fields:
                mistake_fields.append(field_index)
            session['game_data']['mistake_fields'] = str(mistake_fields)

        elif field_index in eval(session['game_data']['mistake_fields']):
            mistake_fields = eval(session['game_data']['mistake_fields'])
            mistake_fields.remove(field_index)
            session['game_data']['mistake_fields'] = str(mistake_fields)

        session['game_data']['pencil_markups'] = pencil_markups
        session['game_data']['game_state'] = game_state

        if session['game_data']['hints'] == 'on':
            return {'won': False,
                    'mistakes': session['game_data']['mistakes'],
                    'mistake_fields': eval(session['game_data']['mistake_fields'])}
        else:
            return {'won': False,
                    'mistakes': 0,
                    'mistake_fields': []}


@app.route("/high_scores", methods=["GET"])
def high_score():
    high_scores = data_manager.get_all_scores()

    # search bar for username, board seed
    order_by_username = request.args.get('username')
    order_by_board_seed = request.args.get('board_seed')
    difficulty_filter = request.args.get('difficulty')
    selected_difficulty_filter = None
    selected_search_by_label = None

    # username search
    if order_by_username:
        high_scores = data_manager.search_high_score_data_by_username(order_by_username)

    # board seed search
    if order_by_board_seed and order_by_board_seed.isnumeric():
        high_scores = data_manager.search_high_score_data_by_board_seed(order_by_board_seed)

    # difficulty filter
    if difficulty_filter:
        if difficulty_filter == '1':
            high_scores = data_manager.get_all_scores()
        else:
            diff_range = DIFFICULTY_DICT[str(int(difficulty_filter) - 1)]
            selected_difficulty_filter = DIFFICULTY_NAME_SCORES_DICT[difficulty_filter]
            high_scores = data_manager.get_high_score_data_by_difficulty(diff_range[0], diff_range[1])

    # difficulty and time format for ux
    for score in high_scores:
        for key in DIFFICULTY_DICT:
            if score['difficulty'] in range(DIFFICULTY_DICT[key][0], DIFFICULTY_DICT[key][1] + 1):
                score['difficulty'] = DIFFICULTY_NAME_DICT[key] + f" ({81-score['difficulty']})"
        score['elapsed_time'] = util.format_time(score['elapsed_time'])

    return render_template('high_scores.html',
                           high_scores=high_scores,
                           selected_difficulty_filter=selected_difficulty_filter,
                           selected_search_by_label=selected_search_by_label)
