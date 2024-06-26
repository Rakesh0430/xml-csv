import sqlite3
import csv
import schedule
import time
import logging
from faker import Faker

# Configure Logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fake = Faker()

def create_sample_data(cursor, num_entries=500):
    """Creates a limited number of sample customer data rows."""

    # Check how many rows already exist
    cursor.execute("SELECT COUNT(*) FROM rakesh")
    existing_rows = cursor.fetchone()[0]
    rows_to_create = max(0, num_entries - existing_rows)

    if rows_to_create > 0:
        logging.info(f"Creating {rows_to_create} new rows.")
        for _ in range(rows_to_create):
            cursor.execute(
                "INSERT INTO rakesh (CustomerId, FirstName, LastName, City, Email, SubscriptionDate) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    fake.random_int(min=1, max=500),
                    fake.first_name(),
                    fake.last_name(),
                    fake.city(),
                    fake.email(),
                    fake.date_this_year()
                )
            )
    else:
        logging.info("Table already has 100 or more rows. No new rows created.")


def fetch_and_create_csv():
    """Fetches records in batches, creates CSVs, and logs until no more rows.
    Stops further execution after processing all rows.
    """
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Create sample data only once at the beginning
    create_sample_data(cursor) 

    batch_size = 50
    offset = 0

    while True:
        try:
            # Fetch a batch of rows
            cursor.execute("SELECT * FROM rakesh ORDER BY id LIMIT ? OFFSET ?", (batch_size, offset))
            data = cursor.fetchall()

            if not data:
                logging.info("All rows fetched. No more rows to process.")
                schedule.clear()  # Clear all scheduled jobs
                break  # Exit the loop when no more rows are found

            # Create CSV for the batch (Outside the try-except block)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"customer_data_{timestamp}_{offset}.csv"
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["CustomerId", "FirstName", "LastName", "City", "Email", "SubscriptionDate"])
                for row in data:
                    writer.writerow(row[1:])
            
            logging.info(f"CSV file '{filename}' created successfully.")

            offset += batch_size

        except Exception as e:
            logging.error(f"Error processing rows: {e}")
            break  # Exit loop on error

    conn.close() # Close the connection after all rows are processed 


# Database Initialization (Create Table and Initial Data)
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rakesh'")
if not cursor.fetchone():  
    cursor.execute('''
        CREATE TABLE rakesh (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerId INTEGER,
            FirstName TEXT,
            LastName TEXT,
            City TEXT,
            Email TEXT,
            SubscriptionDate DATE
        )
    ''')

conn.commit()
conn.close()

# Schedule Task to Run Every Minute
schedule.every(1).minute.do(fetch_and_create_csv)

while True:
    schedule.run_pending()
    time.sleep(1)
