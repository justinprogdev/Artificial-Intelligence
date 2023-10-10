class Altic:
    """This is a design model for Altic, A Q-Learning based agent."""
    def __init__(self, tictactoe_spaces):
        self.training_data_list = []
        self.exploration_rate = 1
        self.exploitation_rate = 0.01
        self.actions = tictactoe_spaces.length

    def train(self, iterations=1000):
        """Train Altic for a given number of iterations."""
        #Todo: Implement the training loop
        # For each iteration of training:
        # perform exploration, exploitation and actions based on inputs
        # including, make a move based on exploration or exploitation
        # record and add state, state prime (reult of action), and reward to training_data_list


class TrainingData:
    """Example training data for an agent."""
    def __init__(self, state, action, reward, next_state, goal_state):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state
        self.goal_state = goal_state