from basico import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.simple import PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#
#MODELO DATABASE USUARIO
#
class users(db.Model, UserMixin):
    __tablename__    = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    nombre = db.Column(db.String(32), nullable=False)
    apellidos = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(125), nullable=False, unique=True)
    clave_hash = db.Column(db.String(128))

    #Creación de Contraseña
    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo legible.')
    
    @password.setter
    def password(self, password):
        self.clave_hash = generate_password_hash(password)
    def verifyPassword(self, password):
        return check_password_hash(self.clave_hash, password)
    
    def __repr__(self):
        return '<usersusuarios %r>' % self.nombre



#
#FORM CLASS - #Registro de Usuario
#
class userForm(FlaskForm):
    nombre = StringField("Nombre", validators = [DataRequired()])
    apellidos = StringField("Apellidos", validators = [DataRequired()])
    email = StringField("E-mail", validators = [DataRequired()])
    clave_hash = PasswordField("Contraseña", validators = [DataRequired(),
                                EqualTo('clave_hash2',
                                message='Las contraseñas deben coincidir.')])
    clave_hash2 = PasswordField("Confirmar contraseña", validators = [DataRequired()])
    completar = SubmitField("Completar")



#
#FORM CLASS - #Inicio de Sesión
#
class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    clave_hash = PasswordField('Contraseña', validators=[DataRequired()])
    completar = SubmitField("Iniciar Sesión")