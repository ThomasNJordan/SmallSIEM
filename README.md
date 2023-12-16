![Logo](logo.png)

# SmallSIEM
A simple SIEM written in Python using a MySQL backend.
SmallSIEM supports the storage and interactions between users, IP addresses, locations, and events
Implements a database using MySQL, Flask, Jinja2, HTML, Python

+Features
+Display records
+Make queries on security events
+Create, delete, and update security events
+Support transactions
+Generate CSV reports of events
+Include views to limit displays of security events to certain users


## Installation
To setup the database, run:
- `pip install -r requirements.txt`
- `mysql -u root -p SIEM_DB < setup.sql`
- `python3 fill_db.py`
Then to setup the webapp:
- `python3 app.py`
