-- Clear existing data
TRUNCATE TABLE fact_market_values CASCADE;
TRUNCATE TABLE fact_player_stats CASCADE;
TRUNCATE TABLE fact_matches CASCADE;
TRUNCATE TABLE dim_players CASCADE;
TRUNCATE TABLE dim_teams CASCADE;

-- Teams
INSERT INTO dim_teams (team_id, team_name, stadium, foundation_year) VALUES
(1, E'Galatasaray', 'RAMS Park', 1905),
(2, E'Fenerbahçe', E'Ülker Stadyumu', 1907),
(3, E'Beşiktaş', E'Tüpraş Stadyumu', 1903),
(4, 'Trabzonspor', 'Papara Park', 1967)
ON CONFLICT (team_id) DO UPDATE SET
    team_name = EXCLUDED.team_name,
    stadium = EXCLUDED.stadium,
    foundation_year = EXCLUDED.foundation_year;

-- Players
INSERT INTO dim_players (player_id, player_name, birth_date, nationality, position) VALUES
(1, 'Mauro Icardi', '1993-02-19', 'Argentina', 'Forward'),
(2, E'Edin Džeko', '1986-03-17', 'Bosnia', 'Forward'),
(3, E'Semih Kılıçsoy', '2005-08-15', E'Türkiye', 'Forward'),
(4, 'Fernando Muslera', '1986-06-16', 'Uruguay', 'Goalkeeper')
ON CONFLICT (player_id) DO UPDATE SET
    player_name = EXCLUDED.player_name,
    birth_date = EXCLUDED.birth_date,
    nationality = EXCLUDED.nationality,
    position = EXCLUDED.position;

-- Matches
INSERT INTO fact_matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score) VALUES
(1, '2023-08-11 20:00:00', 1, 2, 0, 0), -- GS vs FB Draw
(2, '2023-08-12 20:00:00', 3, 4, 2, 1), -- BJK vs TS (BJK Win)
(3, '2023-08-18 20:00:00', 2, 3, 1, 1); -- FB vs BJK Draw

-- Player Stats
INSERT INTO fact_player_stats (match_id, player_id, goals, assists, minutes_played, yellow_cards, red_cards) VALUES
(1, 1, 0, 0, 90, 0, 0), -- Icardi vs FB
(1, 2, 0, 0, 90, 1, 0), -- Dzeko vs GS
(2, 3, 1, 0, 75, 0, 0); -- Semih vs TS

-- Market Values (Initial)
INSERT INTO fact_market_values (valuation_id, player_id, valuation_date, market_value) VALUES
(1, 1, '2023-08-01', 20000000.00), -- Icardi
(2, 3, '2023-08-01', 500000.00);   -- Semih (Low initial)

-- Simulate a change in market value for Snapshot testing (Requires running snapshot twice typically, or we insert 'old' data now and 'new' data later.
-- For now, we insert one record per player.
-- To test snapshot properly, we would run snapshot, then INSERT new value, then run snapshot again.
-- Lets just insert initial values now.
