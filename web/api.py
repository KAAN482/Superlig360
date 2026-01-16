from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

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

@app.route('/api/standings')
def get_standings():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT team_name, played, wins, draws, losses, 
               goals_for, goals_against, goal_diff, points
        FROM analytics_superlig_marts.fct_league_standings
        ORDER BY points DESC, goal_diff DESC
    """)
    standings = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(standings)

@app.route('/api/top-scorers')
def get_top_scorers():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT dp.player_name, SUM(fps.goals) as total_goals
        FROM fact_player_stats fps
        JOIN dim_players dp ON fps.player_id = dp.player_id
        WHERE fps.goals > 0
        GROUP BY dp.player_name
        ORDER BY total_goals DESC
        LIMIT 10
    """)
    scorers = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(scorers)

@app.route('/api/market-values')
def get_market_values():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT dp.player_name, fmv.valuation_date::text, fmv.market_value
        FROM fact_market_values fmv
        JOIN dim_players dp ON fmv.player_id = dp.player_id
        ORDER BY fmv.valuation_date
    """)
    values = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(values)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
