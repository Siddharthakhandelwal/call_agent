import os
from supabase import create_client, Client
import datetime

# Supabase credentials
SUPABASE_URL = "https://mwytkzzzvtdwsscmxqgo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im13eXRrenp6dnRkd3NzY214cWdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjU5NjQ2NiwiZXhwIjoyMDU4MTcyNDY2fQ.pM8de7Nyu71si4M9PLoKsbTGJxW_4ilZcNXBmkfndCQ"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to update only the summary
def update_summary(contact_id, summary):
    """
    Updates only the summary for a given contact ID.
    
    :param contact_id: ID of the contact to update
    :param summary: Summary of the call
    """
    response = (
        supabase.table("general_contacts")
        .update({"summary": summary})
        .eq("id", contact_id)
        .execute()
    )

    if response.data:
        print(f"✅ Summary updated successfully for Contact ID: {contact_id}")
    else:
        print(f"⚠️ Failed to update summary. Response: {response}")

# Function to update only the callback time
def update_callback_time(contact_id, callback_time):
    """
    Updates only the callback time for a given contact ID.
    
    :param contact_id: ID of the contact to update
    :param callback_time: Exact callback time in 'YYYY-MM-DD HH:MM' format (UTC)
    """
    try:
        # Convert string input to datetime object and format it correctly
        callback_time_obj = datetime.datetime.strptime(callback_time, "%Y-%m-%d %H:%M")
        callback_time_iso = callback_time_obj.isoformat()

        response = (
            supabase.table("general_contacts")
            .update({"callback_time": callback_time_iso})
            .eq("id", contact_id)
            .execute()
        )

        if response.data:
            print(f"✅ Callback time updated successfully for Contact ID: {contact_id}")
        else:
            print(f"⚠️ Failed to update callback time. Response: {response}")

    except ValueError:
        print("❌ Invalid date format. Please enter time in 'YYYY-MM-DD HH:MM' format.")

# Example usage