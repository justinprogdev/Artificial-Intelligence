# You must have tkinter installed to run this file.

import tkinter as tk
import numpy as np


class TicTacToeGame:
    def __init__(self):
        """Initialize the game board and current player."""
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def make_move(self, index):
        """
        Make a move on the board at the given index.
        Returns 1 for win, .5 for draw, and 0 for no result.
        """
        # Validate that the square isn't occupied
        if self.board[index] == " ":
            self.board[index] = self.current_player
            if self.check_winner():
                return 1
            elif " " not in self.board:
                return 0.5
        return 0

    def check_winner(self):
        """Check if there's a winner on the board."""
        for line in [
            # Rows
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            # Columns
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            # Diagonals
            [0, 4, 8],
            [2, 4, 6],
        ]:
            # Just compares each value in the line to see if it's same
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != " ":
                return True
        return False

    def reset_board(self):
        """Reset the game board and current player for a new game."""
        self.board = [" " for _ in range(9)]
        self.current_player = "X"


class TicTacToeUI:
    def __init__(self, game):
        """Initialize the UI with a game instance."""
        self.game = game
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.buttons = []
        self.training_cycles = 100

        # Add a label and text box for entering training cycles
        self.training_label = tk.Label(self.window, text="Training Cycles:")
        self.training_label.grid(row=0, column=3)
        self.training_entry = tk.Entry(self.window)
        self.training_entry.grid(row=1, column=3)

        # Add a button to start training on user input
        self.train_button = tk.Button(self.window, text="Train", command=self.train_bot)
        self.train_button.grid(row=2, column=3)

        # Add some commentary for the user to know it's working
        self.message_label = tk.Label(self.window, text="Initializing Game")
        self.message_label.grid(row=4, columnspan=3)

        # Start
        self.initialize_board()
        self.window.mainloop()

    def initialize_board(self):
        """Build the board with three rows of three buttons."""
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(
                    self.window,
                    text=" ",
                    width=10,
                    height=3,
                    command=lambda i=i, j=j: self.click(i, j),
                )
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click(self, row, column):
        """Handle button click events on squares."""
        index = 3 * row + column
        if self.game.board[index] == " ":  # Check if the cell is empty
            result = self.game.make_move(index)
            self.buttons[row][column].config(text=self.game.current_player)
            self.game.current_player = "O" if self.game.current_player == "X" else "X"

            if result == 1:  # Check if the game is won
                self.message_label.config(text="You win!")
                self.game.reset_board()
                self.reset_buttons()
                return  # Exit the method if the game is already won

            if result == 0.5:  # Check if the game is drawn
                self.message_label.config(text="Draw")
                self.game.reset_board()
                self.reset_buttons()
            else:
                self.message_label.config(text="")

            bot_index = self.bot_move()
            if bot_index is not None:
                result = self.game.make_move(bot_index)
                row, column = divmod(bot_index, 3)
                self.buttons[row][column].config(text=self.game.current_player)
                self.game.current_player = (
                    "O" if self.game.current_player == "X" else "X"
                )

            if result == 1:  # Check if the game is won
                self.message_label.config(text="Altic Wins!")
                self.game.reset_board()
                self.reset_buttons()
                return  # Exit the method if the game is already won

            if result == 0.5:  # Check if the game is drawn
                self.message_label.config(text="Draw")
                self.game.reset_board()
                self.reset_buttons()
            else:
                self.message_label.config(text="")

    # use trained bot to make a move
    def bot_move(self):
        state = board_to_state(self.game.board)
        empty_cells = [i for i, cell in enumerate(self.game.board) if cell == " "]

        if empty_cells:
            q_values = [
                q_table[state, i] if i in empty_cells else -np.inf for i in range(9)
            ]
            bot_action = np.argmax(q_values)
            return bot_action
        return None

    def reset_buttons(self):
        """Reset the button texts for a new game."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")

    def train_bot(self):
        self.training_cycles = int(self.training_entry.get())
        if self.training_cycles > 1000000:
            self.training_cycles = 1000000  # Cap at 100,000

        for i in range(1, self.training_cycles):
            state = board_to_state(self.game.board)
            self.message_label.config(text=f"Training Game: {i}")
            self.window.update_idletasks()
            done = False
            while not done:
                empty_cells = [
                    i for i, cell in enumerate(self.game.board) if cell == " "
                ]
                if np.random.rand() < 0.6:
                    action = np.random.choice(empty_cells)
                else:
                    action = np.argmax(q_table[state])

                result = self.game.make_move(action)
                reward = 0
                if result == 1 or result == 0.5:
                    reward = 1
                    done = True
                else:
                    reward = 0.25

                next_state = board_to_state(self.game.board)
                old_value = q_table[state, action]
                next_max = np.max(q_table[next_state])

                if not done:
                    empty_cells = [
                        i for i, cell in enumerate(self.game.board) if cell == " "
                    ]
                    if empty_cells:
                        opponent_action = np.argmax(q_table[state])
                        opponent_result = self.game.make_move(opponent_action)
                        if opponent_result == 1:
                            reward = -0.1
                            done = True

                # Update state-action value
                new_value = (1 - alpha) * old_value + alpha * (
                    reward + gamma * next_max
                )
                q_table[state, action] = new_value
                state = next_state

            self.game.reset_board()


# Initialize Q-table and hyperparameters
q_table = np.zeros([3**9, 9])
alpha, gamma = 0.1, 0.6


# Function to convert board to state
def board_to_state(board):
    mapping = {" ": "0", "X": "1", "O": "2"}
    return int("".join([mapping[cell] for cell in board]), 3)


if __name__ == "__main__":
    game = TicTacToeGame()
    TicTacToeUI(game)
