from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Las variables de entorno SUPABASE_URL o SUPABASE_KEY no están definidas")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_training_data():
    try:
        intents_response = supabase.table("intents").select("*").execute()
        examples_response = supabase.table("examples").select("*").execute()

        print("Respuesta de intents:", intents_response)
        print("Respuesta de examples:", examples_response)

        intents = intents_response.data or []
        examples = examples_response.data or []

        if not intents:
            print("No se encontraron intents en la tabla.")
        if not examples:
            print("No se encontraron examples en la tabla.")

        return intents, examples
    except Exception as e:
        print(f"Error al obtener datos de Supabase: {e}")
        return [], []

def get_response_by_intent(intent_name):
    try:
        response = supabase.table("intents").select("response").eq("name", intent_name).single().execute()
        if response.data:
            return response.data.get("response")
        else:
            print(f"No se encontró respuesta para el intento: {intent_name}")
            return None
    except Exception as e:
        print(f"Error al obtener respuesta por intento: {e}")
        return None

def save_unclassified_message(message):
    try:
        response = supabase.table("unclassified_messages").insert({"text": message}).execute()
        if response.data:
            print(f"Mensaje no clasificado guardado: {response.data}")
        else:
            print("No se pudo guardar el mensaje no clasificado.")
    except Exception as e:
        print(f"Error al guardar mensaje no clasificado: {e}")


def test_connection():
    try:
        intents = supabase.table("intents").select("*").execute().data
        examples = supabase.table("examples").select("*").execute().data
        print("Prueba de conexión exitosa.")
        print("Intents:", intents)
        print("Examples:", examples)
    except Exception as e:
        print(f"Error al conectar a Supabase: {e}")
