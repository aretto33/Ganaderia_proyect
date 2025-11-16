import mariadb

def conectar_bd():
    try: 
        conn= mariadb.connect(
        host='localhost',
        user='AdminGanaderia',
        password='2025',
        database='Proyecto_Ganaderia'
        )
        cursor = conn.cursor()
        print("Conexión exitosa")
    except mariadb.Error as e:
        print(f"Error al conectar con MariaDB: {e}") 
    return None, None

