import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abelpro",
    database="absensi_karyawan"
)

cursor = db.cursor()