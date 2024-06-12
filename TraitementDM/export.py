import csv
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Define the tables you want to export
tables = ['shirts', 'cart', 'users', 'purchases'] 

# Export each table to a separate CSV file
for table in tables:
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    # Write to CSV file
    with open(f"{table}.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)

# Close the connection
conn.close()

print("Data export complete.")
