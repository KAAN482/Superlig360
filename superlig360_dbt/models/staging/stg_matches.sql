
WITH source AS (
    SELECT * FROM {{ source('raw_superlig', 'fact_matches') }}
)

SELECT
    match_id,
    match_date,
    home_team_id,
    away_team_id,
    home_score,
    away_score,
    CASE
        WHEN home_score > away_score THEN 'HOME_WIN'
        WHEN away_score > home_score THEN 'AWAY_WIN'
        ELSE 'DRAW'
    END as match_result
FROM source
