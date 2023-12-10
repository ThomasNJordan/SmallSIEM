from flask import Flask, render_template, request, jsonify, redirect, url_for  # <-- Add this line
from query import *

app = Flask(__name__, template_folder='templates')


@app.route('/get_tables', methods=['GET'])
def get_tables():
    tables = get_all_tables()  # Function to retrieve all tables from the database
    return jsonify(tables)

# Route for the main dashboard
@app.route('/')
def dashboard():
    content = "Hello, World!"
    return render_template('index.html', content=content)


# Function to get all tables from the database
def get_all_tables():
    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)

        query = "SHOW TABLES;"
        cursor.execute(query)

        # Print the raw result to identify the correct key
        raw_result = cursor.fetchall()
        print("Raw result:", raw_result)

        # Modify the key based on the actual structure of the result
        tables = [table['Tables_in_siem_db'] for table in raw_result]

        print("Tables:", tables)  # Add this line

        return tables

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()



@app.route('/')
def index():
    content = "Hello, World!"
    return render_template('index.html', content=content)

@app.route('/display_records', methods=['POST'])
def display_records_html():
    table_name = request.form['table_name']  # Get the table name from the form
    records = display_records(table_name)  # Get records using the function from query.py
    return render_template('display_records.html', table_name=table_name, records=records)

@app.route('/query_with_filters', methods=['POST'])
def query_with_filters_route():
    table_name = request.form['table_name']
    column = request.form['column']
    value = request.form['value']
    records = query_database_with_filters(table_name, column, value)
    return render_template('display_records.html', table_name=table_name, records=records)



@app.route('/create_new_record', methods=['POST', 'GET'])
def create_new_record_route():
    if request.method == 'GET':
        # Render form for adding new record
        return render_template('create_record_form.html')
    elif request.method == 'POST':
        try:
            table_name = request.form['table_name']
            # Print form data for debugging
            print(f"Received form data for table '{table_name}': {request.form}")

            # Retrieve values dynamically based on the number of columns
            values = [request.form[column] for column in request.form if column != 'table_name']
            create_new_record(table_name, values)  # Call function to create a new record
            return redirect(url_for('create_new_record_route'))  # Redirect back to the create form page

        except Exception as e:
            # Print the exception for debugging
            print(f"Exception: {e}")
            return "An error occurred while processing the form."


@app.route('/delete_records', methods=['POST'])
def delete_records_html():
    table_name = request.form['table_name']
    condition = request.form['condition']
    delete_records(table_name, condition)
    return redirect(url_for('display_records_html', table_name=table_name))

# Add route for updating records
@app.route('/update_records', methods=['POST'])
def update_records_html():
    table_name = request.form['table_name']
    column = request.form['column']
    value = request.form['value']
    condition = request.form['condition']
    update_records(table_name, column, value, condition)
    return redirect(url_for('display_records_html', table_name=table_name))

# Add route for creating a new record within a transaction
@app.route('/create_new_record_transaction', methods=['POST', 'GET'])
def create_new_record_transaction_html():
    if request.method == 'GET':
        return render_template('create_record_transaction_form.html')  # Render form for adding new record
    elif request.method == 'POST':
        table_name = request.form['table_name']
        values = [request.form['value1'], request.form['value2'], ...]  # Get values from the form
        create_new_record_transaction(table_name, values)  # Call function to create a new record within a transaction
        return "New record added successfully within a transaction!"  # Return success message

# Add route for generating reports and exporting as CSV
@app.route('/generate_report', methods=['POST'])
def generate_report_html():
    table_name = request.form['table_name']
    output_name = request.form['output_name']
    generate_report(table_name, output_name)
    return f"Report '{table_name}_report.csv' generated successfully."

# Add route for performing aggregation/group-by
@app.route('/perform_aggregation', methods=['POST'])
def perform_aggregation_html():
    operation = request.form['operation']
    table_name = request.form['table_name']
    value = request.form['value']
    perform_aggregation(operation, table_name, value)
    return "Aggregation performed successfully."

# Add route for using subqueries
@app.route('/use_subquery', methods=['GET'])
def use_subquery_html():
    use_subquery()
    return "Subquery executed successfully."

# Add route for performing joins across at least 3 tables
@app.route('/perform_joins', methods=['GET'])
def perform_joins_html():
    perform_joins()
    return "Joins across at least 3 tables performed successfully."


if __name__ == "__main__":
    app.run(debug=True)
