from flask import Flask
from flask import render_template, request,redirect,url_for,flash
from flaskext.mysql import MySQL
import smtplib
from decouple import  config

#se crea la aplicacion
app= Flask(__name__)

#LLAVE SECRETA
app.secret_key="Luis"

mysql=MySQL()
#DEfinen todas las configuraciones iniciales de MYSQL
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='12345'
app.config['MYSQL_DATABASE_DB']='registro_civil'
#Se crea la conexion
mysql.init_app(app)


#AQUI ES PARA TRABAJAR EN EL INDEX
#recibe soclicitudes mediante la url
@app.route('/')
def index():
    sql="SELECT * FROM clientes"
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql)
    clientes=cursor.fetchall()
    #print(clientes)
    conn.commit()
    #se le pasa el parametro declientes
    return render_template('clientes/indexclientes.html', clientes=clientes)
#AQUI TERMINA INDEX

#AQUI ES PARA TRABAJAR EN EL DE CITAS
#recibe soclicitudes mediante la url
@app.route('/cita')
def cita():
    sql="SELECT * FROM cita"
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql)
    citas=cursor.fetchall()
    #print(clientes)
    conn.commit()
    #se le pasa el parametro declientes
    return render_template('clientes/citas.html', citas=citas)
#AQUI TERMINA CITAS

#AQUI ES PARA TRABAJAR EN EL HISTORICO
#recibe soclicitudes mediante la url
@app.route('/registro')
def registro():
    sql="SELECT * FROM registro"
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql)
    registros=cursor.fetchall()
    #print(clientes)
    conn.commit()
    #se le pasa el parametro declientes
    return render_template('clientes/historico.html', registros=registros)
#AQUI TERMINA HISTORICO


#ELIMINAR REGISTROS DE CLIENTES
@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s",(id))
    conn.commit()
    return redirect('/')
#TERMINA ELIMINAR REGISTROS DE CLIENTES

#ELIMINAR REGISTROS DE CITAS
@app.route('/destroy1/<int:id>')
def destroy1(id):
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute("DELETE FROM cita WHERE id_cita=%s",(id))
    conn.commit()
    return redirect('/')
#TERMINA ELIMINAR REGISTROS DE CITAS


#EDITAR REGISTROS
@app.route('/edit/<int:id>')
def edit(id):  
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s",(id))
    clientes=cursor.fetchall()
    conn.commit() 
    return render_template('/clientes/edit.html', clientes=clientes)
#TERMINA EDITAR REGISTROS


#AQUI ES PARA AGREGAR UN NUEVO CLIENTE
@app.route('/create')
def create():
   return render_template('clientes/create.html')
#AQUI TERMINA


#CREAR NUEVO CLIENTE
#RECUPERAR DATOS DEL FORMULARIO Y GUARDARLO EN LA BASE DE DATOS
@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtnombre']
    _curp=request.form['txtcurp']
    _direccion=request.form['txtdireccion']
    _telefono=request.form['txttelefono']
    _correo=request.form['txtcorreo']

    if _nombre =='' or _curp =='' or _direccion =='' or _telefono =='' or _correo =='':
        flash('Recuerda Llenar Todos los Campos')
        return redirect(url_for('create'))

    sql="insert into clientes(nombre, curp,direccion,telefono,correo) values (%s, %s, %s, %s, %s)"
    datos=(_nombre,_curp,_direccion,_telefono,_correo)
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')
#TERMINA CREAR NUEVO CLIENTE  


#EDITAR REGISTROS
@app.route('/edit1/<int:id>')
def edit1(id):  
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s",(id))
    clientes=cursor.fetchall()
    conn.commit() 
    return render_template('/clientes/ncita.html', clientes=clientes)
#TERMINA EDITAR REGISTROS

#EDITAR REGISTROS
@app.route('/edit2/<int:id>')
def edit2(id):  
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM cita WHERE id_cita=%s",(id))
    citas=cursor.fetchall()
    conn.commit() 
    return render_template('/clientes/validar.html', citas=citas)
#TERMINA EDITAR REGISTROS




#CREAR NUEVA CITA
#RECUPERAR DATOS DEL FORMULARIO Y GUARDARLO EN LA BASE DE DATOS
@app.route('/store1', methods=['POST'])
def storage1():
    _fecha=request.form['txtfecha']
    _idcliente=request.form['txtid_cliente']
    _nombre=request.form['txtnombre']
    _correo=request.form['txtcorreo']
    _hora=request.form['txthora']

    if _fecha ==''or _idcliente =='' or _nombre =='' or  _correo =='' or _hora =='':
        flash('Recuerda Llenar Todos los Campos')
        return redirect(url_for('ncita'))

    #ENVIAR CORREO DE CONFIRMACION
    subject= 'REGISTRO DE CITA PREMATRIMONIAL - Cita Agendada'
    message = 'Buen dia '

    persona= _nombre
    me1= 'su cita fue agendada para: '
    fecha= _fecha
    me2= 'A las: '
    hora= _hora
    tex=' Hrs.'

    message= 'Subject:{}\n\n{}{}\n{}{}\n{}{}{}'.format(subject,message,persona,me1,fecha,me2,hora,tex)

    server= smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('luisinperrin10@gmail.com','luiscasta10')

    #Primer argumento, quien envia el correo
    #Segundo argumento quien recibe
    #tercer argumento el mensaje
    server.sendmail('luisinperrin10@gmail.com',_correo,message)
    server.quit()
    print("Correo Enviado Exitosamente!!!")

    sql="insert into cita(fecha,id_cliente,nombre,correo,hora) values (%s, %s, %s, %s, %s)"
    datos=(_fecha, _idcliente, _nombre,_correo,_hora)
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')
#TERMINA CREAR NUEVA CITA 



#VALIDAR UNA CITA
#RECUPERAR DATOS DEL FORMULARIO Y GUARDARLO EN LA BASE DE DATOS
@app.route('/store2', methods=['POST'])
def storage2():
    _idcita=request.form['txtid_cita']
    _fecha=request.form['txtfecha']
    _idcliente=request.form['txtid_cliente']
    _nombre=request.form['txtnombre']
    _correo=request.form['txtcorreo']
    _hora=request.form['txthora']

    if _idcita =='' or _fecha ==''or _idcliente =='' or _nombre =='' or  _correo =='' or _hora =='':
        flash('Recuerda Llenar Todos los Campos')
        return redirect(url_for('ncita'))


    sql="insert into registro(id_cita,fecha,id_cliente,nombre,correo,hora) values (%s,%s, %s, %s, %s, %s)"
    datos=(_idcita, _fecha, _idcliente, _nombre,_correo,_hora)
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')
#TERMINA VALIDAR NUEVA CITA 


#ACTUALIZAR DATOS DEL CLIENTE
@app.route('/update', methods=['POST'])
def update():
    #Recepcionamos los datos
    _nombre=request.form['txtnombre']
    _curp=request.form['txtcurp']
    _direccion=request.form['txtdireccion']
    _telefono=request.form['txttelefono']
    _correo=request.form['txtcorreo']
    id=request.form['txtid']
    sql="UPDATE clientes SET nombre=%s, curp=%s, direccion=%s, telefono=%s, correo=%s WHERE id_cliente=%s"
    datos=(_nombre,_curp,_direccion,_telefono,_correo,id)
    #Abre la conexion
    conn= mysql.connect()
    #Lugar  donde se almacena todo lo que se va a ejecutar
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

#TERMINA ACTUALIZAR DATOS DEL CLIENTE


if __name__=='__main__':
    app.run(debug=True)