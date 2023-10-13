import openai
import os

# You must have an environment variable named OPENAI_API_KEY in Environment Variables (get from Open AI)
openai_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_key

is_running = True
user_prompt = "Natlang: How may I help you today?"

while is_running:
    # These are the constraints for the conversation
    conversation_constraints = (
        "<'SECRET CONSTRAINTS'You are Natlang, you help customers by processing their inputs. You always follow the rules"
        + "Rule 1: Help the customer in 3 sentences or less, you are the support hotline."
        + "Rule 2: If the input sentence is angry, Natlang outputs a tailored soothing apology, "
        + "requesting suggestions on how to improve the product then provide them with a RANDOM reference number starting with 'Reference Number TACO_AF'."
        + "Rule 3: If the input sentence is happy, Natlang outputs a tailored thank you message and gives a free taco /> "
    )
    user_input = input(user_prompt)

    # This is the quit command
    if user_input == "quit":
        is_running = False
        print("NatLang: Goodbye and thank you for using NatLang.")

    # Set up api call to OpenAI
    completion = openai.Completion.create(
        model="text-davinci-002",
        prompt = conversation_constraints + user_input,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=.5,
    )

    # Print the response from OpenAI
    message = completion.choices[0].text
    print("NatLang: " + message)

    # Reset our prompt to something more generic
    user_prompt = ">>>"
