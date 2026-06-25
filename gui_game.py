import tkinter as tk
from tkinter import messagebox


def _is_valid_name(name):
    stripped = name.strip()
    return bool(stripped) and all(ch.isalpha() or ch.isspace() for ch in stripped)


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("X-O Game")
        self.root.geometry("470x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")

        self.colors = {
            "bg": "#0F172A",
            "card": "#1E293B",
            "muted": "#94A3B8",
            "text": "#E2E8F0",
            "accent": "#38BDF8",
            "success": "#22C55E",
            "danger": "#EF4444",
            "cell_idle": "#334155",
            "cell_hover": "#475569",
            "cell_disabled": "#1F2937",
        }

        self.players = [
            {"name": "Player 1", "symbol": "X"},
            {"name": "Player 2", "symbol": "O"},
        ]
        self.current_player_index = 0
        self.board = [" "] * 9
        self.buttons = []
        self.scores = {
            "player_1": 0,
            "player_2": 0,
            "draws": 0,
        }

        self.start_frame = tk.Frame(self.root, padx=24, pady=24, bg=self.colors["bg"])
        self.game_frame = tk.Frame(self.root, padx=20, pady=18, bg=self.colors["bg"])

        self._build_start_screen()
        self._build_game_screen()
        self.start_frame.pack(fill="both", expand=True)

    def _build_start_screen(self):
        title = tk.Label(
            self.start_frame,
            text="Welcome To X-O",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        )
        title.pack(pady=(8, 6))

        subtitle = tk.Label(
            self.start_frame,
            text="Customize players then start the match",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        )
        subtitle.pack(pady=(0, 18))

        p1_frame = tk.LabelFrame(
            self.start_frame,
            text="Player 1",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=8,
        )
        p1_frame.pack(fill="x", pady=8)
        tk.Label(
            p1_frame,
            text="Name",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        tk.Label(
            p1_frame,
            text="Symbol",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.p1_name_entry = tk.Entry(
            p1_frame,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="flat",
        )
        self.p1_symbol_entry = tk.Entry(
            p1_frame,
            width=5,
            font=("Segoe UI", 10, "bold"),
            bg="#F8FAFC",
            relief="flat",
        )
        self.p1_name_entry.insert(0, "Player One")
        self.p1_symbol_entry.insert(0, "X")
        self.p1_name_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        self.p1_symbol_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        p1_frame.grid_columnconfigure(1, weight=1)

        p2_frame = tk.LabelFrame(
            self.start_frame,
            text="Player 2",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=8,
        )
        p2_frame.pack(fill="x", pady=8)
        tk.Label(
            p2_frame,
            text="Name",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        tk.Label(
            p2_frame,
            text="Symbol",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.p2_name_entry = tk.Entry(
            p2_frame,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="flat",
        )
        self.p2_symbol_entry = tk.Entry(
            p2_frame,
            width=5,
            font=("Segoe UI", 10, "bold"),
            bg="#F8FAFC",
            relief="flat",
        )
        self.p2_name_entry.insert(0, "Player Two")
        self.p2_symbol_entry.insert(0, "O")
        self.p2_name_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        self.p2_symbol_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        p2_frame.grid_columnconfigure(1, weight=1)

        start_btn = tk.Button(
            self.start_frame,
            text="Start Game",
            font=("Segoe UI", 12, "bold"),
            command=self.start_game,
            bg=self.colors["success"],
            fg="white",
            activebackground="#16A34A",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
        )
        start_btn.pack(pady=18)

    def _build_game_screen(self):
        score_card = tk.Frame(self.game_frame, bg=self.colors["card"], padx=14, pady=10)
        score_card.pack(fill="x", pady=(0, 10))

        self.score_label = tk.Label(
            score_card,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            anchor="w",
        )
        self.score_label.pack(fill="x")

        self.status_label = tk.Label(
            self.game_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            pady=10,
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        )
        self.status_label.pack()

        board_frame = tk.Frame(self.game_frame, bg=self.colors["bg"])
        board_frame.pack(pady=10)

        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 26, "bold"),
                width=4,
                height=2,
                command=lambda idx=i: self.make_move(idx),
                bg=self.colors["cell_idle"],
                fg=self.colors["text"],
                activebackground=self.colors["cell_hover"],
                activeforeground=self.colors["text"],
                relief="flat",
                bd=0,
            )
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            btn.bind("<Enter>", lambda _, b=btn: self._on_cell_hover(b))
            btn.bind("<Leave>", lambda _, b=btn: self._on_cell_leave(b))
            self.buttons.append(btn)

        control_frame = tk.Frame(self.game_frame, bg=self.colors["bg"])
        control_frame.pack(pady=12)

        restart_btn = tk.Button(
            control_frame,
            text="Restart",
            font=("Segoe UI", 11, "bold"),
            command=self.reset_board,
            width=10,
            bg="#3B82F6",
            fg="white",
            activebackground="#2563EB",
            activeforeground="white",
            relief="flat",
        )
        restart_btn.grid(row=0, column=0, padx=8)

        reset_score_btn = tk.Button(
            control_frame,
            text="Reset Score",
            font=("Segoe UI", 11, "bold"),
            command=self.reset_scores,
            width=10,
            bg="#F59E0B",
            fg="white",
            activebackground="#D97706",
            activeforeground="white",
            relief="flat",
        )
        reset_score_btn.grid(row=0, column=1, padx=8)

        exit_btn = tk.Button(
            control_frame,
            text="Exit",
            font=("Segoe UI", 11, "bold"),
            command=self.root.destroy,
            width=10,
            bg=self.colors["danger"],
            fg="white",
            activebackground="#DC2626",
            activeforeground="white",
            relief="flat",
        )
        exit_btn.grid(row=0, column=2, padx=8)

    def _on_cell_hover(self, btn):
        if btn["state"] == "normal":
            btn.config(bg=self.colors["cell_hover"])

    def _on_cell_leave(self, btn):
        if btn["state"] == "normal":
            btn.config(bg=self.colors["cell_idle"])

    def start_game(self):
        p1_name = self.p1_name_entry.get().strip()
        p2_name = self.p2_name_entry.get().strip()
        p1_symbol = self.p1_symbol_entry.get().strip().upper()
        p2_symbol = self.p2_symbol_entry.get().strip().upper()

        if not _is_valid_name(p1_name) or not _is_valid_name(p2_name):
            messagebox.showerror("Invalid Input", "Names must contain letters and spaces only.")
            return

        if len(p1_symbol) != 1 or len(p2_symbol) != 1 or not p1_symbol.isalpha() or not p2_symbol.isalpha():
            messagebox.showerror("Invalid Input", "Each symbol must be one letter.")
            return

        if p1_symbol == p2_symbol:
            messagebox.showerror("Invalid Input", "Players cannot use the same symbol.")
            return

        self.players[0]["name"] = p1_name
        self.players[0]["symbol"] = p1_symbol
        self.players[1]["name"] = p2_name
        self.players[1]["symbol"] = p2_symbol

        self.current_player_index = 0
        self.reset_board()
        self.update_scores()
        self.start_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def make_move(self, index):
        if self.board[index] != " ":
            return

        current_player = self.players[self.current_player_index]
        self.board[index] = current_player["symbol"]
        symbol_color = "#A5F3FC" if self.current_player_index == 0 else "#FDE68A"
        self.buttons[index].config(
            text=current_player["symbol"],
            state="disabled",
            bg=self.colors["cell_disabled"],
            fg=symbol_color,
            disabledforeground=symbol_color,
        )

        win_combo = self.check_win()
        if win_combo:
            for combo_index in win_combo:
                self.buttons[combo_index].config(bg=self.colors["success"], fg="white", disabledforeground="white")
            if self.current_player_index == 0:
                self.scores["player_1"] += 1
            else:
                self.scores["player_2"] += 1
            self.update_scores()
            self.end_game(f"{current_player['name']} wins!")
            return

        if self.check_draw():
            self.scores["draws"] += 1
            self.update_scores()
            self.end_game("It's a draw!")
            return

        self.current_player_index = 1 - self.current_player_index
        self.update_status()

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
        for a, b, c in win_combinations:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return [a, b, c]
        return None

    def check_draw(self):
        return all(cell != " " for cell in self.board)

    def end_game(self, result_message):
        for btn in self.buttons:
            btn.config(state="disabled")

        play_again = messagebox.askyesno("Game Over", f"{result_message}\n\nPlay again?")
        if play_again:
            self.reset_board()
        else:
            self.root.destroy()

    def update_status(self):
        player = self.players[self.current_player_index]
        self.status_label.config(text=f"{player['name']} ({player['symbol']}) turn")

    def update_scores(self):
        self.score_label.config(
            text=(
                f"{self.players[0]['name']}: {self.scores['player_1']}   |   "
                f"{self.players[1]['name']}: {self.scores['player_2']}   |   "
                f"Draws: {self.scores['draws']}"
            )
        )

    def reset_board(self):
        self.board = [" "] * 9
        for btn in self.buttons:
            btn.config(
                text="",
                state="normal",
                bg=self.colors["cell_idle"],
                fg=self.colors["text"],
                activebackground=self.colors["cell_hover"],
                activeforeground=self.colors["text"],
            )
        self.update_status()

    def reset_scores(self):
        self.scores = {"player_1": 0, "player_2": 0, "draws": 0}
        self.update_scores()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
