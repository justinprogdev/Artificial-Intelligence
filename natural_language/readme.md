# Natlang Career Counselor bot

## Overview
I used the idea of a NatLang bot to create a mid-life career change advisor. 
The purpose is to provide a natural language conversation in the context of mid-life career change, guided by both vocational rules and conversational constraints.

## Prerequisites
- Python 3.x
- OpenAI Python package
- TextBlob Python package
- Pandas Python package
- An OpenAI API key

## Installation Steps

### Step 1: Install Python
If you don't have Python installed, download and install it from [python.org](https://www.python.org/).

### Step 2: Install Required Python Packages
Open your terminal and run the following commands to install the necessary Python packages:
'''
pip install openai textblob pandas 
pip install --pre openai 
'''

### Step 3: Download TextBlob Corpora
You'll need to download the corpora (data files) used by TextBlob. Run the following command:
'''
python -m textblob.download_corpora
'''

### Step 4: Set Up OpenAI API Key
You'll need an OpenAI API key to interact with the GPT-3 API. After obtaining the key from OpenAI, set it as an environment variable in your terminal:
'''
export OPENAI_API_KEY="your-api-key-here"
'''

### Step 5: Run the Program
Navigate to the directory containing your program files, and run the main script:
'''
python your_script_name.py
'''

### How it works
The script initiates a conversation with the user, asking how it can assist today. It then enters a loop, processing user input, analyzing the sentiment of the input, and responding accordingly based on predefined conversation rules and the job data provided. The conversation state is maintained in a log, preventing the bot from having "amnesia" during the interaction. This allows for a more coherent and contextually aware conversation flow