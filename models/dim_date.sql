
{{
    config(
        materialized='table'
    )
}}


WITH date_cte AS (
    SELECT DISTINCT 
        CAST(sale_date AS DATE) AS sale_date
    FROM
        staging_table
)

SELECT 
    CAST(TO_CHAR(sale_date, 'YYMMDD') AS INTEGER) AS sale_date_int,    --Transforming date column into integer as primary key 
    TO_DATE(sale_date, 'YYYY-MM-DD') AS sale_date_iso,    --Creating unified date format 'YYYY-MM-DD'
--Splitting the date into multiple units (Year, Month, Day, Quarter)
    EXTRACT(year FROM sale_date) AS year,
    EXTRACT(month FROM sale_date) AS month,
    EXTRACT(day FROM sale_date) AS day,
    EXTRACT(quarter FROM sale_date) AS quarter
FROM date_cte