import base64
import random
import time
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="Hühnerjagd", layout="wide")


BACKGROUND_IMAGE_PATH = Path("assets/countryside-game-background.jpg")
GRID_SIZE = 4
TOTAL_FIELDS = GRID_SIZE * GRID_SIZE
MAX_ROUNDS = 20
MAX_POINTS_PER_ROUND = 1000
POINT_LOSS_PER_SECOND = 200
TARGET_SYMBOL = "🐔"
EMPTY_FIELD_SYMBOL = " "


def choose_new_target(current_position: int | None = None) -> int:
    possible_positions = list(range(TOTAL_FIELDS))

    if current_position in possible_positions and len(possible_positions) > 1:
        possible_positions.remove(current_position)

    return random.choice(possible_positions)


def calculate_points(elapsed_seconds: float) -> int:
    points = MAX_POINTS_PER_ROUND - elapsed_seconds * POINT_LOSS_PER_SECOND
    return max(0, round(points))


def get_background_image_data_url() -> str:
    image_bytes = BACKGROUND_IMAGE_PATH.read_bytes()
    encoded_image = base64.b64encode(image_bytes).decode("ascii")
    return f"data:image/jpeg;base64,{encoded_image}"


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


def show_theme_styles() -> None:
    background_image_url = get_background_image_data_url()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: #6fa8dc;
        }}

        .block-container {{
            max-width: 1100px;
            padding-top: 1.25rem;
        }}

        .st-key-game_scene {{
            min-height: 640px;
            padding: 1.25rem;
            overflow: hidden;
            cursor: crosshair;
            border: 5px solid #6b3f18;
            border-radius: 8px;
            background-image:
                linear-gradient(180deg, rgba(28, 35, 48, 0.08), rgba(28, 35, 48, 0.18)),
                url("{background_image_url}");
            background-position: center;
            background-size: cover;
            box-shadow: 0 14px 35px rgba(37, 24, 10, 0.35);
        }}

        .st-key-game_scene h1 {{
            margin-bottom: 0.2rem;
            font-size: clamp(2.15rem, 6vw, 3.5rem);
        }}

        .st-key-game_scene h1,
        .st-key-game_scene p,
        .st-key-game_scene label {{
            color: white;
            text-shadow:
                0 2px 0 #1f1f1f,
                0 0 6px rgba(0, 0, 0, 0.75);
        }}

        .game-hud {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 0.8rem 0;
        }}

        .game-hud-item,
        .game-message {{
            min-width: 130px;
            padding: 0.55rem 0.8rem;
            border: 2px solid rgba(255, 255, 255, 0.72);
            border-radius: 8px;
            background: rgba(30, 23, 15, 0.52);
            box-shadow: 0 5px 14px rgba(0, 0, 0, 0.22);
        }}

        .game-hud-label {{
            display: block;
            color: white;
            font-size: 0.9rem;
        }}

        .game-hud-value {{
            display: block;
            color: #fff7d0;
            font-size: clamp(1.6rem, 5vw, 2.2rem);
            font-weight: 800;
            line-height: 1.1;
            text-shadow:
                0 2px 0 #1f1f1f,
                0 0 8px rgba(0, 0, 0, 0.85);
        }}

        .st-key-game_board {{
            display: grid;
            grid-template-columns: repeat({GRID_SIZE}, minmax(0, 1fr));
            gap: 0.35rem;
            min-height: 300px;
            margin-top: 0.7rem;
            cursor: crosshair;
        }}

        .st-key-game_board [data-testid="stElementContainer"] {{
            min-width: 0;
        }}

        .st-key-game_board [data-testid="stButton"] button {{
            min-height: clamp(70px, 12vw, 100px);
            cursor: crosshair;
            border: 0;
            border-radius: 50%;
            background: transparent;
            box-shadow: none;
            color: #fff2a0;
            font-size: clamp(3.4rem, 8vw, 5.5rem);
            text-shadow:
                0 4px 0 #5a2d12,
                0 0 9px rgba(0, 0, 0, 0.55);
            transition: transform 120ms ease, filter 120ms ease;
        }}

        .st-key-game_board [data-testid="stButton"] button div,
        .st-key-game_board [data-testid="stButton"] button p {{
            font-size: inherit;
            line-height: 1;
            margin: 0;
        }}

        .st-key-game_board [data-testid="stButton"] button:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: scale(1.08);
            filter: saturate(1.18);
        }}

        .st-key-game_board [data-testid="stButton"] button:disabled {{
            color: transparent;
            background: transparent;
        }}

        .st-key-new_game_button [data-testid="stButton"] button {{
            border: 2px solid #f5d180;
            border-radius: 8px;
            background: linear-gradient(180deg, #8f4d21, #5f2c14);
            color: #fff7d0;
            font-weight: 700;
            box-shadow: 0 4px 0 #35180c;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hud() -> None:
    current_round = min(st.session_state.round_number, MAX_ROUNDS)

    st.markdown(
        f"""
        <div class="game-hud">
            <div class="game-hud-item">
                <span class="game-hud-label">Punkte</span>
                <span class="game-hud-value">{st.session_state.score}</span>
            </div>
            <div class="game-hud-item">
                <span class="game-hud-label">Runde</span>
                <span class="game-hud-value">{current_round} / {MAX_ROUNDS}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_status() -> None:
    if st.session_state.last_click_time is not None:
        st.markdown(
            f"""
            <div class="game-message">
                Letzter Treffer: {st.session_state.last_click_time:.2f} Sekunden,
                {st.session_state.last_round_points} Punkte
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.game_over:
        st.success("Spiel beendet. Starte ein neues Spiel, wenn du noch einmal spielen möchtest.")


def show_game_board() -> None:
    with st.container(key="game_board"):
        for position in range(TOTAL_FIELDS):
            is_target = position == st.session_state.target_position and not st.session_state.game_over
            label = TARGET_SYMBOL if is_target else EMPTY_FIELD_SYMBOL

            st.button(
                label,
                key=f"field_{position}",
                on_click=handle_field_click,
                args=(position,),
                use_container_width=True,
                disabled=st.session_state.game_over,
            )


def show_game() -> None:
    show_theme_styles()

    with st.container(key="game_scene"):
        st.title("Hühnerjagd")
        st.write("Klicke mit dem Fadenkreuz auf das Huhn.")
        show_hud()
        show_status()

        with st.container(key="new_game_button"):
            st.button("Neues Spiel", on_click=reset_game)

        show_game_board()


initialize_game_state()
show_game()
