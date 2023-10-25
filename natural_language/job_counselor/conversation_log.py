class ConversationLog:
    """Class to manage the conversation log."""
    
    def __init__(self, initial_message: dict):
        """
        Initializes a new instance of the ConversationLog class.
        
        Args:
            initial_message (dict): The initial message to start the conversation log with.
        """
        self.log = [initial_message]
        
    def add_message(self, message: dict) -> None:
        """
        Adds a message to the conversation log.
        
        Args:
            message (dict): The message to add to the log.
        """
        self.log.append(message)
        
    def get_log(self) -> list:
        """
        Retrieves the current conversation log.
        
        Returns:
            list: The current conversation log.
        """
        return self.log
