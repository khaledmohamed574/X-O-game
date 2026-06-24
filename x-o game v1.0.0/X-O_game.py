class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name, try again.")

    def choose_symbol(self, taken_symbols=None):
        taken_symbols = taken_symbols or []
        while True:
            symbol = input(f"{self.name}, enter your symbol (one character only): ")
            if len(symbol) == 1 and symbol.isalpha():
                symbol = symbol.upper()
                if symbol in taken_symbols:
                    print(f"Symbol '{symbol}' is already taken, choose another.")
                    continue
                self.symbol = symbol
                break
            print("Invalid symbol, try again.")


class Menu:
    def display_main_menu(self):
        print("Welcome to X-O game!")
        print("1* Start game")
        print("2* Exit")
        choice = input("Enter your choice (1 or 2): ")
        while choice not in ["1", "2"]:
            print("Invalid choice, try again.")
            choice = input("Enter your choice (1 or 2): ")
        return choice

    def display_endgame_menu(self):
        menu_text = """
Game over!
1* Restart game
2* Exit
"""
        choice = input(menu_text + "Enter your choice (1 or 2): ")
        while choice not in ["1", "2"]:
            print("Invalid choice, try again.")
            choice = input(menu_text + "Enter your choice (1 or 2): ")
        return choice


class Board:
    SIZE = 3

    def __init__(self):
        self.board = [
            [str(self.position_to_choice(row, col)) for col in range(self.SIZE)]
            for row in range(self.SIZE)
        ]

    def choice_to_position(self, choice):
        """Map player input 1-9 to board (row, col)."""
        if choice < 1 or choice > 9:
            raise ValueError("Choice must be between 1 and 9.")
        index = choice - 1
        return index // self.SIZE, index % self.SIZE

    def position_to_choice(self, row, col):
        """Map board (row, col) back to player input 1-9."""
        return row * self.SIZE + col + 1

    def is_number(self, cell):
        return cell.isdigit() and 1 <= int(cell) <= 9

    def display_board(self):
        for row in range(self.SIZE):
            print(" | ".join(self.board[row]))
            if row != self.SIZE - 1:
                print("---------")

    def is_valid_move(self, choice):
        if choice < 1 or choice > 9:
            return False
        row, col = self.choice_to_position(choice)
        return self.is_number(self.board[row][col])

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            row, col = self.choice_to_position(choice)
            self.board[row][col] = symbol
            return True
        return False

    def reset_board(self):
        self.board = [
            [str(self.position_to_choice(row, col)) for col in range(self.SIZE)]
            for row in range(self.SIZE)
        ]

    def is_full(self):
        return all(not self.is_number(cell) for row in self.board for cell in row)

    def flat_board(self):
        return [cell for row in self.board for cell in row]


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            self.setup_players()
            self.play_game()
        else:
            self.exit_game()

    def setup_players(self):
        taken_symbols = []
        print("\nBoard positions:")
        print(" 1 | 2 | 3")
        print("-----------")
        print(" 4 | 5 | 6")
        print("-----------")
        print(" 7 | 8 | 9\n")
        for number, player in enumerate(self.players, start=1):
            print(f"Player {number}, enter your details:")
            player.choose_name()
            player.choose_symbol(taken_symbols)
            taken_symbols.append(player.symbol)
            print(f"{player.name}, your symbol is {player.symbol}")
            print("*" * 20)

    def play_game(self):
        while True:
            self.play_turn()

            if self.check_win():
                self.board.display_board()
                winner = self.players[1 - self.current_player_index]
                print(f"Congratulations {winner.name}! You win!")
            elif self.check_draw():
                self.board.display_board()
                print("It's a draw!")

            if self.check_win() or self.check_draw():
                choice = self.menu.display_endgame_menu()
                if choice == "1":
                    self.restart_game()
                else:
                    self.exit_game()
                    break

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6],             # diagonals
        ]
        flat = self.board.flat_board()
        for combo in win_combinations:
            if flat[combo[0]] == flat[combo[1]] == flat[combo[2]] and not self.board.is_number(flat[combo[0]]):
                return True
        return False

    def check_draw(self):
        return self.board.is_full() and not self.check_win()

    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name} ({player.symbol}), it's your turn!")
        while True:
            try:
                cell_choice = int(input("Enter your move (1-9): "))
                if self.board.update_board(cell_choice, player.symbol):
                    break
                print("Invalid move, try again.")
            except ValueError:
                print("Please enter a valid number between 1 and 9.")
        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def exit_game(self):
        print("Thank you for playing!")


if __name__ == "__main__":
    game = Game()
    game.start_game()
