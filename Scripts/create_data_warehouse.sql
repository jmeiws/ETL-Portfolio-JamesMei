CREATE TABLE dim_date ( 
	sale_date_int        integer  NOT NULL  ,
	sale_date_iso        date    ,
	"year"               integer    ,
	month_number         integer    ,
	day_number           integer    ,
	quarter              integer    ,
	CONSTRAINT pk_dim_property PRIMARY KEY ( sale_date_int )
 );

CREATE TABLE dim_location ( 
	location_id          integer  NOT NULL  ,
	borough              varchar(128)    ,
	zip_code             integer    ,
	neighborhood         varchar(128)    ,
	CONSTRAINT pk_dim_location PRIMARY KEY ( location_id )
 );

CREATE TABLE dim_property ( 
	property_id          integer  NOT NULL  ,
	bin                  bigint    ,
	apartment_number     varchar(128)    ,
	address              varchar(128)    ,
	latitude             decimal(11,8)    ,
	longitude            decimal(11,8)    ,
	bbl                  bigint    ,
	building_class_category varchar(128)    ,
	tax_class_as_of_final_roll varchar(128)    ,
	building_class_as_of_final_roll varchar(128)    ,
	residential_units    integer    ,
	commercial_units     integer    ,
	total_units          integer    ,
	land_square_feet     integer    ,
	gross_square_feet    integer    ,
	year_built           integer    ,
	tax_class_at_time_of_sale integer    ,
	building_class_at_time_of varchar(128)    ,
	CONSTRAINT pk_dim_property_0 PRIMARY KEY ( property_id )
 );

CREATE TABLE fact_sales ( 
	sale_id              integer  NOT NULL  ,
	sale_price           decimal(15,2)    ,
	property_id          integer  NOT NULL  ,
	location_id          integer  NOT NULL  ,
	sale_date_id         integer  NOT NULL  ,
	CONSTRAINT pk_fact_propertysales PRIMARY KEY ( sale_id, sale_date_id, property_id, location_id )
 );

ALTER TABLE fact_sales ADD CONSTRAINT fk_fact_sales_dim_date FOREIGN KEY ( sale_date_id ) REFERENCES dim_date( sale_date_int );

ALTER TABLE fact_sales ADD CONSTRAINT fk_fact_sales_dim_property FOREIGN KEY ( property_id ) REFERENCES dim_property( property_id );

ALTER TABLE fact_sales ADD CONSTRAINT fk_fact_sales_dim_location FOREIGN KEY ( location_id ) REFERENCES dim_location( location_id );
