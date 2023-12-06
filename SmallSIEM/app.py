from flask import Flask, render_template, request
from query import *

app = Flask(__name__, template_folder='templates')

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
def query_with_filters():
    table_name = request.form['table_name']
    column = request.form['column']
    value = request.form['value']
    records = query_with_filters(table_name, column, value)
    return render_template('display_records.html', table_name=table_name, records=records)

@app.route('/create_new_record', methods=['POST', 'GET'])
def create_new_record():
    if request.method == 'GET':
        return render_template('create_record_form.html')  # Render form for adding new record
    elif request.method == 'POST':
        table_name = request.form['table_name']
        values = [request.form['value1'], request.form['value2'], ...]  # Get values from the form
        create_new_record(table_name, values)  # Call function to create a new record
        return "New record added successfully!"  # Return success message

if __name__ == "__main__":
    app.run(debug=True)

