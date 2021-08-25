from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
#
#INSTANCIA DE FLASK
#
app = Flask(__name__)
app.config['SECRET_KEY'] = "superultraclavesecreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'logIn'

#
#DATABASE
#
# En caso de querer probar con sqlite.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdmc-sql.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/appdmc_mysql'
#Inicializar Database
db = SQLAlchemy(app)
#migrar el app al db
migrate = Migrate(app, db) 