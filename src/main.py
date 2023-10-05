import sqlite3
import os
import openai
from dotenv import load_dotenv
import sqlvalidator

load_dotenv()


openai.api_key = os.getenv("OPENAI_KEY")

sys = """
Respond only with a syntactically correct SQL query using the information given from the Human User.
The SQL queries should answer the question using data found in the following database schema.
NBA team names should be formatted like "full city name team name" example Los Angeles Clippers.
"""
with open('nba_db.txt', 'r') as f:
  file_contents = f.read() 
  
dbschema = file_contents

sys = dbschema + sys

msg = input("Input question: ")
try:
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": sys},
			{"role": "user", "content": msg}
		],
		temperature=0,
		max_tokens=256
	)
except Exception as e:
	print("Could not get response from OpenAI:",e)

sql = response['choices'][0]['message']['content']

print(sql)

sql_val = sqlvalidator.parse(sql)
if not sql_val.is_valid():
	raise ValueError("Invalid SQL syntax generated. Try rephrasing your question.")

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
		