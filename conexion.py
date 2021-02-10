import mysql.connector as sql
db= sql.connect(host="localhost",user="root",passwd="12345",database="registro_civil")



#Objetopara ejecutar ordenes
cursor = db.cursor()

#Almacena los resultados en cursos
#El punto execute es para ejecutar sql
#cursor.execute("SELECT * FROM clientes")
#consulta= cursor.fetchall()
#print(consulta)

#BORRAR UN REGISTRO EN LA BASE DE DATOS
#cursor.execute("DELETE FROM clientes where id_cliente=3")

sql="insert into clientes(nombre, curp,direccion,telefono,correo) values (%s, %s, %s, %s, %s)"
datos=("Sandra Luz Alvarado Hernandez","SAAL990310HCSSLS03","1 sur poniente 145 Francisco I Madero","9612315736","saan@gmail.com")
cursor.execute(sql, datos)
db.commit()


# Prepare SQL query to READ a record into the database.
#sql = "SELECT * FROM clientes  \

db.close()