import sqlite3
import openpyxl
import random

wb = openpyxl.load_workbook('NBA_Dataset.xlsx')

conn = sqlite3.connect("nba.db")
cur = conn.cursor()

#teams

ws = wb['teams']

teams = []
team_map = {}

for row in ws.iter_rows():
    row_vals = []
    for cell in row:
        row_vals.append(cell.value)
    team_map[row_vals[1]] = row_vals[0]
    teams.append(row_vals)
    
cur.execute("DELETE FROM team;")
cur.executemany("""
        INSERT INTO team (team_id, team_name)
        VALUES (?, ?);
    """, teams)

conn.commit()

#players

ws = wb['players']

players = []
player_map = {}

for row in ws.iter_rows():
    row_vals = []
    for cell in range(0, len(row)):
        if cell != 2:
            row_vals.append(row[cell].value)
        else:
            row_vals.append(team_map[row[cell].value])
    players.append(row_vals)
    player_map[row_vals[1]] = row_vals[0]

cur.execute("DELETE FROM player;")
cur.executemany("""
        INSERT INTO player (player_id, player_name, team_id, age, height, weight, college, birth_country, draft_year, draft_round)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, players)

conn.commit()

#contracts

ws = wb['contracts']

contracts = []
values = [100000, 240000, 1300000, 400000, 600000, 10000000]

for row in ws.iter_rows():
    row_vals = []
    if not row[0].value in player_map:
        continue

    for cell in range(0, len(row)):
        if cell == 0:
            row_vals.append(player_map[row[cell].value])
        elif cell == 1:
            row_vals.append(team_map[row[cell].value])
        else:
            year = str(row[cell].value).split('-')
            row_vals.append(year[0])
            if int(year[1]) >= 0 and int(year[1]) < 96:
                row_vals.append("20" + year[1])
            else:
                row_vals.append("19" + year[1])
    row_vals.append(random.choice(values))
    contracts.append(row_vals)

cur.execute("DELETE FROM contract;")
cur.executemany("""
        INSERT INTO contract (player_id, team_id, start_date, end_date, total_value)
        VALUES (?, ?, ?, ?, ?);
    """, contracts)

conn.commit()

#match

#sponsor

#owner

conn.close()
