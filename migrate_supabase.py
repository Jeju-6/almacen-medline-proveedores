import psycopg2
from config_db import DB_CONFIG

def migrate():
    conn = psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            contacto VARCHAR(255),
            area VARCHAR(255),
            logo VARCHAR(255),
            activo INTEGER DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(512) NOT NULL,
            rol VARCHAR(50) NOT NULL,
            id_proveedor INTEGER REFERENCES proveedores(id_proveedor),
            email VARCHAR(255),
            activo INTEGER DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS articulos (
            id_articulo SERIAL PRIMARY KEY,
            num_parte VARCHAR(255) NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            descripcion TEXT,
            unidad_medida VARCHAR(50) DEFAULT 'piezas',
            stock_actual INTEGER DEFAULT 0,
            stock_minimo INTEGER DEFAULT 5,
            es_critico INTEGER DEFAULT 0,
            codigo_qr VARCHAR(255) UNIQUE,
            link_compra TEXT,
            imagen VARCHAR(255),
            ubicacion VARCHAR(255),
            id_proveedor INTEGER NOT NULL REFERENCES proveedores(id_proveedor),
            activo INTEGER DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id_movimiento SERIAL PRIMARY KEY,
            id_articulo INTEGER NOT NULL REFERENCES articulos(id_articulo),
            id_usuario INTEGER REFERENCES usuarios(id_usuario),
            tipo VARCHAR(10) NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observaciones TEXT,
            modo_kiosco INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS alertas (
            id_alerta SERIAL PRIMARY KEY,
            id_articulo INTEGER NOT NULL REFERENCES articulos(id_articulo),
            tipo_alerta VARCHAR(50) NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            vista INTEGER DEFAULT 0,
            resuelta INTEGER DEFAULT 0,
            id_usuario_dest INTEGER REFERENCES usuarios(id_usuario)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS ordenes_compra (
            id_orden SERIAL PRIMARY KEY,
            id_articulo INTEGER NOT NULL REFERENCES articulos(id_articulo),
            cantidad_sugerida INTEGER NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(50) DEFAULT 'pendiente',
            notas TEXT,
            id_usuario INTEGER REFERENCES usuarios(id_usuario)
        )
    ''')

    # Crear admin por defecto
    from werkzeug.security import generate_password_hash
    c.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not c.fetchone():
        c.execute('''
            INSERT INTO usuarios (nombre, username, password_hash, rol)
            VALUES (%s, %s, %s, %s)
        ''', ('Administrador', 'admin', generate_password_hash('admin123'), 'admin'))
        print("Usuario admin creado")

    conn.commit()
    conn.close()
    print("Migracion completada exitosamente en Supabase")

if __name__ == "__main__":
    migrate()