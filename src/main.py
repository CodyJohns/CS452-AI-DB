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

try:
	conn = sqlite3.connect("nba.db")
	c = conn.cursor()
	c.execute(sql)
    
	results = c.fetchall()
    
	for result in results:
		print(result)
    
except sqlite3.Error as e:
  print("Error executing query", e)

finally:
  if conn:
    conn.close()
	