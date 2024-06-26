import streamlit as st
import sqlite3
import csv
import time
import logging
import pandas as pd
from io import StringIO  
from faker import Faker
import threading
import schedule

# Configure Logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fake = Faker()

# Database Configuration (Use environment variables or secure config in production)
DB_NAME = 'your_database.db'
TABLE_NAME = 'rakesh'
BATCH_SIZE = 30

# --- Global Flags ---

data_initialized = False
processing_complete = False  # Add a flag to track if all rows have been processed

# --- Database Functions ---

def create_sample_data(cursor, num_entries=100):
    """Creates a limited number of sample customer data rows."""

    # Check how many rows already exist
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    existing_rows = cursor.fetchone()[0]
    rows_to_create = max(0, num_entries - existing_rows)

    if rows_to_create > 0:
        logging.info(f"Creating {rows_to_create} new rows in {TABLE_NAME}.")
        for _ in range(rows_to_create):
            cursor.execute(
                f"INSERT INTO {TABLE_NAME} (CustomerId, FirstName, LastName, City, Email, SubscriptionDate) VALUES (?, ?, ?, ?, ?, ?)",
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
        logging.info(f"Table {TABLE_NAME} already has 100 or more rows. No new rows created.")


def fetch_and_create_csv(batch_size=BATCH_SIZE):
    """Fetches and processes rows in batches periodically."""
    global data_initialized, processing_complete  # Access global flags

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if not data_initialized:
            create_sample_data(cursor)  # Create data only once
            data_initialized = True  # Set flag to True

        offset = 0

        while not processing_complete:  # Check flag to stop the loop
            try:
                cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY id LIMIT ? OFFSET ?", (batch_size, offset))
                data = cursor.fetchall()

                if not data:
                    logging.info("All rows fetched. No more rows to process.")
                    processing_complete = True  # Signal completion
                    schedule.clear()  # Clear all scheduled jobs to prevent further runs.
                    break

                df = pd.DataFrame(data, columns=["Id", "CustomerId", "FirstName", "LastName", "City", "Email", "SubscriptionDate"])

                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)

                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"customer_data_{timestamp}_{offset}.csv"

                with open(filename, 'w', newline='') as csvfile:
                    csvfile.write(csv_buffer.getvalue())

                logging.info(f"CSV file '{filename}' created successfully.")

                offset += batch_size

            except Exception as e:
                logging.error(f"Error processing rows: {e}")
                break  # Exit loop on error


# --- Streamlit App ---

st.title("Customer Data Extraction to CSV")

# Batch Size Input (Optional)
batch_size = st.number_input("Enter Batch Size (Default: 30)", min_value=1, value=BATCH_SIZE)

if st.button("Generate CSV Files Periodically"):
    # Create a new thread for scheduling
    def run_schedule():
        global processing_complete
        processing_complete = False
        schedule.every(1).minute.do(lambda: fetch_and_create_csv(batch_size))
        while not processing_complete: # Keep running until all scheduled jobs are done
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_schedule).start()
    st.success("CSV generation scheduled to run every minute!")

# --- Database Initialization ---

with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}'")
    if not cursor.fetchone():
        cursor.execute(f'''
            CREATE TABLE {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerId INTEGER,
                FirstName TEXT,
                LastName TEXT,
                City TEXT,
                Email TEXT,
                SubscriptionDate DATE
            )
        ''')
