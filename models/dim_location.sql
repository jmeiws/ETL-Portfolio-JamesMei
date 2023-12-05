{{
    config(
        materialized='table'
    )
}}
--Replacing empty values with NULL and changing appropriate data types
WITH location_cte AS (
    SELECT DISTINCT 
        borough,
        CAST(NULLIF(zip_code, '') AS INTEGER) AS zip_code,
        neighborhood
    FROM
        staging_table
)

SELECT 
    ROW_NUMBER () OVER() AS location_id, --Creating surrogate key for dim_location 
    borough,
    zip_code,
    neighborhood
FROM location_cte

