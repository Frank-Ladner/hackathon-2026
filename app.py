import random

import streamlit as st


GRID_SIZE = 4
TOTAL_FIELDS = GRID_SIZE * GRID_SIZE


def choose_new_target(current_position: int | None = None) -> int:
    possible_positions = list(range(TOTAL_FIELDS))

    if current_position in possible_positions and len(possible_positions) > 1:
        possible_positions.remove(current_position)

    return random.choice(possible_positions)


def initialize_game_state() -> None:
    if "score" not in st.session_state:
        st.session_state.score = 0

    if "target_position" not in st.session_state:
        st.session_state.target_position = choose_new_target()


def reset_game() -> None:
    st.session_state.score = 0
    st.session_state.target_position = choose_new_target()


def handle_field_click(position: int) -> None:
    if position != st.session_state.target_position:
        return

    st.session_state.score += 1
    st.session_state.target_position = choose_new_target(position)


def show_game() -> None:
    st.title("Zielscheiben-Spiel")
    st.write("Klicke mit dem Mauszeiger auf das Feld mit dem Ziel.")

    st.metric("Punkte", st.session_state.score)
    st.button("Neues Spiel", on_click=reset_game)

    for row in range(GRID_SIZE):
        columns = st.columns(GRID_SIZE)

        for column_index, column in enumerate(columns):
            position = row * GRID_SIZE + column_index
            label = "Ziel" if position == st.session_state.target_position else "."

            column.button(
                label,
                key=f"field_{position}",
                on_click=handle_field_click,
                args=(position,),
                use_container_width=True,
            )


initialize_game_state()
show_game()
