#                   #
# Made by Naizajar  #
#                   #
from werkzeug.security import check_password_hash, generate_password_hash
from basico import db, app, login_manager
from modelos import users, subjects, reports, userForm, loginForm, subjectForm, reportForm
from flask import Flask, render_template, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.orm import relationship
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#
#ROOT
#
@app.route('/') #PRINCIPAL 
def index(): #de la 'def' se piden los datos de la forma {{ url_for('nombreVar')}} en las templates(html) 
    flash("Aplicación en desarrollo - Version 1.0")
    return render_template('index.html')



#
#SINGUP
#
@app.route('/singup', methods = ['GET', 'POST'])
def singUp():
    forma = userForm()
    usuario = None
    nombre = None
    apellidos = None
    email = None
    
    #Validación para la forma
    if forma.validate_on_submit():
        usuario = users.query.filter_by(email=forma.email.data).first() #variable 'email' proveniente de "class registerForm(): en registro.py"
        if usuario is None:
            clave_hashed = generate_password_hash(forma.clave_hash.data, "sha256")
            usuario = users(nombre = forma.nombre.data,
                            apellidos = forma.apellidos.data,
                            email = forma.email.data,
                            clave_hash = clave_hashed)
            db.session.add(usuario) #se añaden los datos asignados a la var 'usuarios'
            db.session.commit()
        
        nombre = forma.nombre.data
        apellidos = forma.apellidos.data
        email = forma.email.data

        forma.nombre.data = ''
        forma.apellidos.data = ''
        forma.email.data = ''
        forma.clave_hash.data = ''
        flash("¡Tu cuenta ha sido creada exitosamente!")
    
    lista_usuarios = users.query.order_by(users.fecha_creacion)
    return render_template('singup.html', nombre = nombre,
                           apellidos = apellidos,
                           email = email,
                           forma = forma,
                           lista_usuarios = lista_usuarios)



@login_manager.user_loader
def loadUser(usuario_id):
    return users.query.get(int(usuario_id))



#
#LOGIN - TEST SIN CONECTAR (AUN NO LOGUEA DE POR SI)
#
@app.route('/login', methods = ['GET', 'POST'])
def logIn():
    forma = loginForm()
    email = None
    clave = None
    clave_check = None
    valido = None
    
    if forma.validate_on_submit():
        email = forma.email.data
        clave = forma.clave_hash.data
        #Limpiar forma
        forma.email.data = ''
        forma.clave_hash.data = ''
        
        #Lookup por Email
        clave_check = users.query.filter_by(email=email).first()
        
        #Check hashed password
        valido = check_password_hash(clave_check.clave_hash, clave)

    return render_template('login.html',
                           email = email,
                           clave = clave,
                           clave_check = clave_check,
                           valido = valido,
                           forma = forma)
    
    

#
#DASHBOARD
#
#@login_required
#@app.route('/dashboard', methods = ['GET', 'POST'])
#def dashboard():
#    flash("¡Debes iniciar sesión primero!")
#    return render_template('dashboard.html')
    
  
  
  
  
#
#REPORTES NEW REPORT
#  
@app.route('/reportes/newreport', methods=['GET', 'POST'])
def newReport():
    forma_s = subjectForm()
    forma_r = reportForm()
    
    return render_template('newreport.html',
                           forma_s=forma_s, forma_r=forma_r)
#
#ADD SUBJECT
#
@app.route('/reportes/addsubject', methods=['GET', 'POST'])
def addSubject():  
    forma_s = subjectForm()
    forma_r = reportForm()
    nombre = None
    apellidos = None
    rut = None
    #Validación para la forma #### NO RECIBE DATOS LA FORMA DE AÑADIR SUJETO (AÚN)
    if forma_s.validate_on_submit():
        sujeto = subjects(nombre = forma_s.nombre.data,
                          apellidos = forma_s.apellidos.data,
                          rut = forma_s.rut.data)
        #Limpiar forma
        forma_s.nombre.data = ''
        forma_s.apellidos.data = ''
        forma_s.rut.data = ''
        #enviar a database
        db.session.add(sujeto)
        db.session.commit()
        flash("¡Sujeto creado exitosamente!")
    return render_template('newreport.html',
                           nombre=nombre,
                           apellidos=apellidos,
                           rut=rut,
                           forma_s=forma_s, forma_r=forma_r)
    
    
    
#
#ADD REPORT
#
@app.route('/reportes/addreport', methods=['GET', 'POST'])
def addReport():    
    forma_r = reportForm()
    forma_s = subjectForm()
    local = None
    fecha_ingreso = None
    fecha_salida = None
    motivo_salida = None
    satisfaccion = None
    recomendacion = None
    comentarios = None
    #Validación para la forma
    if forma_r.validate_on_submit():
        reporte = reports(local = forma_r.local.data,
                          fecha_ingreso = forma_r.fecha_ingreso.data,
                          fecha_salida = forma_r.fecha_salida.data,
                          motivo_salida = forma_r.motivo_salida.data,
                          satisfaccion = forma_r.satisfaccion.data,
                          recomendacion = forma_r.recomendacion.data,
                          comentarios = forma_r.recomendacion.data)
        #Limpiar forma
        forma_r.local.data = ''
        forma_r.fecha_ingreso.data = ''
        forma_r.fecha_salida.data = ''
        forma_r.motivo_salida.data = ''
        forma_r.satisfaccion.data = ''
        forma_r.recomendacion.data = ''
        forma_r.comentarios.data = ''
        #enviar a database
        db.session.add(reporte)
        db.session.commit()
        flash("¡Reporte creado exitosamente!")
    return render_template('newreport.html', local=local,
                           fecha_ingreso=fecha_ingreso,
                           fecha_salida=fecha_salida,
                           motivo_salida=motivo_salida,
                           satisfaccion=satisfaccion,
                           recomendacion=recomendacion,
                           comentarios=comentarios,
                           forma_s=forma_s, forma_r=forma_r)



#
#LISTA REPORTES
#
@app.route('/reportes/reportsall', methods=['GET', 'POST'])
def reportsAll():
    subjects_todo = subjects()
    reports_todo = reports()
    lista_reportes = reports.query.order_by(reports.fecha_creacion)
    return render_template('reportsall.html',
                           lista_reportes = lista_reportes)
    
    
    
    
    
    
#
#ERRORES CUSTOM DE PÁGINAS
#
#URL Inválido
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
#Error Interno Servidor
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500