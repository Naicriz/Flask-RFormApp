#                   #
# Made by Naizajar  #
#                   #
from werkzeug.security import check_password_hash, generate_password_hash
from basico import db, app, login_manager
from logsing import userForm, loginForm, users
from flask import Flask, render_template, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#
#ROOT
#
@app.route('/') #PRINCIPAL 
def index(): #de la 'def' se piden los datos de la forma {{ url_for('nombreVar')}} en las templates(html) 
    flash("Aplicación en desarrollo - Version 0.6")
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
#LOGIN
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
#NEW REPORT
#
@app.route('/reportes/newreport')
def newReport():
    return render_template('newreport.html')



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