import psycopg2
from config import load_config

def connect():
    return psycopg2.connect(**load_config())

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        level_reached INTEGER,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def get_or_create_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s",(username,))
    row = cur.fetchone()

    if row:
        pid = row[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id",(username,))
        pid = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return pid

def save_score(username, score, level):
    pid = get_or_create_player(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO game_sessions(player_id, score, level_reached)
    VALUES (%s,%s,%s)
    """,(pid,score,level))

    conn.commit()
    cur.close()
    conn.close()

def get_top10():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT p.username, g.score
    FROM game_sessions g
    JOIN players p ON p.id = g.player_id
    ORDER BY g.score DESC
    LIMIT 10
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_best(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT MAX(score)
    FROM game_sessions g
    JOIN players p ON p.id = g.player_id
    WHERE p.username=%s
    """,(username,))

    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0