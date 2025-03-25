import os
from supabase import create_client, Client
import datetime
import pytz  # For handling time zones
from general.main import make_vapi_call
import time
# Supabase credentials
SUPABASE_URL = "https://mwytkzzzvtdwsscmxqgo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im13eXRrenp6dnRkd3NzY214cWdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjU5NjQ2NiwiZXhwIjoyMDU4MTcyNDY2fQ.pM8de7Nyu71si4M9PLoKsbTGJxW_4ilZcNXBmkfndCQ"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to get timezone from country code
def get_timezone(country_code):
    country_timezones = {
        "US": "America/New_York",  # Example: US → New York timezone
        "IN": "Asia/Kolkata",      # Example: India → Kolkata timezone
        "UK": "Europe/London",     # Example: UK → London timezone
    }
    return country_timezones.get(country_code, "UTC")  # Default to UTC if unknown

# Function to check if the current time is daytime (8 AM to 6 PM)
def is_daytime(country_code):
    timezone = pytz.timezone(get_timezone(country_code))
    now = datetime.datetime.now(timezone).time()
    return datetime.time(8, 0) <= now <= datetime.time(18, 0)

# Function to fetch latest data from Supabase
def fetch_data(table_name):
    response = supabase.table(table_name).select("id, name, country_code, phone, email, date_time").execute()
    return response.data if response.data else []

# Custom sorting function
def sort_and_interleave(entries):
    with_datetime = [entry for entry in entries if entry.get('date_time')]
    without_datetime = [entry for entry in entries if not entry.get('date_time')]

    # Convert date_time strings to datetime objects
    for entry in with_datetime:
        entry['date_time'] = datetime.datetime.fromisoformat(entry['date_time'])

    with_datetime.sort(key=lambda x: x['date_time'])

    result = []
    index_without = 0

    for entry in with_datetime:
        result.append(entry)
        if index_without < len(without_datetime):
            result.append(without_datetime[index_without])
            index_without += 1

    result.extend(without_datetime[index_without:])
    return result

# Main execution
if __name__ == "__main__":
    table_name = "general_contacts"

    while True:  # Keep refreshing data and checking for calls
        data = fetch_data(table_name)  # Refresh data before each check
        if not data:
            print("No data found.")
            break  # Exit if no data

        sorted_data = sort_and_interleave(data)
        current_utc_time = datetime.datetime.utcnow().replace(second=0, microsecond=0)

        for row in sorted_data:
            # Fetch latest data before processing each contact
            refreshed_data = fetch_data(table_name)  
            contact = next((c for c in refreshed_data if c["id"] == row["id"]), row)  # Update contact if new data exists

            name = contact.get("name")
            number = f"{contact.get('country_code', '')}{contact.get('phone', '')}"
            mail = contact.get("email")
            contact_id = contact.get("id")
            country_code = contact.get("country_code")
            contact_time = contact.get("date_time")

            # Convert stored date_time to UTC for comparison
            if contact_time:
                contact_time = datetime.datetime.fromisoformat(contact_time).replace(second=0, microsecond=0)
                if contact_time == current_utc_time:
                    make_vapi_call(name, number, mail, contact_id)  # Call if time matches

            # Call if there is **no date_time** but it's daytime in their country
            elif is_daytime(country_code):
                make_vapi_call(name, number, mail, contact_id)

        print("Waiting for next check...")
        time.sleep(60)  # Wait for 60 seconds before checking again
