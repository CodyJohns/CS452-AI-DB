import sqlite3


conn = sqlite3.connect("nba.db")
cur = conn.cursor()
cur.execute ("DROP TABLE IF EXISTS player;")
cur.execute("""
    CREATE TABLE player (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        team_id INTEGER,
        age INTEGER,
        height REAL,
        weight REAL,
        college TEXT,
        birth_country TEXT,
        draft_year INTEGER,
        draft_round INTEGER,
        FOREIGN KEY(team_id) 
            REFERENCES team(team_id)
            ON DELETE SET NULL
    );
    """
)
cur.execute ("DROP TABLE IF EXISTS team;")
cur.execute("""
    CREATE TABLE team (
        team_id INTEGER PRIMARY KEY NOT NULL,
        team_name TEXT NOT NULL UNIQUE,
        city TEXT,
        state TEXT
    );
    """
)
cur.execute ("DROP TABLE IF EXISTS match;")
cur.execute("""
    CREATE TABLE match (
        team_id_1 INTEGER NOT NULL,
        team_id_2 INTEGER NOT NULL CHECK(team_id_2 != team_id_1),
        date TEXT NOT NULL,
        --my Google search said ties are not allowed in NBA, so we will assume there is always a winner
        winning_team INTEGER NOT NULL,
        PRIMARY KEY(team_id_1, team_id_2, date),
        FOREIGN KEY(team_id_1)
            REFERENCES team(team_id)
            ON DELETE CASCADE,
        FOREIGN KEY(team_id_2)
            REFERENCES team(team_id)
            ON DELETE CASCADE
    );
    """
)
cur.execute ("DROP TABLE IF EXISTS contract;")
cur.execute("""
    CREATE TABLE contract (
        contract_id INTEGER PRIMARY KEY,
        player_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        total_value REAL,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY(player_id)
            REFERENCES player(player_id)
            ON DELETE CASCADE,
        FOREIGN KEY(team_id)
            REFERENCES team(team_id)
            ON DELETE CASCADE
    );
    """
)
cur.execute ("DROP TABLE IF EXISTS sponsor;")
cur.execute("""
    CREATE TABLE sponsor (
        team_id INTEGER NOT NULL,
        sponsor_name TEXT NOT NULL,
        PRIMARY KEY(team_id, sponsor_name),
        FOREIGN KEY(team_id)
            REFERENCES team(team_id)
            ON DELETE CASCADE
    );
    """
)
cur.execute ("DROP TABLE IF EXISTS owner;")
cur.execute("""
    CREATE TABLE owner (
        team_id INTEGER NOT NULL,
        owner_name TEXT NOT NULL,
        PRIMARY KEY(team_id, owner_name),
        FOREIGN KEY(team_id)
            REFERENCES team(team_id)
            ON DELETE CASCADE
    );
    """
)
conn.commit()
conn.close()