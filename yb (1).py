import os
import time
import sqlite3
from datetime import datetime, timedelta

# Path to the Chrome history file (replace with the appropriate path if different)
history_path = os.path.expanduser(
    r"~\AppData\Local\Google\Chrome\User Data\Default\History"
)

def check_youtube_visits():
    try:
        # Connect to the Chrome history SQLite database
        with sqlite3.connect(history_path) as conn:
            cursor = conn.cursor()
            
            # Query to find recent visits to youtube.com
            query = """
            SELECT url, last_visit_time
            FROM urls
            WHERE url LIKE '%youtube.com%'
            ORDER BY last_visit_time DESC
            LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                url, last_visit_time = result
                # Convert last_visit_time from Chrome format to a readable datetime
                # Chrome stores timestamps in "Webkit" format (microseconds since 1601-01-01)
                last_visit_dt = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
                
                # Alert the user if youtube.com was visited recently
                print(f"🔔 Alert: You visited YouTube at {last_visit_dt}!")
            else:
                print("No recent YouTube visits detected.")

    except sqlite3.OperationalError:
        print("Error: Unable to access the history database. Close Chrome and try again.")

if __name__ == "__main__":
    print("Monitoring for visits to youtube.com... Press Ctrl+C to stop.")
    while True:
        check_youtube_visits()
        time.sleep(10)  # Check every 10 seconds
