from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='Frontend')


# Function to connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="CPSC408!",
        database="SIEM_DB"
    )

# Function to execute SQL queries
def execute_query(query, fetch_all=False):
    db = None  # Initialize db
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(query)
        
        if fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        return result

    except Exception as e:
        if db and db.is_connected():  # Check if db is not None before using it
            db.rollback()
        print(f"Error: {str(e)}")
        return None

    finally:
        if db and db.is_connected():  # Check if db is not None before using it
            cursor.close()
            db.close()


# Route for the home page
@app.route('/')
def index():
    content = "Hello, World!"
    return render_template('index.html', content=content)

# Example route for displaying records
@app.route('/display_records', methods=['POST'])
def display_records():
    table_name = request.form['table_name']
    query = f"SELECT * FROM {table_name};"
    records = execute_query(query, fetch_all=True)
    return render_template('display_records.html', table_name=table_name, records=records)

# You need to add similar routes for other functionalities (e.g., query_with_filters, create_new_record, delete_records, etc.)

if __name__ == "__main__":
    app.run(debug=True)


