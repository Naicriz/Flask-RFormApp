from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#
#INSTANCIA DE FLASK
#
app = Flask(__name__)
app.config['SECRET_KEY'] = "superultraclavesecreta"



#
#DATABASE
#
# En caso de querer probar con sqlite.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdmc-sql.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/appdmc_mysql'
#Inicializar Database
db = SQLAlchemy(app)