# Homework-1

## Business Problem 
Mei Real Estate Analytics is a data-driven firm seeking to empower real estate professionals. Operating in the dynamic real estate landscape of New York City, our mission is to provide our clients, including investors, developers, and financial institutions, with the tools and information needed to make strategic decisions and thrive in the competitive market. 

### Purpose: Optimizing Investment Strategy for Real Estate Portfolios
Requirements: 
1. Ensure the accuracy and reliability of the NYC Annualized Property Sales dataset
2. Build a scalable data pipeline capable of handling large datasets to accommodate future market data and growth
3. Develop an intuitive and user-friendly Tableau dashboard that allows real estate professionals to easily interpret and derive insights from the presented visualizations.

Missing Requirements:
1. As noted early, ensuring the reliability and accuracy of the system is paramount. While the importance of testing is recognized, the exact testing scenarios, benchmarks, and standards to be employed are not explicitly outlined.

## Business Impact
### Risks: 
* *Data Accuracy and Reliability*: Inaccuracies in the dataset may lead to flawed investment decisions. Implementing thorough data validation processes mitigates this risk.
* *Regulatory Compliance*: Failure to adhere to real estate regulations may result in legal consequences. Regular compliance checks and updates are vital to managing this risk.

### Costs: 
* *Initial setup*: Establishing the data pipeline, developing the Tableau dashboard, and implementing real-time updates entail initial costs.
* *Maintenance*: Ongoing maintenance, data pipeline updates, and server costs contribute to the total cost of ownership.

### Benefits: 
* *Informed Decision-Making*: Real estate professionals gain valuable insights for strategic decision-making, leading to optimized investment strategies.
* *Maximized Returns*: Targeting high-value boroughs and strategic timing of investments can result in maximized returns for investors.

## Business Persona:
* Users: Real estate Analysts, Property Investors, Executives and Decision-Makers
* Actors: Data Engineer, Dashboard Developer, Compliance Officer, IT Support 

