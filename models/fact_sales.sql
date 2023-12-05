{{
    config(
        materialized='table'
    )
}}
--Joining fact table with dimension tables 
WITH fact_cte AS (
    SELECT 
        d.sale_price,
        dp.property_id,
        dl.location_id,
        dd.sale_date_int AS sale_date_id
    FROM staging_table d
    JOIN dim_property dp 
        ON d.property_id = dp.prop_id  AND 
        d.address = dp.address 
    JOIN dim_location dl 
        ON d.borough = dl.borough AND
        d.neighborhood = dl.neighborhood AND
        d.zip_code = dl.zip_code
    JOIN dim_date dd 
        ON TO_DATE(d.sale_date, 'YYYY-MM-DD') = dd.sale_date_iso
) 

SELECT 
    ROW_NUMBER () OVER () AS sale_id, -- Creating surrogate key for fact_sales
    *
FROM fact_cte    
