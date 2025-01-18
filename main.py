import os
import glob
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- Configuration ---
KEY_FILE_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "path/to/your/service_account_key.json")  # Replace with your path
SCOPES = ['https://www.googleapis.com/auth/drive']
PROJECT_BASE_NAME = "Symbiosis_Core_v"
PROJECT_FILE_PATTERN = f"{PROJECT_BASE_NAME}*.json"

# --- Authentication Function ---
def authenticate():
    """Authenticates with Google Drive API using service account."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            KEY_FILE_PATH, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        print("Authentication successful!")
        return service
    except FileNotFoundError:
        print(f"Authentication error: Key file not found at {KEY_FILE_PATH}")
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

# --- Data Loading Function ---
def load_latest_project_data():
    """Loads the latest version of the project data."""
    try:
        files = glob.glob(PROJECT_FILE_PATTERN)
        if not files:
            print(f"Error: No project files found matching pattern '{PROJECT_FILE_PATTERN}'.")
            return None

        latest_file = max(files)
        with open(latest_file, 'r') as f:
            data = json.load(f)
        print(f"Loaded {latest_file}")
        return data
    except FileNotFoundError:
        print(f"Error: File '{latest_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{latest_file}'.")
        return None

# --- Main Terminal Loop ---
def main():
    service = authenticate()
    if not service:
        return  # Exit if authentication fails

    project_data = load_latest_project_data()
    if not project_data:
        return

    while True:
        user_input = input(">>> ")

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "show project name":
            print(f"Project Name: {project_data.get('project_name', 'N/A')}")
        elif user_input.lower() == "show version":
            print(f"Version: {project_data.get('version', 'N/A')}")
        elif user_input.lower() == "show last updated":
            print(f"Last Updated: {project_data.get('last_updated', 'N/A')}")
        elif user_input.lower() == "show project goals":
            goals = project_data.get('project_goals', [])
            if goals:
                for i, goal in enumerate(goals):
                    print(f"{i + 1}. {goal}")
            else:
                print("No project goals found.")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()