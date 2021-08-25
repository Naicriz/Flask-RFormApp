from typing import Text
from wtforms.fields.core import DateField
from basico import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.simple import PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.widgets import TextArea
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base

#base = declarative_base() #enconjunta todas las db?
#Model funciona como función declarativa

#
#MODELO DATABASE USUARIO
#
class users(db.Model, UserMixin):
    __tablename__    = 'user_form'
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

class subjects(db.Model):
    __tablename__    = 'subject_form'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_form.id'))
    nombre = db.Column(db.String(32), nullable=False)
    apellidos = db.Column(db.String(64), nullable=False)
    rut = db.Column(db.String(10), nullable=False)

#REPORTE LIST
class reports(db.Model):
    __tablename__    = 'report_form'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_form.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject_form.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    local = db.Column(db.String(128), nullable=True)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)
    motivo_salida = db.Column(db.String(500), nullable=False)
    satisfaccion = db.Column(db.Integer, nullable=False)
    recomendacion = db.Column(db.String(500), nullable=False)
    comentarios = db.Column(db.String(500), nullable=False)
    
    subject = db.relationship(subjects)




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
    
#
#FORM CLASS - #Registrar sujeto
#
class subjectForm(FlaskForm):
    nombre = StringField("Nombre", validators = [DataRequired()])
    apellidos = StringField("Apellidos", validators = [DataRequired()])
    rut = PasswordField("Rut", validators = [DataRequired()])
    completar = SubmitField("Confirmar Datos")

#
#FORM CLASS - #Reporte de sujeto
#
class reportForm(FlaskForm):
    local = StringField("Local de trabajo", validators = [DataRequired()])
    fecha_ingreso = DateField("Fecha de ingreso laboral", format='%Y-%m-%d', validators = [DataRequired()])
    fecha_salida = DateField("Fecha de salida laboral", format='%Y-%m-%d', validators = [DataRequired()])
    motivo_salida = StringField("Motivo de salida", validators = [DataRequired()])
    satisfaccion = StringField("Satisfacción 1 a 10", validators = [DataRequired()])
    recomendacion = StringField("¿Se recomienda?", validators = [DataRequired()])
    comentarios = StringField("Comentarios", widget=TextArea(), validators = [DataRequired()])
    completar = SubmitField("Confirmar Datos")