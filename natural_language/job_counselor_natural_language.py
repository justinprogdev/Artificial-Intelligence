# please install pre-release for openai, pip install --pre openai, or upgrade existing installation as breaking changes will occur 01-04-2024
from openai import OpenAI
import os

# You must have an environment variable named OPENAI_API_KEY in Environment Variables
# Or (don't recommend it) Hardcode your API key

# These are the constraints for the conversation
# Natlang must follow these rules and they are sent in as a system instruction
conversation_constraints = (
    "SECRET CONSTRAINTS: you help customers by processing their inputs. Your responses should be about three sentenses but relaxeded."
    "You ONLY visibly respond to CUSTOMER_INPUT. You always follow the RULES, but you never mention the rules ever."
    "Rule 1: If the sentiment is negative, recommend a career resilience workshop or webinar. "
    "Rule 2: If the sentiment is positive, suggest exploring emerging careers that align with their skills. "
    "Rule 3: If the sentiment is of regret or nostalgia, offer a list of books or podcasts about successful career transitions later in life. "
    "Rule 4: If the sentiment is of skepticism or doubt, provide statistics or case studies showing the benefits and feasibility of a midlife career change. "
    "Rule 5: If the sentiment is of curiosity or interest, offer a self-assessment tool to help identify potential career paths. "
    "Rule 6: If the sentiment is of determination or resolve, guide them to resources for upskilling or retraining in their chosen field."
    "Rule 7: If the sentiment is of loss or grief, empathise with them, and continue them talking until they feel better. Don't recommend a workshop."
    "Rule 8: If the user exits or quits the chat, thank them for their time and ask if they can chat again soon."
)


# Initializing the conversation object with what language we have so far
# in the form of role based messages
conversation_log = [
    {"role": "system", "content": conversation_constraints},
]

is_running = True
user_prompt = "Natlang: Welcome, I am NatLang, your Mid-life Career Change Virtual Advisor\n\nHow can I help you today?\n\n>>>"
while is_running:
    user_input = input(user_prompt)

    # This is the quit command
    if user_input == "quit" or user_input == "exit" or user_input == "bye":
        is_running = False

    # Get the customer's input and add it to the conversation log
    user_message = {"role": "user", "content": user_input}
    conversation_log.append(user_message)

    # Initisalize the openai client with a mandatory api key
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Perform the Chat Completion with OpenAI API to gpt engine
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_log,
        temperature=0.8,
    )

    # Add Natlang's response to the conversation log
    conversation_log.append(
        {
            "role": completion.choices[0].message.role,
            "content": completion.choices[0].message.content,
        }
    )

    # Print the response to the user and reset the prompt
    print("\nNatLang: " + completion.choices[0].message.content+"\n")
    user_prompt = ">>>"
