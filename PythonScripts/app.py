from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# Connection details
servername = 'localhost\\SQLEXPRESS01'
databasename = 'master'
driver = 'ODBC Driver 17 for SQL Server'

# Construct the connection string
connection_string = f"mssql+pyodbc://{servername}/{databasename}?driver={driver}&Trusted_Connection=yes&Encrypt=yes&TrustServerCertificate=yes"


# Create the engine
engine = create_engine(connection_string)

@app.route('/')
def index():
    return render_template('template1.html')

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM dbo.Profile")
            result = connection.execute(query)
            data = result.fetchall()
            keys = result.keys()
            data_list = [dict(zip(keys, row)) for row in data]
        return jsonify(data_list)
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to the console
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    

