import psycopg2
import random
from datetime import datetime
import os
import time

# Database connection parameters (Environment Variables)
DB_HOST = os.getenv('DB_HOST', 'db') # 'db' for docker network, 'localhost' for local testing
DB_NAME = os.getenv('DB_NAME', 'superlig360')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password')

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def get_teams(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT team_id FROM dim_teams")
        return [row[0] for row in cur.fetchall()]

def generate_match_data(conn):
    teams = get_teams(conn)
    if len(teams) < 2:
        print("Not enough teams to generate a match.")
        return

    home_team = random.choice(teams)
    away_team = random.choice([t for t in teams if t != home_team])
    
    home_score = random.randint(0, 5)
    away_score = random.randint(0, 5)
    match_date = datetime.now()

    with conn.cursor() as cur:
        # Insert Match
        cur.execute("""
            INSERT INTO fact_matches (match_date, home_team_id, away_team_id, home_score, away_score)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING match_id
        """, (match_date, home_team, away_team, home_score, away_score))
        
        match_id = cur.fetchone()[0]
        print(f"Generated Match {match_id}: Team {home_team} vs Team {away_team} ({home_score}-{away_score})")

        conn.commit()

def main():
    print("Starting Mock Scraper...")
    try:
        conn = connect_db()
        print("Connected to Database.")
        generate_match_data(conn)
        conn.close()
        print("Scraper finished successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
