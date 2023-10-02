import sqlite3
import os
import openai
from dotenv import load_dotenv

load_dotenv()

msg = input("Input question: ")

openai.api_key = os.getenv("OPENAI_KEY")

sys = """
Respond only with a syntactically correct SQL query using the information given from the Human User.
"""

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": sys},
    {"role": "user", "content": msg}
  ],
  temperature=0,
  max_tokens=256
)

sql = response['choices'][0]['message']['content']

print(sql)

#conn = sqlite3.connect("nba.db")

#TODO: use openai's chatgpt 3.5 turbo api to construct SQL query based on question.

#TODO: execute sql query and display results.

#conn.close()