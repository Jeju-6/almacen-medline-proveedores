import psycopg2
import os

def get_db_config():
    return {
        'host': os.environ.get('DB_HOST', 'aws-1-us-east-2.pooler.supabase.com'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'database': os.environ.get('DB_NAME', 'postgres'),
        'user': os.environ.get('DB_USER', 'postgres.alvxqmzaiocvmdkjgpqh'),
        'password': os.environ.get('DB_PASSWORD', '')
    }

def init_db():
    try:
        conn = psycopg2.connect(**get_db_config())
        conn.close()
        print("Conexion a Supabase verificada.")
    except Exception as e:
        print(f"Error conectando a Supabase: {e}")

if __name__ == "__main__":
    init_db()