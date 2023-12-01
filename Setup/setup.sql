CREATE DATABASE IF NOT EXISTS SIEM_DB;
USE SIEM_DB;

CREATE TABLE Location (
    LocationID INT PRIMARY KEY AUTO_INCREMENT,
    City VARCHAR(256),
    Country VARCHAR(256),
    Region VARCHAR(256),
    ZIPCode VARCHAR(20),
    ISP VARCHAR(100),
    Longitude DECIMAL(15, 10),  -- Total digits: 15, Digits after decimal point: 10
    Latitude DECIMAL(15, 10)   -- Total digits: 15, Digits after decimal point: 10
);

CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100)
);

CREATE TABLE IPAddress (
    IPAddressID INT PRIMARY KEY AUTO_INCREMENT,
    IPAddress VARCHAR(50),  -- Change the data type and size as per your requirements
    DNS VARCHAR(100),
    Version VARCHAR(10),
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE EventLogs (
    EventLogID INT PRIMARY KEY AUTO_INCREMENT,
    EventStartTime DATETIME,
    EventEndTime DATETIME,
    Severity INT,
    LocationID INT,
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(50),
    EventLogID INT,
    FOREIGN KEY (EventLogID) REFERENCES EventLogs(EventLogID)
);

CREATE TABLE UserEvents (
    UserID INT,
    EventID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    PRIMARY KEY (UserID, EventID)
);
