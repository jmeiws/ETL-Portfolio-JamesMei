import requests
import pandas as pd
import boto3
from io import StringIO

url = "https://data.cityofnewyork.us/resource/w2pb-icbu.json"

# Set the initial parameters
offset = 0
all_data = []

while True:
    # Set up the request parameters
    params = {"$offset": offset}

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Break the loop if no more results are returned
        if not data:
            break

        all_data.extend(data)
        offset += len(data)
    else:
        print(f"Error: {response.status_code}")
        break

# Convert the results to a Pandas DataFrame
nyc_df = pd.DataFrame.from_records(all_data)

# Data Exploration
print(nyc_df.info())
print(nyc_df.isnull().sum())


## Data Cleaning

# Remove duplicate rows based on all columns
nyc_df.drop_duplicates(inplace=True)

# Exclude unnecessary columns
columns_to_exclude = ['census_tract_2020', 'nta_code']
nyc_df = nyc_df.drop(columns=columns_to_exclude, errors='ignore')

print(nyc_df)
print("Column Names:", nyc_df.columns)

# Convert numeric values in 'borough' to string representations
nyc_df['borough'] = nyc_df['borough'].astype(str)

borough_mapping = {
    '1': 'Manhattan',
    '2': 'Bronx',
    '3': 'Brooklyn',
    '4': 'Queens',
    '5': 'Staten Island'
}

nyc_df['borough'] = nyc_df['borough'].replace(borough_mapping).str.upper()

print(nyc_df['borough'].unique())  # Check if 'borough' values are consistent

# COUNT NULL IN bin
null_bin_count = nyc_df['bin'].isnull().sum()

print(f"Number of null values in 'bin' column: {null_bin_count}")

df_bin = nyc_df.dropna(subset=['bin']).copy()  # Remove rows with empty 'bin' values

# Extract apartment number from address
df_bin['apartment_number'] = df_bin['apartment_number'].where(df_bin['apartment_number'].notnull(),
                                                              df_bin['address'].str.extract(r',\s*([^,]*)$',
                                                                                            expand=False))
df_bin['address'] = df_bin['address'].replace({r',\s*([^,]*)$': ''}, regex=True)

# Create a new column combining 'BBL' and 'APARTMENT NUMBER'
df_bin['property_id'] = df_bin['bin'].astype(str) + '_' + df_bin['apartment_number'].astype(str)

print(df_bin)

# Check specific BINs with several apartments
selected_rows = df_bin[df_bin['bin'].str.contains('3010590004')]
print(selected_rows)

# Check for duplicates in the new 'PROPERTY_ID' column
duplicates = df_bin[df_bin.duplicated('property_id', keep=False)]

# Display rows with duplicate 'property_id' and count occurrences
property_id_counts = duplicates['property_id'].value_counts()
print(property_id_counts)
print(duplicates[['bin', 'apartment_number', 'property_id']])



