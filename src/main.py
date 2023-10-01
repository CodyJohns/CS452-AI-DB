import sqlite3

#TODO: get user input
val = input("Input question: ")

print("Your question: {}".format(val))

conn = sqlite3.connect("nba.db")

#TODO: use openai's chatgpt 3.5 turbo api to construct SQL query based on question.

#TODO: execute sql query and display results.

conn.close()