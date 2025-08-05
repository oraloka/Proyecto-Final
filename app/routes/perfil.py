from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.core import Usuario
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('perfil', __name__)

@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    usuario = Usuario.query.get(current_user.id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']
        if request.form['password']:
            usuario.password = generate_password_hash(request.form['password'])
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('perfil.perfil'))
    return render_template('perfil/perfil.html', usuario=usuario)
