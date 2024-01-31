import pandas as pd
from sqlalchemy import create_engine

def update_finra_ids_from_excel(excel_file_path):
    try:
        # Connection details
        servername = 'localhost\\SQLEXPRESS01'
        databasename = 'master'
        driver = 'ODBC Driver 17 for SQL Server'

        # Construct the connection string
        connection_string = f"mssql+pyodbc://{servername}/{databasename}?driver={driver}&Trusted_Connection=yes&Encrypt=yes&TrustServerCertificate=yes"

        # Create the engine
        engine = create_engine(connection_string)

        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path)

        # Iterate through the rows in the DataFrame
        for index, row in df.iterrows():
            profile_id = row['ProfileID']  # Replace 'ProfileID' with the actual column name in your Excel file
            new_finra_id = row['FinraID']  # Replace 'FinraID' with the actual column name in your Excel file

            # Prepare the SQL statement to update FinraID for the given ProfileID
            update_statement = f"UPDATE dbo.Profile SET FinraID = '{new_finra_id}' WHERE ProfileID = {profile_id}"

            # Execute the update statement
            with engine.connect() as connection:
                connection.execute(update_statement)

            print(f"FinraID updated successfully for ProfileID {profile_id} to {new_finra_id}.")

        print("All updates from Excel completed.")
    except Exception as e:
        print(f"An error occurred: {e}")  # Print the exception message

# Example usage:
excel_file_path = r"C:\Users\BSA-OliverJ'22\Projects\Database Architecture\ExcelWorkbooks\SQL_master_import_book.xlsx"  # Replace with the path to your Excel file
update_finra_ids_from_excel(excel_file_path)
