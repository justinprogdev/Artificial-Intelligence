# You must have tkinter installed to run this file.
# command prompt, then Pip install tkinker 
import tkinter as tk
import numpy as np


class TicTacToeAgent:
    def __init__(self):
        # Set the state with a Q table representing all possible states 19,683 (I know, this is easiest)
        self.q_table = np.zeros([3**9, 9])

        # Set the learning rate
        self.alpha = 0.1

        # Set the discount factor
        self.gamma = 0.6

    def make_move(self, board):
        # Convert the board to state by mapping Empty string to "0", "X" to "1" and "O": "2"
        state = board_to_state(board)

        # Get all empty cells for possible moves
        empty_cells = [i for i, cell in enumerate(board) if cell == " "]

        if empty_cells:
            # List of Q values
            q_values = [
                # for each empty cell i, get Q State, Action for it
                self.q_table[state, i] if i in empty_cells else -np.inf
                for i in range(9)
            ]

            # Return the action with the highest Q value
            agent_action = np.argmax(q_values)
            return agent_action
        return None


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
    def __init__(self, game, agent):
        """Initialize the UI with a game instance."""
        self.game = game
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.buttons = []
        self.agent = agent
        self.training_cycles = 100

        # Add a label and text box for entering training cycles
        self.training_label = tk.Label(self.window, text="Training Cycles:")
        self.training_label.grid(row=0, column=3)
        self.training_entry = tk.Entry(self.window)
        self.training_entry.grid(row=1, column=3)

        # Add a button to start training on user input
        self.train_button = tk.Button(self.window, text="Train", command=lambda: self.train_agent(self.agent))
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
                    # Add click event handler for each button
                    command=lambda i=i, j=j: self.click(i, j),
                )
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click(self, row, column):
        """Handle button click events on squares from UI."""
        index = 3 * row + column

        # If Cell is empty, process move
        if self.game.board[index] == " ":
            result = self.game.make_move(index)
            self.buttons[row][column].config(text=self.game.current_player)

            # 1. Process Move for Human
            # Check if the game is won
            if result == 1:
                self.message_label.config(text="You win!")
                self.game.reset_board()
                self.reset_buttons()
                return  # Exit the method if the game is already won

            # Check if the game is draw
            if result == 0.5:
                self.message_label.config(text="Draw")
                self.game.reset_board()
                self.reset_buttons()
            else:
                self.message_label.config(text="")

            # switch to the next player
            self.game.current_player = "O" if self.game.current_player == "X" else "X"

            # 2. Make Move for Altic
            # The agent makes a move based on the board state
            agent_index = self.agent.make_move(self.game.board)

            if agent_index is not None:
                result = self.game.make_move(agent_index)
                row, column = divmod(
                    agent_index, 3
                )  # Convert index to row, column w division and Modulo
                self.buttons[row][column].config(
                    text=self.game.current_player
                )  # update button text w agent's letter
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

    def reset_buttons(self):
        """Reset the button texts for a new game."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")

    def train_agent(self, agent):
        """Train the agent for the given number of cycles based on user input.
        The agent will play against itself and learn from the results.
        It uses the Q-Learning algorithm, and implements Gym to do so."""

        # Training Cylcles from user input
        self.training_cycles = int(self.training_entry.get())

        # Cap at 1,000,000 cycles
        if self.training_cycles > 1000000:
            self.training_cycles = 1000000

        # Train the agent N times
        for i in range(1, self.training_cycles):
            # Convert the board to state
            state = board_to_state(self.game.board)

            # Provided a counter to the user, so they know it's still training
            self.message_label.config(
                text=f"Training Game: {(self.training_cycles - i) - 1}"
            )
            self.window.update_idletasks()

            done = False

            # Start a training game
            while not done:
                # Get all empty cells for possible moves
                empty_cells = [i for i, cell in enumerate(self.game.board) if cell == " "]

                # Run the alogorithm to choose between exploration and exploitation
                # If random number is less than 0.8, then explore, else exploit
                if np.random.rand() < 0.8:
                    action = np.random.choice(empty_cells)
                else:
                    # Get the highest Q value for the current state
                    action = np.argmax(agent.q_table[state])

                # Make a move based on the chosen action
                result = self.game.make_move(action)

                # initialize reward
                reward = 0

                # If game is won or drawn the game is done
                # and a proportion of the reward is given based on results
                if result == 1:
                    reward = 1
                    done = True

                elif result == 0.5:
                    reward = 1

                else:
                    reward = 0.1

                if not done:
                    empty_cells = [
                        i for i, cell in enumerate(self.game.board) if cell == " "
                    ]
                    if empty_cells:
                        opponent_action = np.argmax(agent.q_table[state])
                        opponent_result = self.game.make_move(opponent_action)
                        if opponent_result == 1 or opponent_result == 0.5:
                            reward = -0.2 # Punish the agent for losing
                            done = True

                # Update state-action value
                next_state = board_to_state(self.game.board)
                old_value = agent.q_table[state, action]
                next_max = np.max(agent.q_table[next_state])

                new_value = (1 - agent.alpha) * old_value + agent.alpha * (
                    reward + agent.gamma * next_max
                )
                agent.q_table[state, action] = new_value
                state = next_state

            self.game.reset_board()


# Function to convert board to state
def board_to_state(board):
    mapping = {" ": "0", "X": "1", "O": "2"}
    return int("".join([mapping[cell] for cell in board]), 3)


if __name__ == "__main__":
    game = TicTacToeGame()
    agent = TicTacToeAgent()
    TicTacToeUI(game, agent)
