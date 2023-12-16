![Logo](logo.png)

# SmallSIEM
A simple SIEM written in Python using a MySQL backend.

## Installation
To setup the database, run:
- `pip install -r requirements.txt`
- `mysql -u root -p < Setup/setup.sql`
- `python3 Setup/fill_db.py`
Then to setup the webapp:
- `python3 SmallSIEM/app.py`