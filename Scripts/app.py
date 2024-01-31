from flask import Flask, request, jsonify, render_template
import openai
import os
from sqlalchemy import create_engine, text
from flask_cors import CORS
import traceback
import re 

app = Flask(__name__)
CORS(app)

# Connection details
servername = 'localhost\\SQLEXPRESS01'
databasename = 'master'
driver = 'ODBC Driver 17 for SQL Server'

# Construct the connection string
connection_string = f"mssql+pyodbc://{servername}/{databasename}?driver={driver}&Trusted_Connection=yes&Encrypt=yes&TrustServerCertificate=yes"

# Create the engine
engine = create_engine(connection_string, echo=True)

@app.route('/')
def index():
    return render_template('template1.html')

@app.route('/generate-sql', methods=['POST'])
def generate_sql_query():
    try:
        # Get the user's GPT query from the request
        user_response = request.get_json()
        user_query = user_response.get('query', '')
        # Create the system message by including the text file content
        with open(r"C:\Users\BSA-OliverJ'22\Projects\Database Architecture\TxtFiles\TableSchema.txt", 'r') as file:
            file_content = file.read()
        system_message = f"The following dataset is the list of all valid tables and columns in a response_data structure:\n{file_content}"

        # Print the user query for debugging
        print(f"User Query: {user_query}")

        # Make an API request to GPT-3.5 Turbo using the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate GPT-3 model
            messages=[
                {"role": "system", "content": "You are a database query assistant, please return a SQL query wrapped with start marker: ""```sql"" and end marker ""```"" :"},
                {"role": "user", "content": user_query},
                {"role": "user", "content": system_message}
            ],
        )

        # Assuming the API response is stored in the 'response_text' variable
        response_text = response['choices'][0]['message']['content']

        # Find the start and end positions of the SQL query
        start_marker = "```sql"
        end_marker = "```"

        # Find the index of the start marker
        start_index = response_text.find(start_marker)

        if start_index != -1:
            # Find the index of the end marker, starting from the position after the start marker
            end_index = response_text.find(end_marker, start_index + len(start_marker))

            if end_index != -1:
                # Extract the SQL query between the markers
                sql_query = response_text[start_index + len(start_marker):end_index].strip()
            else:
                # Handle the case when the end marker is not found
                sql_query = "ERROR"  # Replace YourTableName with the actual table name
        else:
            # Handle the case when the start marker is not found
            sql_query = "ERROR"  # Replace YourTableName with the actual table name

        # Print the generated SQL query for debugging
        print(f"Generated SQL Query: {sql_query}")

        # Print the generated SQL query for debugging
        print(f"Generated SQL Query: {sql_query}")

        # You can now execute the SQL query on your SQL database

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            response_data = result.fetchall()

        for row in response_data:
            print(row)
        
        # Convert the SQL server response to a JSON response
        keys = result.keys()
        data_list = [dict(zip(keys, row)) for row in response_data]

        return jsonify({'response_data': data_list})

    except Exception as e:
        # Print the error message for debugging
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
