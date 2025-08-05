from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.core import Usuario
from werkzeug.security import generate_password_hash

bp = Blueprint('register', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nameUser']
        email = request.form.get('email')
        password = request.form['passwordUser']
        rol = request.form.get('role', 'cliente')

        # Validar campos obligatorios
        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('register.register'))

        if Usuario.query.filter((Usuario.nombre==nombre)|(Usuario.email==email)).first():
            flash('El usuario o email ya existe.', 'danger')
            return redirect(url_for('register.register'))

        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password, rol=rol, estado='activo')
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
