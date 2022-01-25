ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.saved_games DROP CONSTRAINT IF EXISTS pk_saved_game_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.saved_games DROP CONSTRAINT IF EXISTS fk_board_seed_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.saved_games DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.scores DROP CONSTRAINT IF EXISTS pk_scores_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.scores DROP CONSTRAINT IF EXISTS fk_board_seed_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.scores DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.game_boards DROP CONSTRAINT IF EXISTS pk_game_board_id CASCADE;

DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    h_password text,
    email text,
    reg_date timestamp without time zone
);

DROP TABLE IF EXISTS public.saved_games;
CREATE TABLE saved_games (
    id serial NOT NULL,
    user_id int,
    board_seed_id int,
    initial_board text,
    game_state text,
    solved_board text,
    pencil_markups text,
    mistake_fields text,
    elapsed_time int,
    timestamp timestamp without time zone,
    mistakes int,
    hints bool
);

DROP TABLE IF EXISTS public.game_boards;
CREATE TABLE game_boards (
    id serial NOT NULL,
    difficulty int,
    board text,
    solved_board text,
    times_solved int
);

DROP TABLE IF EXISTS public.scores;
CREATE TABLE scores (
    id serial NOT NULL,
    board_seed_id int,
    user_id int,
    elapsed_time int,
    mistakes int,
    difficulty int
);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY saved_games
    ADD CONSTRAINT pk_saved_game_id PRIMARY KEY (id);

ALTER TABLE ONLY game_boards
    ADD CONSTRAINT pk_game_board_id PRIMARY KEY (id);

ALTER TABLE ONLY scores
    ADD CONSTRAINT pk_scores_id PRIMARY KEY (id);

ALTER TABLE ONLY saved_games
    ADD CONSTRAINT fk_board_seed_id FOREIGN KEY (board_seed_id) REFERENCES game_boards(id) ON DELETE CASCADE;

ALTER TABLE ONLY saved_games
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY scores
    ADD CONSTRAINT fk_board_seed_id FOREIGN KEY (board_seed_id) REFERENCES game_boards(id) ON DELETE CASCADE;

ALTER TABLE ONLY scores
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
