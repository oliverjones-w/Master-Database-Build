

import pandas as pd
from sqlalchemy import create_engine

# Connection details
servername = 'localhost\\SQLEXPRESS01'  # Double backslash for escaping
databasename = 'master'
driver = 'ODBC Driver 17 for SQL Server'  # Make sure this matches the name of the ODBC driver installed on your machine

# Construct the connection string
connection_string = f"mssql+pyodbc://{servername}/{databasename}?driver={driver}&Trusted_Connection=yes&Encrypt=yes&TrustServerCertificate=yes"

# Create the engine
engine = create_engine(connection_string)

# Load the Excel file
file_path = r"C:\Users\BSA-OliverJ'22\OneDrive\Desktop\OneDrive\MS SQL Server\NYTradingRatesMapImportBook.xlsx"
df = pd.read_excel(file_path)

#Remove rows where 'FirmTypeName' is missing
df = df.dropna(subset=['FirmTypeName'])


# Get the list of tables in the current database
query = """
SELECT TABLE_SCHEMA, TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
"""
tables_df = pd.read_sql(query, con=engine)

# Display the list of tables
#print(tables_df)

# Print the first few rows to confirm it's loaded correctly
#print(df.head())
#print(df.columns)

#Fetch the mapping from the database
firm_type_df = pd.read_sql('SELECT FirmTypeName, FirmTypeID FROM FirmType', con=engine)

# Convert the DataFrame to a dictionary for easy lookup
firm_type_mapping = dict(zip(firm_type_df['FirmTypeName'], firm_type_df['FirmTypeID']))

# Replace the descriptive names with the corresponding IDs using the mapping
df['FirmTypeID'] = df['FirmTypeName'].map(firm_type_mapping)

# Check if there are any unmatched names that didn't get an ID
unmatched_names = df[df['FirmTypeID'].isnull()]
if not unmatched_names.empty:
    print("Warning: These names didn't match any FirmTypeID:", unmatched_names['FirmTypeName'])

if 'FirmTypeName' in df.columns:
    df = df.drop(columns=['FirmTypeName'])

df = df[['FirmName', 'FirmTypeID']]

print(df[['FirmName', 'FirmTypeID']])

df.to_sql('Firm', con=engine, schema='dbo', if_exists='append', index=False)



