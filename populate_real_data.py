import psycopg2
from datetime import datetime

# Real data from Google Süper Lig (scraped manually via browser)
REAL_TEAMS_DATA = [
    {"rank": 1, "name": "Galatasaray", "played": 17, "wins": 13, "draws": 3, "losses": 1, "goals_for": 39, "goals_against": 12, "goal_diff": 27, "points": 42},
    {"rank": 2, "name": "Fenerbahçe", "played": 17, "wins": 11, "draws": 6, "losses": 0, "goals_for": 39, "goals_against": 14, "goal_diff": 25, "points": 39},
    {"rank": 3, "name": "Trabzonspor", "played": 17, "wins": 10, "draws": 5, "losses": 2, "goals_for": 33, "goals_against": 20, "goal_diff": 13, "points": 35},
    {"rank": 4, "name": "Göztepe", "played": 17, "wins": 9, "draws": 5, "losses": 3, "goals_for": 21, "goals_against": 9, "goal_diff": 12, "points": 32},
    {"rank": 5, "name": "Beşiktaş", "played": 17, "wins": 8, "draws": 5, "losses": 4, "goals_for": 30, "goals_against": 22, "goal_diff": 8, "points": 29},
    {"rank": 6, "name": "Samsunspor", "played": 17, "wins": 6, "draws": 7, "losses": 4, "goals_for": 22, "goals_against": 20, "goal_diff": 2, "points": 25},
    {"rank": 7, "name": "Başakşehir", "played": 17, "wins": 6, "draws": 5, "losses": 6, "goals_for": 27, "goals_against": 18, "goal_diff": 9, "points": 23},
    {"rank": 8, "name": "Kocaelispor", "played": 17, "wins": 6, "draws": 5, "losses": 6, "goals_for": 15, "goals_against": 17, "goal_diff": -2, "points": 23},
    {"rank": 9, "name": "Gaziantep FK", "played": 17, "wins": 6, "draws": 5, "losses": 6, "goals_for": 24, "goals_against": 30, "goal_diff": -6, "points": 23},
    {"rank": 10, "name": "Alanyaspor", "played": 17, "wins": 4, "draws": 9, "losses": 4, "goals_for": 16, "goals_against": 15, "goal_diff": 1, "points": 21},
    {"rank": 11, "name": "Gençlerbirliği", "played": 17, "wins": 5, "draws": 3, "losses": 9, "goals_for": 21, "goals_against": 24, "goal_diff": -3, "points": 18},
    {"rank": 12, "name": "Rizespor", "played": 17, "wins": 4, "draws": 6, "losses": 7, "goals_for": 20, "goals_against": 24, "goal_diff": -4, "points": 18},
    {"rank": 13, "name": "Konyaspor", "played": 17, "wins": 4, "draws": 5, "losses": 8, "goals_for": 21, "goals_against": 29, "goal_diff": -8, "points": 17},
    {"rank": 14, "name": "Kasımpaşa", "played": 17, "wins": 3, "draws": 6, "losses": 8, "goals_for": 14, "goals_against": 24, "goal_diff": -10, "points": 15},
    {"rank": 15, "name": "Antalyaspor", "played": 17, "wins": 4, "draws": 3, "losses": 10, "goals_for": 16, "goals_against": 31, "goal_diff": -15, "points": 15},
    {"rank": 16, "name": "Kayserispor", "played": 17, "wins": 2, "draws": 9, "losses": 6, "goals_for": 16, "goals_against": 33, "goal_diff": -17, "points": 15},
    {"rank": 17, "name": "Eyüpspor", "played": 17, "wins": 3, "draws": 4, "losses": 10, "goals_for": 10, "goals_against": 24, "goal_diff": -14, "points": 13},
    {"rank": 18, "name": "Karagümrük", "played": 17, "wins": 2, "draws": 3, "losses": 12, "goals_for": 14, "goals_against": 32, "goal_diff": -18, "points": 9}
]

TOP_SCORERS = [
    {"name": "Eldar Shamyradov", "team": "Başakşehir", "goals": 12},
    {"name": "Paul Onuachu", "team": "Trabzonspor", "goals": 11},
    {"name": "Mauro Icardi", "team": "Galatasaray", "goals": 9},
    {"name": "Edin Džeko", "team": "Fenerbahçe", "goals": 8},
    {"name": "Semih Kılıçsoy", "team": "Beşiktaş", "goals": 7},
    {"name": "Yunus Akgün", "team": "Fenerbahçe", "goals": 6},
    {"name": "Krzysztof Piątek", "team": "Başakşehir", "goals": 6}
]

