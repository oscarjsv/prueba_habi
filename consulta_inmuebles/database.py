import os
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def connect_to_database():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_SCHEMA")
        )
        return conexion
    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return None
