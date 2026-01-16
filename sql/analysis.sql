-- 1. Window Functions: Weekly Top Scorers Ranking (Dummy Example)
-- Assuming we have data, this calculates rank based on goals in a specific match/week
SELECT 
    p.player_name,
    m.match_date,
    fps.goals,
    RANK() OVER (PARTITION BY DATE_TRUNC('week', m.match_date) ORDER BY fps.goals DESC) as goal_rank
FROM 
    fact_player_stats fps
JOIN 
    dim_players p ON fps.player_id = p.player_id
JOIN 
    fact_matches m ON fps.match_id = m.match_id
WHERE 
    fps.goals > 0;


-- 2. Window Functions: Team Form (LAG)
-- Checks previous match result concept (simplistic win/loss logic needed in data)
SELECT 
    t.team_name,
    m.match_date,
    CASE 
        WHEN m.home_team_id = t.team_id AND m.home_score > m.away_score THEN 'W'
        WHEN m.home_team_id = t.team_id AND m.home_score < m.away_score THEN 'L'
        WHEN m.away_team_id = t.team_id AND m.away_score > m.home_score THEN 'W'
        WHEN m.away_team_id = t.team_id AND m.away_score < m.home_score THEN 'L'
        ELSE 'D'
    END as result,
    LAG(
        CASE 
            WHEN m.home_team_id = t.team_id AND m.home_score > m.away_score THEN 'W'
            WHEN m.home_team_id = t.team_id AND m.home_score < m.away_score THEN 'L'
            WHEN m.away_team_id = t.team_id AND m.away_score > m.home_score THEN 'W'
            WHEN m.away_team_id = t.team_id AND m.away_score < m.home_score THEN 'L'
            ELSE 'D'
        END
    ) OVER (PARTITION BY t.team_id ORDER BY m.match_date) as prev_result
FROM 
    fact_matches m
JOIN 
    dim_teams t ON m.home_team_id = t.team_id OR m.away_team_id = t.team_id;


-- 3. CTE: League Standings
WITH match_points AS (
    SELECT 
        home_team_id as team_id,
        CASE 
            WHEN home_score > away_score THEN 3
            WHEN home_score = away_score THEN 1
            ELSE 0 
        END as points,
        home_score - away_score as goal_diff,
        CASE WHEN home_score > away_score THEN 1 ELSE 0 END as wins
    FROM fact_matches
    UNION ALL
    SELECT 
        away_team_id as team_id,
        CASE 
            WHEN away_score > home_score THEN 3
            WHEN away_score = home_score THEN 1
            ELSE 0 
        END as points,
        away_score - home_score as goal_diff,
        CASE WHEN away_score > home_score THEN 1 ELSE 0 END as wins
    FROM fact_matches
)
SELECT 
    t.team_name,
    SUM(mp.points) as total_points,
    SUM(mp.goal_diff) as total_average,
    SUM(mp.wins) as total_wins
FROM 
    match_points mp
JOIN 
    dim_teams t ON mp.team_id = t.team_id
GROUP BY 
    t.team_name
ORDER BY 
    total_points DESC, total_average DESC;
