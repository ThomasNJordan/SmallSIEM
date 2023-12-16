# Use Ubuntu as the base image
FROM ubuntu:latest

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    mysql-server \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV MYSQL_ROOT_PASSWORD="CPSC408!"
ENV MYSQL_DATABASE="SIEM_DB"

# Expose the default MySQL and Flask ports
EXPOSE 3306
EXPOSE 5000

# Create a directory for the app
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Start the MySQL service (might not be required, depending on the image)
# CMD service mysql start

# Start the Flask app
CMD ["python3", "app.py"]
