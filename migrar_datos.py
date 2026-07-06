import sqlite3
import psycopg2
from config_db import DB_CONFIG

def migrar():
    # Conectar a SQLite
    sqlite_conn = sqlite3.connect('almacen.db')
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    # Conectar a Supabase
    pg_conn = psycopg2.connect(**DB_CONFIG)
    pg_cur = pg_conn.cursor()

    print("Migrando proveedores...")
    sqlite_cur.execute("SELECT * FROM proveedores")
    for row in sqlite_cur.fetchall():
        try:
            pg_cur.execute('''
                INSERT INTO proveedores (id_proveedor, nombre, contacto, area, logo, activo)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_proveedor) DO NOTHING
            ''', (row['id_proveedor'], row['nombre'], row['contacto'],
                  row['area'], row['logo'] if 'logo' in row.keys() else None, row['activo']))
        except Exception as e:
            print(f"Error proveedor {row['nombre']}: {e}")
            pg_conn.rollback()
            continue
    pg_conn.commit()
    print(f"Proveedores migrados")

    print("Migrando usuarios...")
    sqlite_cur.execute("SELECT * FROM usuarios")
    for row in sqlite_cur.fetchall():
        try:
            pg_cur.execute('''
                INSERT INTO usuarios (id_usuario, nombre, username, password_hash, rol, id_proveedor, email, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_usuario) DO NOTHING
            ''', (row['id_usuario'], row['nombre'], row['username'], row['password_hash'],
                  row['rol'], row['id_proveedor'], 
                  row['email'] if 'email' in row.keys() else None, row['activo']))
        except Exception as e:
            print(f"Error usuario {row['username']}: {e}")
            pg_conn.rollback()
            continue
    pg_conn.commit()
    print("Usuarios migrados")

    print("Migrando articulos...")
    sqlite_cur.execute("SELECT * FROM articulos")
    for row in sqlite_cur.fetchall():
        try:
            pg_cur.execute('''
                INSERT INTO articulos (id_articulo, num_parte, nombre, descripcion, unidad_medida,
                    stock_actual, stock_minimo, es_critico, codigo_qr, link_compra, imagen, ubicacion, id_proveedor, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_articulo) DO NOTHING
            ''', (row['id_articulo'], row['num_parte'], row['nombre'], row['descripcion'],
                  row['unidad_medida'], row['stock_actual'], row['stock_minimo'], row['es_critico'],
                  row['codigo_qr'], row['link_compra'], row['imagen'],
                  row['ubicacion'] if 'ubicacion' in row.keys() else None,
                  row['id_proveedor'], row['activo']))
        except Exception as e:
            print(f"Error articulo {row['nombre']}: {e}")
            pg_conn.rollback()
            continue
    pg_conn.commit()
    print("Articulos migrados")

    print("Migrando movimientos...")
    sqlite_cur.execute("SELECT * FROM movimientos")
    for row in sqlite_cur.fetchall():
        try:
            pg_cur.execute('''
                INSERT INTO movimientos (id_movimiento, id_articulo, id_usuario, tipo, cantidad, fecha_hora, observaciones, modo_kiosco)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_movimiento) DO NOTHING
            ''', (row['id_movimiento'], row['id_articulo'], row['id_usuario'],
                  row['tipo'], row['cantidad'], row['fecha_hora'],
                  row['observaciones'], row['modo_kiosco']))
        except Exception as e:
            print(f"Error movimiento {row['id_movimiento']}: {e}")
            pg_conn.rollback()
            continue
    pg_conn.commit()
    print("Movimientos migrados")

    print("Migrando alertas...")
    sqlite_cur.execute("SELECT * FROM alertas")
    for row in sqlite_cur.fetchall():
        try:
            pg_cur.execute('''
                INSERT INTO alertas (id_alerta, id_articulo, tipo_alerta, fecha_hora, vista, resuelta, id_usuario_dest)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_alerta) DO NOTHING
            ''', (row['id_alerta'], row['id_articulo'], row['tipo_alerta'],
                  row['fecha_hora'], row['vista'], row['resuelta'], row['id_usuario_dest']))
        except Exception as e:
            print(f"Error alerta {row['id_alerta']}: {e}")
            pg_conn.rollback()
            continue
    pg_conn.commit()
    print("Alertas migradas")

    # Actualizar secuencias
    print("Actualizando secuencias...")
    tablas = ['proveedores', 'usuarios', 'articulos', 'movimientos', 'alertas', 'ordenes_compra']
    ids = ['id_proveedor', 'id_usuario', 'id_articulo', 'id_movimiento', 'id_alerta', 'id_orden']
    for tabla, id_col in zip(tablas, ids):
        try:
            pg_cur.execute(f"SELECT setval(pg_get_serial_sequence('{tabla}', '{id_col}'), COALESCE((SELECT MAX({id_col}) FROM {tabla}), 1))")
        except Exception as e:
            print(f"Error secuencia {tabla}: {e}")
            pg_conn.rollback()
    pg_conn.commit()

    sqlite_conn.close()
    pg_conn.close()
    print("\n✅ Migración completada exitosamente!")

if __name__ == "__main__":
    migrar()