import os
import datetime
from datetime import timedelta
import requests  # Import requests module to send HTTP requests

#from ms_teams_webhook import MSTeamsWebhookClient  # Assuming you have a library to send MS Teams messages

# def send_to_teams(message):
#     webhook_url = "YOUR_MS_TEAMS_WEBHOOK_URL"  # Replace with your webhook URL
#     teams_client = MSTeamsWebhookClient(webhook_url)
#     teams_client.send_text(message)


def send_to_teams(message):
    webhook_url = "YOUR_MS_TEAMS_WEBHOOK_URL"  # Replace with your webhook URL
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": message
    }
    # Send POST request to MS Teams webhook
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully!!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")


def check_csv_files():
    # Specify the folder path
    folder_path = "/path/to/your/folder"

    # Get the current time and the threshold time (30 minutes ago)
    now = datetime.datetime.now()
    threshold_time = now - timedelta(minutes=30)

    # Initialize a list to store outdated files
    issues = []

    # Iterate through files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)

            # Get the last modified time of the file
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            # Check if the file was modified within the last 30 minutes
            if modified_time < threshold_time:
                issues.append((file_name, modified_time))

    # Notify through MS Teams channel (not to personal account)
    if issues:
        message = "The following files were not updated within the last 30 minutes:\n"
        for file_name, modified_date in issues:
            message += f"- {file_name}, Last Modified: {modified_date}\n"
        send_to_teams(message)
    else:
        send_to_teams("All .csv files are up-to-date. All good!")

if __name__ == "__main__":
    check_csv_files()
