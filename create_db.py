import mysql.connector

baseDatos = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "password",
    )

cur = baseDatos.cursor()

#cur.execute("CREATE DATABASE appdmc_mysql")

cur.execute("SHOW DATABASES")

#db es el inicializador del database: db = SQLAlchemy(app)
for db in cur:
    print(db)