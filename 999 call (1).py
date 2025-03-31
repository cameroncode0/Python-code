import time
from datetime import datetime

# Initialize a list to keep track of 999 call timestamps and log file name
detected_calls = []
log_file = "999_calls_log.txt"

def log_to_file(entry):
    """Append the entry to the log file."""
    with open(log_file, "a") as file:
        file.write(entry + "\n")

def monitor_calls():
    print("Monitoring for 999 calls... Type 'exit' to stop.")
    
    # Start the monitoring loop
    while True:
        user_input = input("Enter call input: ")  # Replace this with your actual input source.
        
        if user_input.lower() == "exit":
            print("Stopping monitoring.")
            break
        
        if "999" in user_input:
            # Log the 999 call with a timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"🚨 999 call detected at {timestamp}"
            detected_calls.append(log_entry)  # Add to list
            log_to_file(log_entry)  # Add to file
            print(log_entry)
        else:
            print("No 999 call detected.")

        # Print the running total of detected 999 calls
        print(f"Total 999 calls detected so far: {len(detected_calls)}\n")
        
        time.sleep(1)  # Pause to simulate time delay, adjust as needed.

    # Display a summary of all detected 999 calls from the list at the end of the session
    print("\nSummary of Detected 999 Calls:")
    if detected_calls:
        for call in detected_calls:
            print(call)
        print(f"\nTotal 999 calls detected: {len(detected_calls)}")
    else:
        print("No 999 calls were detected during this session.")

# Run the monitoring function if the script is executed directly
if __name__ == "__main__":
    # Clear log file at the start of each session
    open(log_file, "w").close()
    monitor_calls()
