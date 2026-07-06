import psycopg2
from config_db import DB_CONFIG

def get_db():
    from app import get_db as app_get_db
    return app_get_db()

def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        print("Conexion a Supabase verificada.")
    except Exception as e:
        print(f"Error conectando a Supabase: {e}")

if __name__ == "__main__":
    init_db()