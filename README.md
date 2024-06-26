python -m streamlit run apps.py
python csv_to_xml_converter.py
python sorting_xml_to_csv.py
python -m streamlit run app.py
pip install streamlit pandas sqlite3 faker   ## requirements for python


Multi-threading in Your Code:

In the code, multi-threading is used to decouple the Streamlit web interface from the background task of periodically generating CSV files.

Main Thread (Streamlit): This thread handles the user interface:

Displaying the app
Responding to button clicks
Background Thread (CSV Generation):  When you click the "Generate CSV Files Periodically" button, a new thread is created. This thread executes the run_schedule function, which does the following:

Scheduling: It sets up a schedule to call the fetch_and_create_csv function every minute.
Loop: It enters a loop where it continuously checks if there are pending scheduled tasks (schedule.run_pending()) and pauses for a second (time.sleep(1)) before checking again.
Stopping the Threads:

The fetch_and_create_csv function contains logic to detect when all rows have been processed.
When this happens, it signals the background thread to stop by setting the processing_complete flag to True and clears the scheduled tasks.
The background thread's while loop then exits, and the thread terminates