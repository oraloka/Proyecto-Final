from flask_mail import Message
from flask import current_app
from app import mail

def enviar_notificacion_email(destinatario, asunto, cuerpo):
    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo
    mail.send(msg)

# Ejemplo de uso:
# enviar_notificacion_email('cliente@email.com', 'Pedido aceptado', 'Tu pedido ha sido aceptado por el administrador.')
