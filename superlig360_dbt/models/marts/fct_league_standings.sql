
WITH matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
),

home_stats AS (
    SELECT
        home_team_id as team_id,
        COUNT(*) as games_played,
        SUM(CASE WHEN match_result = 'HOME_WIN' THEN 3
                 WHEN match_result = 'DRAW' THEN 1
                 ELSE 0 END) as points,
        SUM(home_score) as goals_for,
        SUM(away_score) as goals_against,
        SUM(CASE WHEN match_result = 'HOME_WIN' THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN match_result = 'DRAW' THEN 1 ELSE 0 END) as draws,
        SUM(CASE WHEN match_result = 'AWAY_WIN' THEN 1 ELSE 0 END) as losses
    FROM matches
    GROUP BY home_team_id
),

away_stats AS (
    SELECT
        away_team_id as team_id,
        COUNT(*) as games_played,
        SUM(CASE WHEN match_result = 'AWAY_WIN' THEN 3
                 WHEN match_result = 'DRAW' THEN 1
                 ELSE 0 END) as points,
        SUM(away_score) as goals_for,
        SUM(home_score) as goals_against,
        SUM(CASE WHEN match_result = 'AWAY_WIN' THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN match_result = 'DRAW' THEN 1 ELSE 0 END) as draws,
        SUM(CASE WHEN match_result = 'HOME_WIN' THEN 1 ELSE 0 END) as losses
    FROM matches
    GROUP BY away_team_id
),

combined_stats AS (
    SELECT * FROM home_stats
    UNION ALL
    SELECT * FROM away_stats
),

teams AS (
    SELECT * FROM {{ source('raw_superlig', 'dim_teams') }}
)

SELECT
    t.team_name,
    SUM(cs.games_played) as played,
    SUM(cs.wins) as wins,
    SUM(cs.draws) as draws,
    SUM(cs.losses) as losses,
    SUM(cs.goals_for) as goals_for,
    SUM(cs.goals_against) as goals_against,
    SUM(cs.goals_for) - SUM(cs.goals_against) as goal_diff,
    SUM(cs.points) as points
FROM combined_stats cs
JOIN teams t ON cs.team_id = t.team_id
GROUP BY t.team_name
ORDER BY points DESC, goal_diff DESC
