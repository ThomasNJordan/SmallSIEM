import mysql.connector
import csv

# Function to connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="CPSC408!",
        database="SIEM_DB"
    )

# Function to get columns from a table
def get_columns(table_name):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        columns = display_records(table_name)
        column_names = list(columns[0].keys()) if columns else []

        return column_names

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to display records from a table
def display_records(table_name):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return records

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to query with parameters/filters
def query_database_with_filters(table_name, column, value):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Using parameterized query to prevent SQL injection
        query = f"SELECT * FROM {table_name} WHERE {column} LIKE %s;"
        cursor.execute(query, (value,))

        records = cursor.fetchall()

        # Display filtered records
        result = []
        for record in records:
            result.append(record)

        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to create a new record
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

# Function to delete records
def delete_records(table_name, condition):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        query = f"DELETE FROM {table_name} WHERE {condition};"
        cursor.execute(query)
        
        db.commit()
        print("Records deleted successfully.")

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to update records
def update_records(table_name, column, value, condition):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        query = f"UPDATE {table_name} SET {column} = '{value}' WHERE {condition};"
        cursor.execute(query)
        
        db.commit()
        print("Records updated successfully.")

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to create a new record within a transaction
def create_new_record_transaction(table_name, values):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Start the transaction
        db.start_transaction()

        # Generating placeholders dynamically based on the number of values
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        cursor.execute(query, values)
        
        # Commit the transaction if all operations succeed
        db.commit()
        print("New record inserted successfully.")

    except mysql.connector.Error as err:
        # Rollback the transaction if any operation fails
        db.rollback()
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to generate reports and export as CSV
def generate_report(table_name, output_name):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        records = cursor.fetchall()

        # Write records to a CSV file
        with open(f"{output_name}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(records)
        
        print(f"Report '{table_name}_report.csv' generated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def perform_aggregation(table, value):
    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)  # Use dictionary cursor to get records as dictionaries

        query = f"SELECT *, {value} FROM {table} GROUP BY {value};"
        cursor.execute(query)
        records = cursor.fetchall()

        # Return aggregated records
        return records

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to use subqueries
def use_subquery():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        query = "SELECT * FROM Location WHERE LocationID IN (SELECT LocationID FROM EventLogs);"
        cursor.execute(query)
        records = cursor.fetchall()

        # Display records from subquery
        for record in records:
            return record

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Function to perform joins across at least 3 tables
def perform_joins():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        query = """
            SELECT *
            FROM Location
            JOIN EventLogs ON Location.LocationID = EventLogs.LocationID
            JOIN UserEvents ON EventLogs.EventLogID = UserEvents.EventLogID;
        """
        cursor.execute(query)
        records = cursor.fetchall()

        # Display records from join
        for record in records:
            return record

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()
