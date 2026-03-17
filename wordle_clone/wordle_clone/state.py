import reflex as rx
import random
from .words import VALID_WORDS, ANSWERS

class State(rx.State):
    """The app state."""
    
    answer: str = ""
    guesses: list[str] = []
    current_guess: str = ""
    game_over: bool = False
    game_won: bool = False
    message: str = ""
    message_open: bool = False

    def _initialize(self):
        if not self.answer:
            self.answer = random.choice(ANSWERS)
            print(f"DEBUG: Current Wordle Answer is -> {self.answer}")
            
    def on_load(self):
        self._initialize()

    def restart_game(self):
        self.answer = random.choice(ANSWERS)
        self.guesses = []
        self.current_guess = ""
        self.game_over = False
        self.game_won = False
        self.show_message("Game Restarted!")
        
    def show_message(self, msg: str):
        self.message = msg
        self.message_open = True
        
    def close_message(self, _=None):
        self.message_open = False

    def handle_key_down(self, key_payload: str):
        # Strip timestamp that JS frontend attaches to bypass React state blocking
        key = key_payload.split("_")[0] if "_" in key_payload else key_payload
        
        if self.message_open and key == "Escape":
            self.message_open = False
            return
            
        if self.game_over:
            return
            
        if key == "Enter":
            self.submit_guess()
        elif key == "Backspace":
            self.remove_letter()
        elif len(key) == 1 and key.isalpha():
            self.add_letter(key.upper())

    def add_letter(self, letter: str):
        if self.game_over: return
        if len(self.current_guess) < 5:
            self.current_guess += letter.upper()

    def remove_letter(self):
        if self.game_over: return
        if len(self.current_guess) > 0:
            self.current_guess = self.current_guess[:-1]

    def submit_guess(self):
        if self.game_over: return
        if len(self.current_guess) < 5:
            self.show_message("Not enough letters")
            return
        
        guess_upper = self.current_guess.upper()
        if guess_upper not in VALID_WORDS:
            self.show_message("Not in word list")
            return
            
        self.guesses.append(guess_upper)
        self.current_guess = ""
        
        if guess_upper == self.answer:
            self.game_won = True
            self.game_over = True
            self.show_message("Splendid! You guessed the word!")
        elif len(self.guesses) >= 6:
            self.game_won = False
            self.game_over = True
            self.show_message(f"Game Over. The word was {self.answer}")

    @rx.var
    def share_text(self) -> str:
        if not self.answer: return ""
        text = f"Wordle Clone {len(self.guesses)}/6\n\n"
        for guess in self.guesses:
            answer_letters = list(self.answer)
            colors = ["⬜"] * 5
            for i, char in enumerate(guess):
                if char == self.answer[i]:
                    colors[i] = "🟦"
                    answer_letters[i] = None
            for i, char in enumerate(guess):
                if colors[i] == "⬜" and char in answer_letters:
                    colors[i] = "🟨"
                    answer_letters[answer_letters.index(char)] = None
            text += "".join(colors) + "\n"
        return text.strip()

    @rx.var
    def letter_statuses(self) -> dict[str, str]:
        if not self.answer: return {}
        status_map = {}
        for guess in self.guesses:
            answer_letters = list(self.answer)
            for i, char in enumerate(guess):
                if char == self.answer[i]:
                    status_map[char] = "correct"
                    answer_letters[i] = None
            for i, char in enumerate(guess):
                if char == self.answer[i]: continue
                if char in answer_letters:
                    if status_map.get(char) != "correct":
                        status_map[char] = "present"
                    answer_letters[answer_letters.index(char)] = None
                else:
                    if char not in status_map:
                        status_map[char] = "absent"
        return status_map

    @rx.var
    def letter_colors(self) -> dict[str, str]:
        statuses = self.letter_statuses
        colors = {}
        for char, status in statuses.items():
            if status == "correct":
                colors[char] = "#0ea5e9"
            elif status == "present":
                colors[char] = "#d4af37"
            else:
                colors[char] = "#e5e7eb"
        return colors

    @rx.var
    def grid(self) -> list[list[dict[str, str]]]:
        if not self.answer: return []
        grid_data = []
        for guess in self.guesses:
            row = []
            answer_letters = list(self.answer)
            statuses = ["absent"] * 5
            for i, char in enumerate(guess):
                if char == self.answer[i]:
                    statuses[i] = "correct"
                    answer_letters[i] = None
            for i, char in enumerate(guess):
                if statuses[i] == "absent" and char in answer_letters:
                    statuses[i] = "present"
                    answer_letters[answer_letters.index(char)] = None
            
            for i, char in enumerate(guess):
                color = "#e5e7eb" # absent
                if statuses[i] == "correct": color = "#0ea5e9"
                elif statuses[i] == "present": color = "#d4af37"
                row.append({"letter": char, "status": statuses[i], "color": color, "font_color": "white" if statuses[i] != "absent" else "#0f172a"})
            grid_data.append(row)
            
        if len(self.guesses) < 6 and not self.game_over:
            current_row = []
            for i in range(5):
                if i < len(self.current_guess):
                    current_row.append({"letter": self.current_guess[i], "status": "typing", "color": "transparent", "font_color": "#0f172a"})
                else:
                    current_row.append({"letter": "", "status": "empty", "color": "transparent", "font_color": "#0f172a"})
            grid_data.append(current_row)
            
        while len(grid_data) < 6:
            empty_row = [{"letter": "", "status": "empty", "color": "transparent", "font_color": "#0f172a"} for _ in range(5)]
            grid_data.append(empty_row)
            
        return grid_data
