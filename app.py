import random
import time

import streamlit as st


GRID_SIZE = 4
TOTAL_FIELDS = GRID_SIZE * GRID_SIZE
MAX_ROUNDS = 20
POINTS_PER_SECOND = 100


def choose_new_target(current_position: int | None = None) -> int:
    possible_positions = list(range(TOTAL_FIELDS))

    if current_position in possible_positions and len(possible_positions) > 1:
        possible_positions.remove(current_position)

    return random.choice(possible_positions)


def calculate_points(elapsed_seconds: float) -> int:
    return round(elapsed_seconds * POINTS_PER_SECOND)


def start_next_round(current_position: int | None = None) -> None:
    st.session_state.target_position = choose_new_target(current_position)
    st.session_state.round_started_at = time.monotonic()


def initialize_game_state() -> None:
    if "score" not in st.session_state:
        st.session_state.score = 0

    if "round_number" not in st.session_state:
        st.session_state.round_number = 1

    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    if "last_click_time" not in st.session_state:
        st.session_state.last_click_time = None

    if "last_round_points" not in st.session_state:
        st.session_state.last_round_points = 0

    if "target_position" not in st.session_state or "round_started_at" not in st.session_state:
        start_next_round()


def reset_game() -> None:
    st.session_state.score = 0
    st.session_state.round_number = 1
    st.session_state.game_over = False
    st.session_state.last_click_time = None
    st.session_state.last_round_points = 0
    start_next_round()


def handle_field_click(position: int) -> None:
    if st.session_state.game_over:
        return

    if position != st.session_state.target_position:
        return

    elapsed_seconds = time.monotonic() - st.session_state.round_started_at
    round_points = calculate_points(elapsed_seconds)

    st.session_state.score += round_points
    st.session_state.last_click_time = elapsed_seconds
    st.session_state.last_round_points = round_points

    if st.session_state.round_number >= MAX_ROUNDS:
        st.session_state.game_over = True
        return

    st.session_state.round_number += 1
    start_next_round(position)


def show_game() -> None:
    st.title("Zielscheiben-Spiel")
    st.write("Klicke mit dem Mauszeiger auf das Feld mit dem Ziel.")

    current_round = min(st.session_state.round_number, MAX_ROUNDS)

    score_column, round_column = st.columns(2)
    score_column.metric("Punkte", st.session_state.score)
    round_column.metric("Runde", f"{current_round} / {MAX_ROUNDS}")

    if st.session_state.last_click_time is not None:
        st.write(
            f"Letzter Treffer: {st.session_state.last_click_time:.2f} Sekunden, "
            f"{st.session_state.last_round_points} Punkte"
        )

    if st.session_state.game_over:
        st.success("Spiel beendet. Starte ein neues Spiel, wenn du noch einmal spielen möchtest.")

    st.button("Neues Spiel", on_click=reset_game)

    for row in range(GRID_SIZE):
        columns = st.columns(GRID_SIZE)

        for column_index, column in enumerate(columns):
            position = row * GRID_SIZE + column_index
            is_target = position == st.session_state.target_position and not st.session_state.game_over
            label = "Ziel" if is_target else "."

            column.button(
                label,
                key=f"field_{position}",
                on_click=handle_field_click,
                args=(position,),
                use_container_width=True,
                disabled=st.session_state.game_over,
            )


initialize_game_state()
show_game()
