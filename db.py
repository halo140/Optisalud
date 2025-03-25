# db.py
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="optisalud.com",       # Cambia por tu host
        user="optisalud_power",      # Cambia por tu usuario de MySQL
        password="19rcg}8BA-Ph", # Cambia por tu contraseña
        database="optisalud_PowerBi"  # Cambia por el nombre de tu base de datos
    )
    return connection
