"""Welcome to Wordle Clone."""

import reflex as rx
from .state import State
from .components import grid, keyboard, result_modal

style = {
    "font_family": "Inter, sans-serif",
    ":root": {
        "--slate-4": "#f8fafc",
        "--slate-6": "#e2e8f0",
        "--light-gray": "#e5e7eb",
        "--slate-8": "#e5e7eb",
        "--slate-12": "#0f172a",
        "--sky-blue": "#0ea5e9",
        "--gold": "#d4af37",
    }
}

def index() -> rx.Component:
    return rx.center(
        # Hook global key listener to the page
        rx.script("""
            window.addEventListener('keydown', function(e) {
                // Ignore keydowns if modifier keys are pressed
                if (e.ctrlKey || e.metaKey || e.altKey) return;
                
                // Allow only certain keys
                if (e.key === "Enter" || e.key === "Backspace" || e.key === "Escape" || (e.key.length === 1 && e.key.match(/[a-zA-Z]/i))) {
                    var input = document.getElementById('hidden_trigger');
                    if (input) {
                        let setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                        // Append timestamp so consecutive repeated keys still trigger on_change!
                        setter.call(input, e.key + "_" + Date.now());
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
            });
        """),
        rx.input(
            id="hidden_trigger",
            style={"display": "none"},
            on_change=State.handle_key_down,
        ),
        rx.vstack(
            rx.heading(f"Wordle Clone (Answer: {State.answer})", size="8", weight="bold", margin_y="4"),
            rx.divider(),
            rx.spacer(),
            # Grid
            grid(),
            rx.spacer(),
            # Keyboard 
            keyboard(),
            result_modal(),
            
            align="center",
            width="100%",
            height="100vh",
            max_width="600px",
            justify="between",
        ),
        width="100%",
        on_mount=State.on_load,
    )

app = rx.App(style=style)
app.add_page(index, title="Wordle Clone")
