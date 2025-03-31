import psutil
import time

def check_vscode_running():
    """Check if Visual Studio Code (code.exe or code) is running."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'code' or process.info['name'] == 'Code.exe':
            return True
    return False

def monitor_vscode(interval=5):
    """Monitors for the VS Code process and alerts when it starts."""
    vscode_opened = False

    print("Monitoring for VS Code...")

    while True:
        if check_vscode_running():
            if not vscode_opened:
                print("VS Code has been opened!")
                vscode_opened = True
        else:
            vscode_opened = False  # Reset if VS Code is closed

        time.sleep(interval)  # Wait before checking again

# Start monitoring with a check interval of 5 seconds
monitor_vscode(interval=5)