## Data Sources
[NYC Citywide Annualized Calendar Sales Update](https://data.cityofnewyork.us/City-Government/NYC-Citywide-Annualized-Calendar-Sales-Update/w2pb-icbu): This data set was obtained from NYC Open Data using a web API. 

The API endpoint used for data extraction is https://data.cityofnewyork.us/resource/w2pb-icbu.json.

To access Python script used to source the data, click [here.](Scripts/extraction.py)


## Data Dictionary
You can access the source's data dictionary in the [Annualized_Calendar_Sales_Update_Data_Dictionary.xlsx](Annualized_Calendar_Sales_Update_Data_Dictionary.xlsx) repo file. To download the Excel file directly, click [here.](https://github.com/jmeiws/Homework-1/raw/main/Annualized_Calendar_Sales_Update_Data_Dictionary.xlsx)

#### Dataset Size:
The raw dataset contains approximately 600,000 records. 

#### Strengths:
1. Rich information: The dataset provides a wealth of information about property sales, including sale prices, locations, tax classes, and transaction dates.
2. Historical trends: The dataset's historical nature allows for the analysis of trends over time, enabling users to identify patterns and make informed predictions.

#### Weaknesses: 
1. Data Quality: There exists a decent number of incomplete/inaccurate data entries that may compromise the overall quality of analyses and predictions. This calls for format standardizaiton in columns such as Borough, Address, etc. 
   * Example: Columns like residential_units containing 0, empty values, etc
2. Missing Descriptions: Some column names are hard to comprehend, as they do not appear in the source's provided data dictionary.

## Data Tools: 
* Data dictionary: Excel
* Dimensional Modeling: DbSchema
* Data Storage and Data Warehouse: AWS (Amazon S3 , Amazon Redshift Serverless)
* Data Extraction: Python
* Data Cleaning/Transformations: dbt labs
  * For automating our data pipeline, dbt labs allows for scheduled runs for orchestrated data transformations.
* Serving Data: Tableau 

## Methods
### ETL Diagram: 
![ELT diagram](https://github.com/jmeiws/Homework-1/assets/145298707/3d18c684-79a6-43fb-912b-6289c7f5ae62)

#### 1. Extract
 Python is used to connect to the API and retrieve the data, which is then organized and stored in a Pandas DataFrame. Minimal cleaning was performed. Refer to [extraction.py](Scripts/extraction.py) for more details on the extraction process and the type of data cleaning performed. 
#### 2. Load 
After setting up an AWS account, the extracted data is loaded into an Amazon S3 bucket, as a good practice to avoid frequent API calls to the source system. I chose S3 as my cloud storage because of its integration with Amazon Redshift Serverless. This serves as a staging area for the data before being loaded into the target data warehouse. Refer to [load_s3.py](Scripts/load_s3.py) for the configuration of my S3 bucket. Keys taken out for privacy concerns. 

At this point, an Amazon Redshift cluster has been created. Refer to [AWS documentation](https://docs.aws.amazon.com/redshift/latest/gsg/new-user-serverless.html) for configuration steps. 

Now, the benefits of AWS functionality shines: In Redshift's query editor, their UI allow users to seamlessly load files from an S3 bucket into a table. 

![image](https://github.com/jmeiws/Homework-1/assets/145298707/7e7944ad-6593-4a6b-9635-f1b19fd1e9af)

Here, I load the relatively raw data from my S3 bucket into a table named 'staging_table'. At this point, I am not worried about inconsistencies within the data such as data types -- these will be taken care of in the transformation part of the ELT. 

#### 3. Transform
Before transforming the data, I built a [dimensional model](hw_dimensional_model.PNG) according to my specific business context. Displayed below is a star schema designed using DbSchema: 
![image](https://github.com/jmeiws/Homework-1/assets/145298707/f565e112-6d4a-490d-a2b1-eda66acc9566)

*Note*: Although I did not use the sql script generated by DbSchema to create the data warehouse, please refer to [create_data_warehouse.sql](Scripts/create_data_warehouse.sql) to learn more about the overall schema and table structure of my Redshift cluster. 

In the final transformation step, the raw data that has been loaded into your data warehouse is finally ready for modeling using dbt Labs. After configuring and connecting dbt Labs to my Redshift cluster and GitHub, dbt models are created to transform the raw data in 'staging_table' into dimension tables and fact tables. The models are transformed according to specific business rules: surrogate keys are created for each table, fields are casted correctly, date formats are unified, NULL/duplicate values are dealt with, and so on. Refer to the directory [models](models) for data transformations performed on dbt Labs. 

*Observations*: The dataset contained many columns with rows that did not make logical sense. For example, some records had a field 'year_built' as 0 or 'land_square_feet' as 0. As a data engineer in charge of this pipeline, I want to note the importance of documenting and reporting these to relevant actors of the system. Instead of removing these rows, it is crucial that I report my observations to a relevant field expert and gather more information before proceeding. 

After executing the dbt models: 
- Dimension Models:
   1. dim_location
   2. dim_property
   3. dim_date
- Fact Tables:
   1. fact_sales
## Serving Data using Tableau
With the dimension and fact tables created in the Data Warehouse, I connected Tableau Desktop to my Amazon Redshift database, and created data visualizations for my dashboard.

### Dashboard
![image](https://github.com/jmeiws/Homework-1/assets/145298707/c0177dc0-7b0a-4356-a9b3-9de385afcdec)

1. Average Sale Price per Borough (Bar Chart):

* Objective: This visualization aims to provide a comparative analysis of average sale prices across different boroughs in New York City.
* Insights: Investors and analysts can easily identify boroughs with higher average sale prices, aiding in strategic decision-making for property investments.

2. Heatmap of Sale Counts by Zip Code:

* Objective: The heatmap visually represents the distribution of property sales across various zip codes in NYC.
* Insights: Users can quickly identify hotspots with higher sale counts, helping investors pinpoint areas of high market activity and potential investment opportunities.

3. Number of Sales Over Time (Line Chart):

* Objective: The line chart illustrates the trend in the number of property sales over a specific time period.
* Insights: This dynamic visualization allows users to observe trends and patterns, helping in understanding market fluctuations and making informed decisions based on temporal variations.

4. Distribution of Sales by Tax Class (Pie Chart):

* Objective: The pie chart visualizes the proportion of property sales categorized by different tax classes.
* Insights: Investors and developers gain insights into the distribution of tax classes, aiding in understanding the tax implications of various property transactions.

#### Insights Example  
The Tableau dashboard contains a date slicer, allowing users to interactively filter data based on specific time periods. Ultimately, this enables a more granular analysis of property sales trends and patterns over time. 

Taking a closer look at the dashboard above, there is an interesting trend in 2021 and 2022 More particularly, if we examine the line chart "Number of Sales Over Time", there is a steep decrease in the number of property sales in 2022 in comparison to 2021. Let's use the filter "Sale Date Iso" on the right side to examine the charts for calendar years 2021 and 2022.

##### 2021
![image](https://github.com/jmeiws/Homework-1/assets/145298707/baaa4d32-4de6-47ef-b114-8940836c5bdd)

The 2021 average property sale price in Manhattan was $2,940,140. The number of property sales at the end of 2021 approximated around 8000. 
##### 2022
![image](https://github.com/jmeiws/Homework-1/assets/145298707/b1d25e90-a87a-4089-a6e0-ce0b3b9e1484)

The 2022 average property sale price in Manhattan was $3,527,204. Now, the number of property sales at the end of 2022 ended with a downward trend at around 7000.   

In examining this trend, our data calls for a deeper investigation between 2020 - 2022 in external factors  that may cause these behaviors. Whether this may be due to a potential market shift, economic conditions, or even location-specific trends, utilizing this dashboard gives an opportunity to our users and points them towards deeper insights to be extracted in the real estate market. 

## Lessons Learned
1. Although I was taught the importance of gathering business requirements before starting to build a data pipeline in theory, it was still surprising to recognize first-hand how truly crucial it is to do so. It made a lot of the conceptual and logical modeling processes much more efficient and comprehendable.
2. It was my first time connecting databases, for example, between tools like Python, dbt, and Tableau. I learned the concept of IP address whitelisting and the necessity of proper configuration in order to successfully connect these platforms. 
3. Amazon Redshift does not enforce unique, primary-key, and foreign-key constraints. I spent a bit of time trying to enforce primary keys upon tables created from dbt, but I learned that it is not as much important as the dimension and fact tables created from dbt, in theory, should implicitly enforce them if coded properly. 



