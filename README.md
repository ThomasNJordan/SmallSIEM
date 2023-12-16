![Logo](logo.png)

Thomas Jordan, Thomas Kim, Ewan Shen

# SmallSIEM
A simple SIEM written in Python using a MySQL backend.
SmallSIEM supports the storage and interactions between users, IP addresses, locations, and events
Implements a database using MySQL, Flask, Jinja2, HTML, Python


## Installation
To setup the database, run:
- `pip install -r requirements.txt`
- `mysql -u root -p SIEM_DB < setup.sql`
- `python3 fill_db.py`
Then to setup the webapp:
- `python3 app.py`
