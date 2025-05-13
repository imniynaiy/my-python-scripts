import sqlite3
import csv

# Define the SQLite database file and CSV file paths
# db_path = '~/Library/Mobile Documents/com~apple~CloudDocs/douban.db'
db_path = './temp/douban.db'
csv_path = './temp/movie-watching.csv'

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Open the CSV file and read its contents
with open(csv_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader)  # Get the first line as column names

    # Create a table with the column names from the CSV
    table_name = 'data_table'
    columns = ', '.join([f'"{header}" TEXT' for header in headers])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

    # Insert the CSV data into the table
    for row in reader:
        placeholders = ', '.join(['?'] * len(headers))
        columns = ', '.join([f'"{header}"' for header in headers])
        cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', row)

# Commit changes and close the connection
conn.commit()
conn.close()