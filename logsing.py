from basico import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.simple import PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base

#base = declarative_base() #enconjunta todas las db?
#Model funciona como función declarativa

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
#MODELOS DATABASE REPORTE
#
#Registro del Sujeto

class subjectForm(db.Model):
    __tablename__    = 'subject_reported'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nombre = db.Column(db.String(32), nullable=False)
    apellidos = db.Column(db.String(64), nullable=False)
    rut = db.Column(db.String(12), nullable=False)

#REPORTE LIST
class reportForm(db.Model):
    __tablename__    = 'report_form'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject_reported.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    local = db.Column(db.String(128), nullable=True)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)
    motivo_salida = db.Column(db.String(500), nullable=False)
    satisfaccion = db.Column(db.String(500), nullable=False)
    recomendacion = db.Column(db.String(500), nullable=False)
    comentarios = db.Column(db.String(500), nullable=False)
    
    subject = db.relationship(subjectForm)



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
    clave_hash2 = PasswordField("Confirmar Contraseña", validators = [DataRequired()])
    completar = SubmitField("Completar")
#
#FORM CLASS - #Inicio de Sesión
#
class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    clave_hash = PasswordField('Contraseña', validators=[DataRequired()])
    completar = SubmitField("Iniciar Sesión")