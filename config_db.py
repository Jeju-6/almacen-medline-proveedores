DB_CONFIG = {
    'host': 'aws-1-us-east-2.pooler.supabase.com',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres.alvxqmzaiocvmdkjgpqh',
    'password': 'AlmacenMedline'
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"