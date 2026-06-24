class Player :
    def __init__(self):
        self.name= ""
        self.symbol= ""
    def choose_name(self):
        while True :
            name = input("enter your name (letters only) : ")
            if name.isalpha():
                self.name = name 
                break
            print("invalid name try again")
    def choose_symbol(self):
        while True :
            symbol = input(f"{self.name} ,enter your symbol (one character only) : ")
            if len(symbol) ==1 and symbol.isalpha():
                self.symbol = symbol.upper()
                break
            print("invalid symbol try again")
class Menu :
    def display_main_menu(self):
        print("welcome to X-O game :")
        print("1* start game ")
        print("2* exit ")
        choice = input("enter your choice 1 or 2 :")
        while choice not in ["1","2"]:
            print("invalid choice try again ")
            choice = input("enter your choice 1 or 2 :")
        return choice
    def display_endgame_menu(self):
        menu_text = """
        game over !
        1* restsrt game 
        2* exit
        """
        choice = input(menu_text + "enter your choice 1 or 2 :")
        while choice not in ["1","2"]:
            print("invalid choice try again ")
            choice = input(menu_text + " enter your choice 1 or 2 :")
        return choice
class Board :
    def __init__(self):
        # represent the board as a flat list of 9 cells (indexes 0-8)
        self.board = [" "] * 9

    def display_board(self):
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            # show cell numbers for empty cells to help the player
            disp = [cell if cell != " " else str(i*3 + j + 1) for j, cell in enumerate(row)]
            print(" | ".join(disp))
            if i != 2:
                print("---------")

    def update_board(self, choice, symbol):
        index = choice - 1
        if self.is_valid_move(choice):
            self.board[index] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        index = choice - 1
        return 0 <= index < 9 and self.board[index] == " "

    def reset_board(self):
        self.board = [" "] * 9
class Game :
    def __init__(self):
        self.players = [Player() , Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0
    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1" :
            self.setup_players()
            self.play_game()
        else :
            self.exit_game()

    def setup_players(self) :
        for number , player  in  enumerate(self.players, start=1) :
            print(f"player {number} , enter your details :")
            player.choose_name()
            # prevent both players using the same symbol
            while True:
                player.choose_symbol()
                other_index = 1 - (number - 1)
                other = self.players[other_index]
                if other.symbol and player.symbol == other.symbol:
                    print(f"Symbol '{player.symbol}' is already taken. Choose another.")
                    # reset and retry
                    player.symbol = ""
                    continue
                break
            print(f"{player.name} , your symbol is {player.symbol}")
            print("*"*20)
    def play_game(self) :
        while True :
            self.play_turn()
            if self.check_win() or self.check_draw() :
                choice = self.menu.display_endgame_menu()
                if choice == "1" :
                    self.restart_game()
                else :
                    self.exit_game()
                    break

    def restart_game(self) :
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def check_win(self) :
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # columns
            [0,4,8], [2,4,6]            # diagonals 
        ]
        for combo in win_combinations:
            if (self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]] != " "):
                return True
        return False   
    def check_draw(self) :
        return (not self.check_win()) and all(cell != " " for cell in self.board.board)

    def play_turn(self) :  
        current_player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{current_player.name} ({current_player.symbol}), it's your turn !")
        while True:
            try:
                cell_choice = int(input("enter your move (1-9) :"))
                if not (1 <= cell_choice <= 9):
                    print("move out of range, enter a number 1-9")
                    continue
                if not self.board.is_valid_move(cell_choice):
                    print(f"cell {cell_choice} is already occupied")
                    continue
                if self.board.update_board(cell_choice, current_player.symbol):
                    break
                else:
                    print("couldn't place symbol, try again")
            except ValueError:
                print("please enter a valid number between 1 and 9")
        self.switch_player()
    def switch_player(self) :
        self.current_player_index = 1 - self.current_player_index
    def exit_game(self) :
        print("thank you for playing !")


if __name__ == "__main__":
    game = Game()
    game.start_game()






    