import mysql.connector


def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host="3.138.156.32",
            port="3309",
            user="pruebas",
            password="VGbt3Day5R",
            database="habi_db"
        )
        print("Conexión a la base de datos exitosa")
        return conexion
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
        return None

# host: 3.138.156.32
# port: 3309
# user: pruebas
# pass: VGbt3Day5R
# schema: habi_db
