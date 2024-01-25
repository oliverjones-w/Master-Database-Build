import pandas as pd
from sqlalchemy import create_engine

def upload_data_to_db(file_path, table_name, schema_name, column_mappings=None, columns_to_insert=None):
    # Connection details
    servername = 'localhost\\SQLEXPRESS01'
    databasename = 'master'
    driver = 'ODBC Driver 17 for SQL Server'

    # Construct the connection string
    connection_string = f"mssql+pyodbc://{servername}/{databasename}?driver={driver}&Trusted_Connection=yes&Encrypt=yes&TrustServerCertificate=yes"

    # Create the engine
    engine = create_engine(connection_string)

    # Load the Excel file
    df = pd.read_excel(file_path)

    # Process column mappings if provided
    if column_mappings:
        for descriptive_col_name, mapping_info in column_mappings.items():
            if 'query' in mapping_info:
                # Fetch the mapping from the database
                mapping_df = pd.read_sql(mapping_info['query'], con=engine)
                
                # Convert the DataFrame to a dictionary for easy lookup
                mapping_dict = dict(zip(mapping_df.iloc[:, 0], mapping_df.iloc[:, 1]))
                
                # Generate a new column name for the ID column if not provided
                id_col_name = mapping_info.get('id_col_name', descriptive_col_name + 'ID')
                
                # Replace the descriptive names with the corresponding IDs using the mapping
                df[id_col_name] = df[descriptive_col_name].map(mapping_dict)
                
                # Check if there are any unmatched names that didn't get an ID
                unmatched_names = df[df[id_col_name].isnull()]
                if not unmatched_names.empty:
                    print(f"Warning: These entries didn't match any {descriptive_col_name}:", unmatched_names[descriptive_col_name])
            else:
                df[mapping_info] = df[descriptive_col_name]
                
    # Print the DataFrame after mapping for review
    print(df.head())

    # Select only the columns to insert into the database
    if columns_to_insert:
        df = df[columns_to_insert]

    # Print the DataFrame that will be inserted for final review
    print("DataFrame to be inserted:")
    print(df.head())

    # Insert data into the database table
    df.to_sql(table_name, con=engine, schema=schema_name, if_exists='append', index=False)
    print(f"Data uploaded successfully to {schema_name}.{table_name}")

# Usage:
file_path = r"C:\Users\BSA-OliverJ'22\OneDrive\Desktop\OneDrive\MS SQL Server\SQL_master_import_book.xlsx"
table_name = 'Firm'
schema_name = 'dbo'
column_mappings = {
    'FirmTypeName': {
        'query': 'SELECT FirmTypeName, FirmTypeID FROM FirmType',
        'id_col_name': 'FirmTypeID'
    }
}

columns_to_insert = ['FirmName', 'FirmTypeID']  # Specify only the columns you want to insert into the database

upload_data_to_db(file_path, table_name, schema_name, column_mappings, columns_to_insert)

