from supabase import create_client

SUPABASE_URL = "https://iixqcpoiptsgqlchyprr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpeHFjcG9pcHRzZ3FsY2h5cHJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQwOTg2MjIsImV4cCI6MjA0OTY3NDYyMn0.ZkAaCGXRL-hjxoScgrR2WmDfT-7Tc15DyQ8MYhBA0ag"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_training_data():
    intents = supabase.table("intents").select("*").execute().data
    examples = supabase.table("examples").select("*").execute().data
    return intents, examples

def save_unclassified_message(message):
    supabase.table("unclassified_messages").insert({"text": message}).execute()
