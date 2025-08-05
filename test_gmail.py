import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'cajlpj@gmail.com'
smtp_password = 'hkqf aeom tsoa mvfd'  # App Password

# Cambia esto por el destinatario que quieras probar
to_email = 'cajlpj@gmail.com'

msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = to_email
msg['Subject'] = 'Prueba SMTP directa desde Python'
msg.attach(MIMEText('Este es un correo de prueba enviado directamente con smtplib.', 'plain'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, to_email, msg.as_string())
    server.quit()
    print('Correo enviado correctamente a', to_email)
except Exception as e:
    print('Error al enviar correo:', e)
