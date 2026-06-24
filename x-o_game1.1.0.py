class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                return
            print("Invalid name. Try again.")

    def choose_symbol(self):
        while True:
            symbol = input(f"{self.name}, enter your symbol (one character only): ")
            if len(symbol) == 1 and symbol.isalpha():
                self.symbol = symbol.upper()
                return
            print("Invalid symbol. Try again.")


class Menu:
    def display_main_menu(self):
        print("\nWelcome to X-O Game")
        print("1. Start Game")
        print("2. Exit")

        while True:
            choice = input("Enter your choice: ")
            if choice in ["1", "2"]:
                return choice
            print("Invalid choice. Try again.")

    def display_endgame_menu(self):
        print("\nGame Over!")
        print("1. Restart Game")
        print("2. Exit")

        while True:
            choice = input("Enter your choice: ")
            if choice in ["1", "2"]:
                return choice
            print("Invalid choice. Try again.")


class Board:
    def __init__(self):
        self.board = [" "] * 9

    def display_board(self):
        print()

        for i in range(3):
            row = []

            for j in range(3):
                index = i * 3 + j

                if self.board[index] == " ":
                    row.append(str(index + 1))
                else:
                    row.append(self.board[index])

            print(" | ".join(row))

            if i < 2:
                print("---------")

        print()

    def is_valid_move(self, choice):
        index = choice - 1
        return 0 <= index < 9 and self.board[index] == " "

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def reset_board(self):
        self.board = [" "] * 9


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()

        if choice == "2":
            self.exit_game()
            return

        self.setup_players()

        while True:
            self.play_game()

            choice = self.menu.display_endgame_menu()

            if choice == "1":
                self.restart_game()
            else:
                self.exit_game()
                break

    def setup_players(self):
        for number, player in enumerate(self.players, start=1):
            print(f"\nPlayer {number}")

            player.choose_name()

            while True:
                player.choose_symbol()

                if (
                    number == 2
                    and player.symbol == self.players[0].symbol
                ):
                    print("Symbol already taken.")
                else:
                    break

            print(f"{player.name} will play with '{player.symbol}'")

    def play_game(self):
        while True:
            self.play_turn()

            if self.check_win():
                winner = self.players[self.current_player_index]

                self.board.display_board()
                print(f"🎉 {winner.name} wins!")
                break

            if self.check_draw():
                self.board.display_board()
                print("It's a draw!")
                break

            self.switch_player()

    def play_turn(self):
        current_player = self.players[self.current_player_index]

        self.board.display_board()

        print(
            f"{current_player.name} ({current_player.symbol}) - next Turn"
        )

        while True:
            try:
                move = int(input("Enter your move (1-9): "))

                if not (1 <= move <= 9):
                    print("Move must be between 1 and 9.")
                    continue

                if self.board.update_board(
                    move,
                    current_player.symbol
                ):
                    break

                print("Cell already occupied.")

            except ValueError:
                print("Please enter a valid number.")

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_win(self):
        combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in combinations:
            a, b, c = combo

            if (
                self.board.board[a] ==
                self.board.board[b] ==
                self.board.board[c] != " "
            ):
                return True

        return False

    def check_draw(self):
        return " " not in self.board.board

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0

    def exit_game(self):
        print("Thank you for playing!")


if __name__ == "__main__":
    game = Game()
    game.start_game()