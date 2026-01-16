import psycopg2

# Connect with explicit UTF-8
conn = psycopg2.connect(
    host='localhost',
    database='superlig360',
    user='postgres',
    password='password',
    client_encoding='UTF8'
)
conn.set_client_encoding('UTF8')

cur = conn.cursor()

# Clear and reinsert with proper UTF-8
print("Updating teams with UTF-8 encoding...")
cur.execute("TRUNCATE TABLE fact_market_values CASCADE")
cur.execute("TRUNCATE TABLE fact_player_stats CASCADE")
cur.execute("TRUNCATE TABLE fact_matches CASCADE")
cur.execute("DELETE FROM dim_players CASCADE")
cur.execute("DELETE FROM dim_teams CASCADE")

# Teams
teams_data = [
    (1, 'Galatasaray', 'RAMS Park', 1905),
    (2, 'Fenerbahçe', 'Ülker Stadyumu', 1907),
    (3, 'Beşiktaş', 'Tüpraş Stadyumu', 1903),
    (4, 'Trabzonspor', 'Papara Park', 1967)
]

for team in teams_data:
    cur.execute(
        "INSERT INTO dim_teams (team_id, team_name, stadium, foundation_year) VALUES (%s, %s, %s, %s)",
        team
    )

# Players
players_data = [
    (1, 'Mauro Icardi', '1993-02-19', 'Argentina', 'Forward'),
    (2, 'Edin Džeko', '1986-03-17', 'Bosnia', 'Forward'),
    (3, 'Semih Kılıçsoy', '2005-08-15', 'Türkiye', 'Forward'),
    (4, 'Fernando Muslera', '1986-06-16', 'Uruguay', 'Goalkeeper')
]

for player in players_data:
    cur.execute(
        "INSERT INTO dim_players (player_id, player_name, birth_date, nationality, position) VALUES (%s, %s, %s, %s, %s)",
        player
    )

# Matches
matches_data = [
    (1, '2023-08-11 20:00:00', 1, 2, 0, 0),
    (2, '2023-08-12 20:00:00', 3, 4, 2, 1),
    (3, '2023-08-18 20:00:00', 2, 3, 1, 1)
]

for match in matches_data:
    cur.execute(
        "INSERT INTO fact_matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score) VALUES (%s, %s, %s, %s, %s, %s)",
        match
    )

# Player Stats
stats_data = [
    (1, 1, 0, 0, 90, 0, 0),
    (1, 2, 0, 0, 90, 1, 0),
    (2, 3, 1, 0, 75, 0, 0)
]

for stat in stats_data:
    cur.execute(
        "INSERT INTO fact_player_stats (match_id, player_id, goals, assists, minutes_played, yellow_cards, red_cards) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        stat
    )

# Market Values
values_data = [
    (1, 1, '2023-08-01', 20000000.00),
    (2, 3, '2023-08-01', 500000.00)
]

for value in values_data:
    cur.execute(
        "INSERT INTO fact_market_values (valuation_id, player_id, valuation_date, market_value) VALUES (%s, %s, %s, %s)",
        value
    )

conn.commit()
cur.close()
conn.close()

print("✅ Data updated successfully with UTF-8 encoding")
print("Verifying...")

# Verify
conn = psycopg2.connect(
    host='localhost',
    database='superlig360',
    user='postgres',
    password='password',
    client_encoding='UTF8'
)
cur = conn.cursor()
cur.execute("SELECT team_name FROM dim_teams ORDER BY team_id")
teams = cur.fetchall()
print("\nTeams in database:")
for team in teams:
    print(f"  - {team[0]}")

cur.close()
conn.close()
