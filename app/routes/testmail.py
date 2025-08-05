from flask import Blueprint, current_app
from flask_mail import Message
from app import mail
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash

bp = Blueprint('testmail', __name__)

@bp.route('/testmail', methods=['GET', 'POST'])
@login_required
def test_mail():
    if request.method == 'POST':
        destinatario = request.form['email']
        asunto = 'Prueba de correo Flask-Mail'
        cuerpo = '¡Este es un correo de prueba enviado desde tu app Flask!'
        msg = Message(asunto, recipients=[destinatario])
        msg.body = cuerpo
        mail.send(msg)
        flash('Correo de prueba enviado a ' + destinatario, 'success')
        return redirect(url_for('testmail.test_mail'))
    return render_template('testmail/testmail.html')
