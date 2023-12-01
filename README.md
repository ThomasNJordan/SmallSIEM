![Logo](logo.png)

# SmallSIEM
A simple SIEM written in Python using a MySQL backend.

## Installation
To setup the dummy database, run:
- `pip install -r requirements.txt`
- `mysql -u root -p SIEM_DB < setup.sql`
- `python3 fill_db.py`