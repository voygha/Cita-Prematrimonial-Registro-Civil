import smtplib
from decouple import  config

subject= 'Cita Agendada'
message = 'Buen dia '

persona= 'Luis'
me1= 'su cita fue agendada para: '
fecha= '10/03/2021'
me2= 'A las: '
hora='10 am'

message= 'Subject:{}\n\n{}{}\n{}{}\n{}{}'.format(subject,message,persona,me1,fecha,me2,hora)

server= smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('mycorreo@gmail.com','mycontraseña')

#Primer argumento, quien envia el correo
#Segundo argumento quien recibe
#tercer argumento el mensaje
server.sendmail('mycorreo@gmail.com','destinatario@gmail.com',message)
server.quit()
print("Correo Enviado Exitosamente!!!")