#You must have tkinter installed to run this file.

import tkinter as tk
import numpy as np

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
        self.training_cycles = 1

        # Add a label and entry for training cycles
        self.training_label = tk.Label(self.window, text="Training Cycles:")
        self.training_label.grid(row=0, column=3)
        self.training_entry = tk.Entry(self.window)
        self.training_entry.grid(row=1, column=3)
        
        # Add a button to start training
        self.train_button = tk.Button(self.window, text="Train", command=self.train_bot)
        self.train_button.grid(row=2, column=3)
        
        # Add some commentary for the user
        self.message_label = tk.Label(self.window, text="Initializing Game")
        self.message_label.grid(row=4, columnspan=3)
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
        if self.game.board[index] == ' ':  # Check if the cell is empty
            result = self.game.make_move(index)
            self.buttons[row][column].config(text=self.game.current_player)
            self.game.current_player = 'O' if self.game.current_player == 'X' else 'X'
            
            if result:
                self.message_label.config(text=result)
                self.game.reset_board()
                self.reset_buttons()
                return  # Exit the method if the game is already won
            
            bot_index = self.bot_move()
            if bot_index is not None:
                result = self.game.make_move(bot_index)
                row, column = divmod(bot_index, 3)
                self.buttons[row][column].config(text=self.game.current_player)
                self.game.current_player = 'O' if self.game.current_player == 'X' else 'X'
            
            if result:
                self.message_label.config(text=result)
                self.game.reset_board()
                self.reset_buttons()
            else:
                self.message_label.config(text="")


    # use trained bot to make a move
    def bot_move(self):
        state = board_to_state(self.game.board)
        empty_cells = [i for i, cell in enumerate(self.game.board) if cell == ' ']
        
        if empty_cells:
            q_values = [q_table[state, i] if i in empty_cells else -np.inf for i in range(9)]
            bot_action = np.argmax(q_values)
            return bot_action
        return None

    def reset_buttons(self):
        """Reset the button texts for a new game."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ')

    def train_bot(self):
        self.training_cycles = int(self.training_entry.get())
        if self.training_cycles > 1000000:
            self.training_cycles = 1000000  # Cap at 100,000
        # Train the bot
        for i in range(1, self.training_cycles):
            game = TicTacToeGame()
            state = board_to_state(game.board)
            self.message_label.config(text=f"Training Game: {i}")
            self.window.update_idletasks()  # Force update of the Tkinter window
            done = False
            while not done:
                print("Training Game:", i + 1)
                action = np.argmax(q_table[state])
                result = game.make_move(action)
                reward = 1 if result else -.1
                done = bool(result)
                next_state = board_to_state(game.board)
                old_value = q_table[state, action]
                next_max = np.max(q_table[next_state])
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                q_table[state, action] = new_value
                state = next_state

                if not done:
                    empty_cells = [i for i, cell in enumerate(game.board) if cell == ' ']
                    if empty_cells:
                        opponent_action = np.random.choice(empty_cells)
                        game.make_move(opponent_action)
                        done = bool(game.check_winner())
            game.reset_board()

# Initialize Q-table and hyperparameters
q_table = np.zeros([3**9, 9])
alpha, gamma = 0.1, 0.6

# Function to convert board to state
def board_to_state(board):
    mapping = {' ': '0', 'X': '1', 'O': '2'}
    return int(''.join([mapping[cell] for cell in board]), 3)


if __name__ == '__main__':
    game = TicTacToeGame()
    TicTacToeUI(game)
