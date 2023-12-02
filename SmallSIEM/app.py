from flask import Flask, render_template, request, jsonify
from query import *
import json

app = Flask(__name__, template_folder='templates')

# Route for the home page
@app.route('/')
def index():
    content = "Hello, World!"
    return content

# Route to render the form to enter the table name
@app.route('/display_records', methods=['GET'])
def display_records_form():
    return render_template('display_records.html')

# Route to handle form submission and display records based on the provided table name
@app.route('/display_records', methods=['POST'])
def display_records_route():
    try:
        table_name = request.form['table']  # Get the table name from the submitted form

        # Call the function from query.py to display records for the specified table
        result = display_records(table_name)

        # Return the result as JSON or in any other suitable format
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})  # Return error message if an exception occurs

# You need to add similar routes for other functionalities (e.g., query_with_filters, create_new_record, delete_records, etc.)

if __name__ == "__main__":
    app.run(debug=True)


