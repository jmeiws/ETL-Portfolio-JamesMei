import pandas as pd
from sodapy import Socrata

# Connect to web API
client = Socrata("data.cityofnewyork.us", None)
results = client.get("w2pb-icbu")
results_df = pd.DataFrame.from_records(results)
pd.set_option('display.max_columns', None)

# Display dataframe
print("Display DataFrame:")
print(results_df)