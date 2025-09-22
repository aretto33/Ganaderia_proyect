#Conección de maria db usando python, si no deja instala el módulo en la terminal...usa pip install mariadb

import mariadb

try: 
    coneccion = mariadb.connect(
    host='localhost',
    user='arletteg',
    password='123456',
    database='Proyecto_Ganaderia'
    )
    cursor = coneccion.cursor()
    print("Coneccion exitosa")
except mariadb.Error as e:
    print(f"Error al conectar con MariaDB: {e}")



