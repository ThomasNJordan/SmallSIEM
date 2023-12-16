import mysql.connector
from faker import Faker
import random
import datetime

fake = Faker()

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CPSC408!",
    database="SIEM_DB"
)
cursor = db.cursor()

# Generate dummy data for Location table
locations_data = []
for _ in range(50):  # Generating 50 locations
    city = fake.city()
    country = fake.country()
    region = fake.state()
    zip_code = fake.zipcode()
    isp = fake.company()
    longitude = fake.longitude()
    latitude = fake.latitude()
    locations_data.append((city, country, region, zip_code, isp, longitude, latitude))

# Generate dummy data for User table
users_data = []
for _ in range(100):  # Generating 100 users
    user_name = fake.name()
    users_data.append((user_name,))

# Generate dummy data for IPAddress table
ip_addresses_data = []
for _ in range(500):  # Generating 500 IP addresses
    dns = fake.domain_name()
    version = random.choice(['IPv4', 'IPv6'])
    if version == 'IPv4':
        ip_address = fake.ipv4()
    else:
        ip_address = fake.ipv6()
    user_id = random.randint(1, 100)  # Assuming 100 users exist
    ip_addresses_data.append((ip_address, dns, version, user_id))

# Generate dummy data for EventLogs table with weighted severity
event_logs_data = []
for _ in range(1000):  # Generating 1000 event logs
    start_time = fake.date_time_between(start_date='-30d', end_date='now')
    end_time = start_time + datetime.timedelta(minutes=random.randint(30, 120))
    
    # Weighted severity generation
    severity = random.choices([1, 2, 3, 4, 5], weights=[50, 100, 150, 300, 400])[0]
    
    location_id = random.randint(1, 50)  # Assuming 50 locations exist
    event_logs_data.append((start_time, end_time, severity, location_id))

# Generate dummy data for Events table with weighted severity
events_data = []
severity_map = {
    1: "Very low",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Very high"
}

for event_log in event_logs_data:
    severity = event_log[2]  # Index 2 contains severity in event_logs_data
    event_type = severity_map[severity]
    event_log_id = random.randint(1, 1000)  # Assuming 1000 event logs exist
    events_data.append((event_type, event_log_id))

# Generate dummy data for UserEvents table
user_events_data = set()  # Using a set to store unique combinations
while len(user_events_data) < 1000:
    user_id = random.randint(1, 100)  # Assuming user IDs from 1 to 100
    event_id = random.randint(1, 1000)  # Assuming event IDs from 1 to 1000
    user_events_data.add((user_id, event_id))

# Convert set to a list for use in executemany
user_events_data_list = list(user_events_data)

# Insert data into Location table
location_query = "INSERT INTO Location (City, Country, Region, ZIPCode, ISP, Longitude, Latitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(location_query, locations_data)

# Insert data into User table
user_query = "INSERT INTO User (Name) VALUES (%s)"
cursor.executemany(user_query, users_data)

# Insert data into IPAddress table
ip_query = "INSERT INTO IPAddress (DNS, Version, UserID) VALUES (%s, %s, %s)"
cursor.executemany(ip_query, ip_addresses_data)

# Insert data into EventLogs table
event_logs_query = "INSERT INTO EventLogs (EventStartTime, EventEndTime, Severity, LocationID) VALUES (%s, %s, %s, %s)"
cursor.executemany(event_logs_query, event_logs_data)

# Insert data into Events table
events_query = "INSERT INTO Events (Type, EventLogID) VALUES (%s, %s)"
cursor.executemany(events_query, events_data)

# Insert data into UserEvents table
user_events_query = "INSERT INTO UserEvents (UserID, EventID) VALUES (%s, %s)"
cursor.executemany(user_events_query, user_events_data_list)

# Commit changes and close connection
db.commit()
db.close()
