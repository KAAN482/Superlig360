-- Dimension Tables

CREATE TABLE IF NOT EXISTS dim_teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    stadium VARCHAR(100),
    foundation_year INT
);

CREATE TABLE IF NOT EXISTS dim_players (
    player_id SERIAL PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
    position VARCHAR(50)
);

-- Fact Tables

CREATE TABLE IF NOT EXISTS fact_matches (
    match_id SERIAL PRIMARY KEY,
    match_date TIMESTAMP NOT NULL,
    home_team_id INT REFERENCES dim_teams(team_id),
    away_team_id INT REFERENCES dim_teams(team_id),
    home_score INT,
    away_score INT
);

CREATE TABLE IF NOT EXISTS fact_player_stats (
    stat_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES fact_matches(match_id),
    player_id INT REFERENCES dim_players(player_id),
    goals INT DEFAULT 0,
    assists INT DEFAULT 0,
    minutes_played INT,
    yellow_cards INT DEFAULT 0,
    red_cards INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fact_market_values (
    valuation_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES dim_players(player_id),
    valuation_date DATE NOT NULL,
    market_value DECIMAL(15, 2) -- Value in Euros
);
