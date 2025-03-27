import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key

# Load environment variables from .env file
load_dotenv()

# Withings API credentials
CLIENT_ID = os.getenv("WITHINGS_CLIENT_ID")
CLIENT_SECRET = os.getenv("WITHINGS_CLIENT_SECRET")
REDIRECT_URI = os.getenv("WITHINGS_REDIRECT_URI")  # e.g., "http://localhost/callback"
ACCESS_TOKEN = os.getenv("WITHINGS_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("WITHINGS_REFRESH_TOKEN")

# Withings API endpoints
TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
MEASURES_URL = "https://wbsapi.withings.net/measure"

def refresh_access_token(retries=3):
    """Refresh the access token using the refresh token, with retry logic."""
    global ACCESS_TOKEN, REFRESH_TOKEN
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt} to refresh access token...")
            response = requests.post(
                TOKEN_URL,
                data={
                    "action": "requesttoken",
                    "grant_type": "refresh_token",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "refresh_token": REFRESH_TOKEN,
                },
            )
            response_data = response.json()
            print(f"Token Refresh Response: {response_data}")  # Debugging

            if response.status_code == 200 and "body" in response_data:
                ACCESS_TOKEN = response_data["body"]["access_token"]
                REFRESH_TOKEN = response_data["body"]["refresh_token"]
                print("Access token refreshed successfully.")

                # Save the new tokens to the .env file
                set_key(".env", "WITHINGS_ACCESS_TOKEN", ACCESS_TOKEN)
                set_key(".env", "WITHINGS_REFRESH_TOKEN", REFRESH_TOKEN)

                return ACCESS_TOKEN
            else:
                print(f"Failed to refresh token: {response_data}")
        except Exception as e:
            print(f"Error refreshing token on attempt {attempt}: {e}")

        # If this was the last attempt, raise an exception
        if attempt == retries:
            raise Exception("Failed to refresh access token after multiple attempts.")

def fetch_weight_data():
    """Fetch weight data from the Withings API."""
    global ACCESS_TOKEN
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    start_date = int((datetime.now() - timedelta(days=30)).timestamp())
    end_date = int(datetime.now().timestamp())

    try:
        response = requests.post(
            MEASURES_URL,
            headers=headers,
            data={
                "action": "getmeas",
                "meastype": 1,  # Weight
                "category": 1,  # Real measurements
                "startdate": start_date,
                "enddate": end_date,
            },
        )
        response_data = response.json()
        print(f"Fetch Weight Response: {response_data}")  # Debugging

        # If the access token is invalid, refresh it and retry
        if response.status_code == 401:  # Unauthorized
            print("Access token expired. Refreshing...")
            refresh_access_token()
            headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
            response = requests.post(
                MEASURES_URL,
                headers=headers,
                data={
                    "action": "getmeas",
                    "meastype": 1,
                    "category": 1,
                    "startdate": start_date,
                    "enddate": end_date,
                },
            )
            response_data = response.json()

        if response.status_code == 200 and "body" in response_data:
            measures = response_data["body"]["measuregrps"]
            weights = [
                measure["measures"][0]["value"] * (10 ** measure["measures"][0]["unit"])
                for measure in measures
            ]
            return weights
        else:
            raise Exception(f"Failed to fetch weight data: {response_data}")
    except Exception as e:
        print(f"Error fetching weight data: {e}")
        raise

def main():
    try:
        # Fetch weight data
        refresh_access_token()
        weights = fetch_weight_data()
        if weights:
            print(f"Your weights for the past month: {weights}")
            print(f"Most recent weight: {weights[-1]} kg")
        else:
            print("No weight data found for the past month.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()