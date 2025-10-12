import mariadb

try: 
    conn= mariadb.connect(
    host='localhost',
    user='arletteg',
    password='123456',
    database='Proyecto_Ganaderia'
    )
    cursor = conn.cursor()
    print("Conexión exitosa")
except mariadb.Error as e:
    print(f"Error al conectar con MariaDB: {e}") 