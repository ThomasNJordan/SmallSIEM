from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from query import *

app = Flask(__name__, template_folder='templates')
# To enable cookies
app.secret_key = b'CPSC408!'

@app.route('/get_tables', methods=['GET'])
def get_tables():
    tables = get_all_tables()  # Function to retrieve all tables from the database
    return jsonify(tables)

# Route for the main dashboard
@app.route('/')
def dashboard():
    return render_template('index.html', messages=get_flashed_messages())

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
    return render_template('query_with_filters.html', table_name=table_name, records=records)

'''
The following code is for creating a new record
'''
@app.route('/create_new_record', methods=['POST'])
def create_new_record_get():
    try:
        table_name = request.form['table_name']
        columns = get_columns(table_name)
        return render_template('create_new_record.html', table_name=table_name, columns=columns)
    
    except Exception as e:
        print(f"Exception: {e}")
        return "An error occurred while fetching column names."

@app.route('/add_record', methods=['POST'])
def add_record():
    try:
        table_name = request.form['table_name']
        values = [request.form[column] for column in request.form if column != 'table_name']
        
        create_new_record(table_name, values)  # Call the function to create a new record in query.py
        
        flaflash('New record added successfully!', 'create')
        return render_template('index.html')

    except Exception as e:
        print(f"Exception: {e}")
        return "An error occurred while adding a new record."
####

@app.route('/delete_records', methods=['GET', 'POST'])
def delete_records_html():
    try:
        table_name = request.form['table_name']
        condition = request.form['condition']
        delete_records(table_name, condition)

        flash('Record deleted successfully!', 'delete')
        return render_template('index.html')
    except Exception as e:
        # In case of an error, flash an error message
        flash(f"Error: {e}", 'error')
        return redirect(url_for('display_records_html', table_name=table_name, condition=condition))

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
