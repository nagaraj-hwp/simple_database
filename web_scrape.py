import requests
import mysql.connector
import sys
import datetime
import json
import getpass

hostname = input("Enter the host name or host IP address: ")
username = input("Enter the username: ")
user_password = getpass.getpass("Enter the password for the above entered username: ")
database_name = input("Enter the database name you wanted to perform operations: ")

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host=hostname,
    user=username,
    password=user_password,
    database=database_name
)

if conn.is_connected():
    print("Connected to MySQL database")
else:
    print("Failed to connect to MySQL database")
    sys.exit(1)

cursor = conn.cursor(prepared=True)
cursor.execute("SELECT VERSION()")
result = cursor.fetchone()
print("MySQL Server Version:", result[0])

# Create a table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS market_data (
        symbol VARCHAR(255) PRIMARY KEY,
        high DECIMAL(18, 8),
        low DECIMAL(18, 8),
        volume DECIMAL(18, 8),
        quotevolume DECIMAL(18, 8),
        percentchange DECIMAL(18, 8),
        updatedtime VARCHAR(255)
    );
'''
cursor.execute(create_table_query)

# Get a list of tables in the database
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# # Print the table names
# for table in tables:
#     print(table[0])
#     # Get columns information for a specific table
#     table_name = table[0]
#     cursor.execute(f"DESCRIBE {table_name}")

#     # Fetch all column information
#     columns = cursor.fetchall()

#     # Print the column names
#     for column in columns:
#         print(column[0])

print()
###########################################################################################
# Retrieve data from the API endpoint
url = "https://api.bittrex.com/v3/markets/summaries"
response = requests.get(url)
data = response.json()

# Insert data into the market_data table
insert_query = """
    INSERT INTO market_data (symbol, high, low, volume, quotevolume, percentchange, updatedtime)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for row in data:
    symbol = row.get('symbol', None)
    high = row.get('high', None)
    low = row.get('low', None)
    volume = row.get('volume', None)
    quotevolume = row.get('quoteVolume', None)
    percentchange = row.get('percentChange', None)
    updatedtime = row.get('updatedAt', None)

    cursor.execute(insert_query, (symbol, high, low, volume, quotevolume, percentchange, updatedtime))

# Commit the changes and close the connection
conn.commit()
conn.close()
###########################################################################################
