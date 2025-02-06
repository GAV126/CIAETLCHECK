import os
import time
import shutil
import getpass
import win32net
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
FOLDER_A = "//serverA/path/to/folder_A"
FOLDER_B = "//serverB/path/to/folder_B"  # This can be passed as a parameter
POLLING_INTERVAL = 2  # Seconds

# Authentication
SERVER_A = "\\serverA"
SERVER_B = "\\serverB"
USERNAME = input("Enter username: ")
PASSWORD = getpass.getpass("Enter password: ")

credentials = {"remote": SERVER_A, "username": USERNAME, "password": PASSWORD}
try:
    win32net.NetUseAdd(None, 2, credentials)
    print(f"Authenticated to {SERVER_A}")
except Exception as e:
    print(f"Failed to authenticate: {e}")
    exit(1)


class CSVFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            self.copy_file(event.src_path)

    def copy_file(self, src_path):
        filename = os.path.basename(src_path)
        dest_path = os.path.join(FOLDER_B, filename)
        print(f"Copying {filename} to {FOLDER_B}...")
        shutil.copy2(src_path, dest_path)
        print(f"Copied {filename} successfully!")


if __name__ == "__main__":
    run_script = input("Do you want to start monitoring? (yes/no): ").strip().lower()
    if run_script != "yes":
        print("Script execution aborted.")
        exit(0)

    event_handler = CSVFileHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_A, recursive=False)

    print(f"Monitoring {FOLDER_A} for new CSV files...")
    observer.start()

    try:
        while True:
            time.sleep(POLLING_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    print("Stopped monitoring.")
