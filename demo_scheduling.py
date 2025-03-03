import re
import json
import google.auth
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import llm

# Load environment variables from .env file
load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")  # Path to credentials JSON
SCOPES = [os.getenv("SCOPES")]  # API scope
CALENDAR_ID = os.getenv("CALENDAR_ID")  # Google Calendar ID
EVENTS_FILE = os.getenv("EVENTS_FILE")  # JSON file for storing events

# Authenticate with Google Calendar API
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
calendar_service = build("calendar", "v3", credentials=creds)

# 🔹 AI-Based Busy Detection
def detect_busy_response(user_input):
    """Uses AI to detect if the user is busy based on context."""
    response = llm.invoke(f"User keh raha hai: '{user_input}'. Kya yeh busy hai? Agar haan toh 'yes' likho, warna 'no'.")
    return "yes" in response.content.lower() if hasattr(response, "content") else "yes" in str(response).lower()

# 🔹 Save event to JSON file
def save_event_to_json(event_data):
    """Stores the scheduled event details in a JSON file."""
    try:
        # Load existing events
        try:
            with open(EVENTS_FILE, "r") as file:
                events = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            events = []

        # Append new event
        events.append(event_data)

        # Save updated events list
        with open(EVENTS_FILE, "w") as file:
            json.dump(events, file, indent=4)

        return True
    except Exception as e:
        print(f"Error saving event: {e}")
        return False

# 🔹 Google Calendar Event Creation
def create_calendar_event(name, date, time):
    """Schedules an ERP demo in Google Calendar and logs it in a JSON file."""
    event = {
        "summary": f"ERP Demo for {name}",
        "description": "ERP demo session",
        "start": {"dateTime": f"{date}T{time}:00", "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": f"{date}T{time}:30", "timeZone": "Asia/Kolkata"},
    }
    
    try:
        event_result = calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        event_data = {
            "name": name,
            "date": date,
            "time": time,
            "event_id": event_result.get("id"),
            "event_link": event_result.get("htmlLink"),
        }
        
        # Save to JSON
        save_event_to_json(event_data)

        return f"📅 Demo schedule ho gaya hai! Aapka time: {date} {time}. \nEvent Link: {event_result.get('htmlLink')}"
    except Exception as e:
        return f"❌ Error: Event create nahi ho saka. {str(e)}"

# 🔹 Main Demo Scheduling Function
def demo_scheduling_tool(user_input):
    """Handles ERP demo scheduling."""
    if detect_busy_response(user_input):
        return "Samajh gaya! Aap kis time free honge taaki main ek convenient time par demo schedule kar saku?"

    match = re.search(r"(\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) for (.+)", user_input)
    if match:
        date, time, name = match.groups()
        confirmation_message = create_calendar_event(name, date, time)
        return f"✅ {confirmation_message} \nAgar aapko aur koi help chahiye toh bataiye!"

    return "Kripya details is format me dein: 'YYYY-MM-DD at HH:MM for Name'."
