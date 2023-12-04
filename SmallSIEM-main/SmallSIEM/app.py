from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='templates')


# Function to connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="CPSC408!",
        database="SIEM_DB"
    )
def get_all_tables():
    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'siem_db';")
        tables = [row['table_name'] for row in cursor.fetchall()]
        return tables
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def get_columns(table_name):
    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)

        # Fetch columns for the specified table
        cursor.execute(f"DESCRIBE {table_name};")
        columns = [row['Field'] for row in cursor.fetchall()]

        return columns

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to execute SQL queries
# Function to execute SQL queries
def execute_query(query, fetch_all=False):
    db = None
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(query)

        if fetch_all:
            # Fetch all records and get column names
            columns = [column[0] for column in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        else:
            # Fetch one record and get column names
            columns = [column[0] for column in cursor.description]
            record = dict(zip(columns, cursor.fetchone()))
            records = [record] if record else []

        return records

    except Exception as e:
        if db and db.is_connected():
            db.rollback()
        print(f"Error: {str(e)}")
        return []

    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()



# Route for the home page
@app.route('/')
def index():
    content = "Hello, World!"
    return render_template('index.html', content=content)

# Example route for displaying records
# Example route for displaying records

@app.route('/display_records', methods=['POST'])
def display_records():
    table_name = request.form['table_name']  # Update the key to match the form field name
    query = f"SELECT * FROM {table_name};"
    records = execute_query(query, fetch_all=True)
    return render_template('display_records.html', table_name=table_name, records=records)



# Example route for querying records with filters
# Route for querying records with filters
# Route for querying records with filters

@app.route('/query_with_filters', methods=['POST'])
def query_with_filters():
    
    try:
        print("Received a request to query records with filters.")

        # Check if the form data is being received correctly
        print("Form data:", request.form)

        table_name = request.form['table_name_filter']  # Update the key to match the form field name
        column = request.form['column']
        value = request.form['value']

        print(f"Received form data: table={table_name}, column={column}, value={value}")

        query = f"SELECT * FROM {table_name} WHERE {column} LIKE '{value}';"
        records = execute_query(query, fetch_all=True)

        print(f"Query executed successfully. Records: {records}")

        return render_template('query_with_filters.html', table_name=table_name, records=records)

    except KeyError as e:
        print(f"KeyError: {e}")
        return "Invalid form data. Please make sure you provide values for all fields."
    
# @app.route('/create_new_record', methods=['GET'])
# def create_new_record_form():
#     return render_template('create_new_record.html')

# @app.route('/create_new_record', methods=['POST'])
# def create_new_record():
#     try:
#         table_name = request.form['table']
#         # Fetch columns for the selected table
#         columns_query = f"SHOW COLUMNS FROM {table_name};"
#         columns = [column[0] for column in execute_query(columns_query, fetch_all=True)]

#         return render_template('create_new_record.html', table_name=table_name, columns=columns)

#     except KeyError:
#         return "Invalid form data. Please make sure you provide a table name."
    

def create_new_record(table_name, values):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        cursor.execute(query, values)
        
        db.commit()
        print("New record inserted successfully.")

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Route for creating a new record
@app.route('/create_new_record', methods=['POST', 'GET'])
def create_new_record_route():
    table_name = None
    create_new_record_success = False
    columns = []  # Initialize columns

    if request.method == 'POST':
        try:
            table_name = request.form['table_name']
            values = request.form.getlist('values[]')

            # Validate that the number of values matches the number of columns
            columns = get_columns(table_name)
            if len(values) == len(columns):
                # Create a new record
                create_new_record(table_name, values)
                create_new_record_success = True
            else:
                create_new_record_success = False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            create_new_record_success = False

    # If it's a GET request, fetch all tables for initial rendering
    elif request.method == 'GET':
        columns = []  # Empty columns list for initial rendering

    return render_template('create_new_record.html', table_name=table_name, columns=columns, create_new_record_success=create_new_record_success)




# You need to add similar routes for other functionalities (e.g., query_with_filters, create_new_record, delete_records, etc.)

if __name__ == "__main__":
    app.run(debug=True)

