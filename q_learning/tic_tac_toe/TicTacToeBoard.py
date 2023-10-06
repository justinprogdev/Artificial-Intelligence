'''Don't steal this for your homework.
- Justin McClain'''
import tkinter as tk

class TicTacToeGame:
    def __init__(self):
        """Initialize the game board and current player."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def make_move(self, index):
        """
        Make a move on the board at the given index.
        Returns a message if the game is won or drawn.
        """
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            if self.check_winner():
                return f'Player {self.current_player} wins!'
            elif ' ' not in self.board:
                return "It's a draw!"
        return None

    def check_winner(self):
        """Check if there's a winner on the board."""
        for line in [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                return True
        return False

    def reset_board(self):
        """Reset the game board and current player for a new game."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'


class TicTacToeUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')
        self.buttons = []
        
        # Add game mode selection
        self.game_mode = tk.StringVar(value="Human")
        tk.Radiobutton(self.window, text="Human", variable=self.game_mode, value="Human").grid(row=0, column=3)
        tk.Radiobutton(self.window, text="Bot", variable=self.game_mode, value="Bot").grid(row=1, column=3)
        
        self.initialize_board()
        self.window.mainloop()

    def initialize_board(self):
        """Build the board with three rows of three buttons."""
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.window, text=' ', width=10, height=3,
                                   command=lambda i=i, j=j: self.click(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click(self, row, column):
        """Handle button click events."""
        index = 3 * row + column
        result = self.game.make_move(index)
        self.buttons[row][column].config(text=self.game.current_player)
        self.game.current_player = 'O' if self.game.current_player == 'X' else 'X'
        
        if self.game_mode.get() == "Bot":
            bot_index = self.bot_move()
            if bot_index is not None:
                self.game.make_move(bot_index)
                row, column = divmod(bot_index, 3)
                self.buttons[row][column].config(text=self.game.current_player)
                self.game.current_player = 'O' if self.game.current_player == 'X' else 'X'
        
        if result:
            print(result)
            self.game.reset_board()
            self.reset_buttons()

    def bot_move(self):
        """Placeholder for bot logic (currently just control logic)."""
        for i, cell in enumerate(self.game.board):
            if cell == ' ':
                return i

    def reset_buttons(self):
        """Reset the button texts for a new game."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ')


if __name__ == '__main__':
    game = TicTacToeGame()
    TicTacToeUI(game)
