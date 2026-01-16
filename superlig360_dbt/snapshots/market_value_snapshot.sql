
{% snapshot market_value_snapshot %}

{{
    config(
      target_database='superlig360',
      target_schema='snapshots',
      unique_key='valuation_id',

      strategy='timestamp',
      updated_at='valuation_date',
    )
}}

select * from {{ source('raw_superlig', 'fact_market_values') }}

{% endsnapshot %}
