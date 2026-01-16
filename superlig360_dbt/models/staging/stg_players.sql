
WITH source AS (
    SELECT * FROM {{ source('raw_superlig', 'dim_players') }}
)

SELECT
    player_id,
    player_name,
    birth_date,
    nationality,
    position
FROM source
