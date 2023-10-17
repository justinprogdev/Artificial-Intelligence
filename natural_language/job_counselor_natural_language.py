# Required Dependency Installations:
# install textblob: pip install textblob
# install textblob corpa: python -m textblob.download_corpora
# install openai: pip install openai
# install pandas: pip install pandas

import os
import pandas as pd
from openai import OpenAI
from textblob import TextBlob
from job_data import JobData as job_data  # from file job_data.py
from nlp_rules import NlpRules as rules  # from file nlp_rules.py
from conversation_log import ConversationLog  # from file conversation_log.py

def analyze_sentiment(text):
    """Returns sentiment and intensity of sentiment if any"""
    if not text:
        return "Sentiment: N/A Intensity: N/A"
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    intensity = abs(blob.sentiment.subjectivity)
    return f"Sentiment: {sentiment} Intensity: {intensity}"

def main():
    # Conversation constraints and vocational rules
    conversation_rules = (
        rules().get_conversation_constraints() + " " + rules().get_vocational_rules()
    )

    # Initializing conversation log object
    conversation_log = ConversationLog({"role": "system", "content": conversation_rules})

    # Get job data for processing phrases with keywords/tokens
    df = pd.DataFrame(
        job_data().get_job_data(),
        columns=[
            "Job Title",
            "Education Requirement",
            "Job Description",
            "Available Salary Range",
        ],
    )

    is_running = True
    user_prompt = ("NatLang: Welcome, I am NatLang, your Mid-life Career Change Virtual Advisor\n\n"
                   "How can I help you today?\n\n>>>")

    while is_running:
        user_input = input(user_prompt)

        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            is_running = False

        sentiment_output = analyze_sentiment(user_input)

        user_message = {
            "role": "user",
            "content": user_input + " | Sentiment: " + sentiment_output,
        }
        conversation_log.add_message(user_message)

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_log.get_log(),
            temperature=0.8,
        )

        ai_message = {
            "role": completion.choices[0].message.role,
            "content": completion.choices[0].message.content,
        }
        conversation_log.add_message(ai_message)

        print(f"\nNatLang: {completion.choices[0].message.content}\n")
        user_prompt = ">>>"

if __name__ == "__main__":
    main()