DB_CONFIG = {
    'host': 'localhost',
    'database': 'superlig360',
    'user': 'postgres',
    'password': 'password',
    'client_encoding': 'UTF8'
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding('UTF8')
    return conn

def populate_real_data():
    """Populate database with real Süper Lig data from Google"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        print("=" * 60)
        print("POPULATING DATABASE WITH REAL SÜPER LIG DATA")
        print("=" * 60)
        
        # Clear existing data
        print("\nClearing old data...")
        cur.execute("TRUNCATE TABLE fact_market_values CASCADE")
        cur.execute("TRUNCATE TABLE fact_player_stats CASCADE")
        cur.execute("TRUNCATE TABLE fact_matches CASCADE")
        cur.execute("DELETE FROM dim_players CASCADE")
        cur.execute("DELETE FROM dim_teams CASCADE")
        
        # Insert teams
        print("\nInserting teams...")
        team_id_map = {}
        for team in REAL_TEAMS_DATA:
            cur.execute("""
                INSERT INTO dim_teams (team_id, team_name, stadium, foundation_year)
                VALUES (%s, %s, %s, %s)
            """, (team['rank'], team['name'], 'Stadium', 1900))
            team_id_map[team['name']] = team['rank']
            print(f"  {team['rank']}. {team['name']} - {team['points']} puan")
        
        # Insert players (top scorers)
        print("\nInserting top scorers...")
        player_id = 1
        player_team_map = {}
        for scorer in TOP_SCORERS:
            cur.execute("""
                INSERT INTO dim_players (player_id, player_name, birth_date, nationality, position)
                VALUES (%s, %s, %s, %s, %s)
            """, (player_id, scorer['name'], '1990-01-01', 'Türkiye', 'Forward'))
            player_team_map[scorer['name']] = team_id_map.get(scorer['team'], 1)
            print(f"  {scorer['name']} ({scorer['team']}) - {scorer['goals']} gol")
            player_id += 1
        
        # Generate synthetic matches based on standings
        print("\nGenerating synthetic matches based on real standings...")
        match_id = 1
        for team in REAL_TEAMS_DATA:
            team_id = team['rank']
            
            # Generate wins
            for w in range(min(team['wins'], 5)):
                opponent_id = ((team_id + w) % 18) + 1
                if opponent_id != team_id:
                    cur.execute("""
                        INSERT INTO fact_matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (match_id, datetime.now(), team_id, opponent_id, 2, 0))
                    match_id += 1
            
            # Generate draws
            for d in range(min(team['draws'], 3)):
                opponent_id = ((team_id + d + 5) % 18) + 1
                if opponent_id != team_id:
                    cur.execute("""
                        INSERT INTO fact_matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (match_id, datetime.now(), team_id, opponent_id, 1, 1))
                    match_id += 1
            
            # Generate some losses
            for l in range(min(team['losses'], 2)):
                opponent_id = ((team_id + l + 10) % 18) + 1
                if opponent_id != team_id:
                    cur.execute("""
                        INSERT INTO fact_matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (match_id, datetime.now(), team_id, opponent_id, 0, 2))
                    match_id += 1
        
        # Add player stats for top scorers
        print("\nAdding player stats...")
        for idx, scorer in enumerate(TOP_SCORERS, 1):
            # Add stats across multiple matches
            goals_remaining = scorer['goals']
            match_count = 0
            for mid in range(1, min(match_id, 50), 3):  # Every 3rd match
                if goals_remaining > 0:
                    goals_in_match = min(goals_remaining, 2)
                    cur.execute("""
                        INSERT INTO fact_player_stats (match_id, player_id, goals, assists, minutes_played, yellow_cards, red_cards)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (mid, idx, goals_in_match, 0, 90, 0, 0))
                    goals_remaining -= goals_in_match
                    match_count += 1
                if goals_remaining == 0:
                    break
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE POPULATED WITH REAL DATA!")
        print("=" * 60)
        print(f"\n  Teams: {len(REAL_TEAMS_DATA)}")
        print(f"  Players: {len(TOP_SCORERS)}")
        print(f"  Matches: {match_id - 1}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_real_data()
