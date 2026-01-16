import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

# Page Config
st.set_page_config(page_title="Süper Lig 360", layout="wide")

# Database Connection
# Using SQLAlchemy for easier pandas integration
# Running locally, so we connect to localhost. 
# If running inside docker, we would use 'db'. 
# Since we run 'streamlit run' from host, we use localhost.
DB_URL = "postgresql+psycopg2://postgres:password@localhost:5432/superlig360"

@st.cache_data
def load_data(query):
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# Title
st.title("⚽ Süper Lig 360 - Analytics Dashboard")

# Sidebar
st.sidebar.header("Filter Options")
st.sidebar.info("Connected to local PostgreSQL (Docker)")

# Tabs
tab1, tab2, tab3 = st.tabs(["🏆 Puan Durumu", "🥅 Gol Krallığı", "💰 Piyasa Değerleri"])

with tab1:
    st.header("Süper Lig Puan Durumu")
    query_standings = "SELECT * FROM analytics_superlig_marts.fct_league_standings ORDER BY points DESC, goal_diff DESC"
    df_standings = load_data(query_standings)
    
    if not df_standings.empty:
        # Styling the dataframe
        st.dataframe(
            df_standings.style.highlight_max(axis=0, subset=['points', 'goals_for']),
            use_container_width=True
        )
    else:
        st.warning("No data found in fct_league_standings.")

with tab2:
    st.header("Gol Krallığı")
    # Join with dim_players to get names
    query_scorers = """
        SELECT dp.player_name, dt.team_name, SUM(fps.goals) as total_goals
        FROM fact_player_stats fps
        JOIN dim_players dp ON fps.player_id = dp.player_id
        JOIN fact_matches fm ON fps.match_id = fm.match_id
        JOIN dim_teams dt ON (fm.home_team_id = dt.team_id OR fm.away_team_id = dt.team_id)
        -- Note: Team join logic strictly needs player-team link which we missed in schema (player assigned to team).
        -- For this demo, we can just show player name and goals.
        GROUP BY dp.player_name, dt.team_name
        ORDER BY total_goals DESC
        LIMIT 10
    """
    # Simplified query since we don't have current_team_id in dim_players in this simplified schema
    query_scorers_simple = """
        SELECT dp.player_name, SUM(fps.goals) as total_goals
        FROM fact_player_stats fps
        JOIN dim_players dp ON fps.player_id = dp.player_id
        GROUP BY dp.player_name
        ORDER BY total_goals DESC
    """
    
    df_scorers = load_data(query_scorers_simple)
    
    if not df_scorers.empty:
        st.bar_chart(df_scorers.set_index('player_name'))
        st.table(df_scorers)

with tab3:
    st.header("Oyuncu Piyasa Değerleri")
    query_values = """
        SELECT dp.player_name, fmv.valuation_date, fmv.market_value
        FROM fact_market_values fmv
        JOIN dim_players dp ON fmv.player_id = dp.player_id
        ORDER BY fmv.valuation_date
    """
    df_values = load_data(query_values)
    
    if not df_values.empty:
        st.line_chart(df_values, x='valuation_date', y='market_value', color='player_name')
    else:
        st.info("No market value data available.")

st.markdown("---")
st.caption("Süper Lig 360 | Data Engineering Project Demo")
