#                   #
# Made by Naizajar  #
#                   #
from werkzeug.security import generate_password_hash
from basico import app, db
from singup import registerForm, users
from flask import Flask, render_template, flash

#
#ROOT
#
@app.route('/') #PRINCIPAL 
def index(): #de la 'def' se piden los datos de la forma {{ url_for('nombreVar')}} en las templates(html) 
    flash("Aplicación en desarrollo - Version 0.4")
    return render_template('index.html')



#
#SINGUP
#
@app.route('/usuario/singup', methods = ['GET', 'POST'])
def singUp():
    forma = registerForm()
    usuario = ''
    nombre = ''
    apellidos = ''
    email = ''
    
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