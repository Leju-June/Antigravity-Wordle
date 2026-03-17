"""Welcome to Wordle Clone."""

import reflex as rx
from .state import State
from .components import grid, keyboard, result_modal

style = {
    "font_family": "Inter, sans-serif",
    ":root": {
        "--slate-4": "#f1f5f9",
        "--slate-6": "#cbd5e1",
        "--slate-8": "#94a3b8",
        "--slate-12": "#0f172a",
        "--green-9": "#22c55e",
        "--amber-9": "#eab308",
    }
}

class GlobalKeyListener(rx.Fragment):
    """Component to catch global keydowns."""

    def add_imports(self) -> dict[str, str | list[str]]:
        return {"react": ["useEffect"]}

    def _get_hooks(self) -> str:
        return f"""
        useEffect(() => {{
            const handleKeyDown = (e) => {{
                // Ignore keydowns if modifier keys are pressed
                if (e.ctrlKey || e.metaKey || e.altKey) return;
                
                // Allow only certain keys
                if (e.key === "Enter" || e.key === "Backspace" || e.key === "Escape" || (e.key.length === 1 && e.key.match(/[a-zA-Z]/i))) {{
                    {rx.utils.format.format_event(State.handle_key_down(rx.Var("e.key")))}
                }}
            }};
            window.addEventListener('keydown', handleKeyDown);
            return () => window.removeEventListener('keydown', handleKeyDown);
        }}, []);
        """

def global_key_listener() -> rx.Component:
    return GlobalKeyListener.create()

def index() -> rx.Component:
    return rx.center(
        # Hook global key listener to the page
        global_key_listener(),
        rx.vstack(
            rx.heading("Wordle Clone", size="8", weight="bold", margin_y="4"),
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
