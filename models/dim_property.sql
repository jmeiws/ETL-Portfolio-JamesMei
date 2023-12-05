{{ config(materialized="table") }}

--Replacing empty values with NULL and changing appropriate data types
with
    property_cte as (
        select distinct
            cast(nullif(bin, '') as bigint) as bin, 
            address,
            nullif(apartment_number, ''),
            nullif(latitude, ''),
            nullif(longitude, ''),
            cast(nullif(bbl, '') as bigint) as bbl,
            building_class_category,
            tax_class_as_of_final_roll,
            building_class_as_of_final,
            cast(nullif(residential_units, '') as integer),
            cast(nullif(commercial_units, '') as integer),
            cast(nullif(total_units, '') as integer),
            cast(
                nullif(replace(land_square_feet, ',', ''), '') as integer
            ) as land_square_feet,
            cast(
                nullif(replace(gross_square_feet, ',', ''), '') as integer
            ) as gross_square_feet,
            cast(nullif(year_built, '') as integer),
            tax_class_at_time_of_sale,
            building_class_at_time_of,
            property_id as prop_id
        from staging_table
    )

select row_number() over () as property_id, * --creating surrogate key for dim_property
from property_cte


