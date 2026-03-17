import reflex as rx
from .state import State

color_map = {
    "correct": "#0ea5e9",  # Sky Blue
    "present": "#d4af37",  # Gold
    "absent": "#e5e7eb",   # Light Gray
    "empty": "transparent",
    "typing": "transparent"
}

border_map = {
    "correct": "none",
    "present": "none",
    "absent": "none",
    "empty": "2px solid var(--slate-6)",
    "typing": "2px solid var(--slate-8)"
}

font_color_map = {
    "correct": "white",
    "present": "white",
    "absent": "var(--slate-12)",
    "typing": "var(--slate-12)",
    "empty": "var(--slate-12)"
}

def cell(item: dict) -> rx.Component:
    """A single cell in the grid."""
    letter = item["letter"]
    
    return rx.flex(
        rx.text(letter, size="8", weight="bold", color=item["font_color"]),
        align="center",
        justify="center",
        width=["48px", "62px"],
        height=["48px", "62px"],
        border=border_map.get(item["status"], border_map["empty"]),
        bg=item["color"],
        border_radius="md",
        transition="all 0.4s ease-in-out",
        # Adding some pop animation if it's currently typed
        transform=rx.cond(item["status"] == "typing", "scale(1.05)", "scale(1)"),
    )

def row(row_data: list[dict]) -> rx.Component:
    """A row of 5 cells."""
    return rx.hstack(
        rx.foreach(row_data, cell),
        spacing="2"
    )

def grid() -> rx.Component:
    return rx.vstack(
        rx.foreach(State.grid, row),
        spacing="2",
        padding="4",
    )

def keyboard_key(key: str, flex: str = "1") -> rx.Component:
    bg_color = State.letter_colors.get(key, "var(--slate-4)")
    text_color = rx.cond(
        State.letter_statuses.get(key) == "absent",
        "var(--slate-12)",
        rx.cond(
            State.letter_statuses.get(key) == "empty",
            "var(--slate-12)",
            "white"
        )
    )
    
    return rx.button(
        key,
        on_click=State.handle_key_down(key),
        bg=bg_color,
        color=text_color,
        flex=flex,
        height="58px",
        font_weight="bold",
        font_size=["12px", "14px"],
        border_radius="md",
        _hover={"opacity": 0.8},
    )

def keyboard() -> rx.Component:
    row1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
    row2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
    row3 = ["Z", "X", "C", "V", "B", "N", "M"]
    
    return rx.vstack(
        rx.hstack(
            *[keyboard_key(k) for k in row1],
            spacing="1",
            width="100%",
            justify="center",
        ),
        rx.hstack(
            *[keyboard_key(k) for k in row2],
            spacing="1",
            width="90%",
            justify="center",
        ),
        rx.hstack(
            keyboard_key("Enter", flex="1.5"),
            *[keyboard_key(k) for k in row3],
            keyboard_key("Backspace", flex="1.5"),
            spacing="1",
            width="100%",
            justify="center",
        ),
        width=["100%", "500px"],
        spacing="2",
        padding="4",
    )

def result_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Wordle Clone", align="center"),
            rx.dialog.description(
                rx.vstack(
                    rx.text(State.message, size="6", weight="bold", align="center"),
                    rx.cond(
                        State.game_over,
                        rx.box(
                            rx.text("Your Result:", align="center", size="3"),
                            # Shows the emojis block natively
                            rx.code(State.share_text, align="center", text_align="center", display="block", white_space="pre-wrap", mt="2", mb="4"),
                            rx.hstack(
                                rx.button(
                                    rx.icon("copy"),
                                    "Share", 
                                    on_click=rx.set_clipboard(State.share_text),
                                    color_scheme="sky"
                                ),
                                rx.button(
                                    rx.icon("rotate-cw"),
                                    "Play Again",
                                    on_click=State.restart_game,
                                    color_scheme="blue"
                                ),
                                justify="center",
                                width="100%"
                            ),
                            width="100%"
                        ),
                        rx.button("OK", on_click=State.close_message, width="100%")
                    )
                )
            ),
            max_width="400px",
        ),
        open=State.message_open,
        on_open_change=State.close_message,
    )
