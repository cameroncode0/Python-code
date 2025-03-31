import time
import re

# Log file path (default for authentication logs on Linux)
LOG_FILE = "/var/log/auth.log"

# Define keywords to search for common brute-force patterns
SUSPICIOUS_PATTERNS = [
    "Failed password",    # Failed login attempts
    "Invalid user",       # Invalid usernames
    "Connection closed",  # Frequent disconnections
]

# Track previously seen lines to avoid redundant alerts
def tail_log(file_path):
    with open(file_path, "r") as f:
        f.seek(0, 2)  # Move to the end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)  # Wait for new data
                continue
            yield line

# Monitor log file and alert on suspicious patterns
def detect_attacks():
    print("Monitoring log file for suspicious activity...")
    for line in tail_log(LOG_FILE):
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, line):
                print(f"ALERT: Possible cyber attack detected! Log entry: {line.strip()}")

# Start monitoring
if __name__ == "__main__":
    try:
        detect_attacks()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"Error: {e}")
