from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.core import Usuario
from app.models.core import Usuario

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']
        # Buscar usuario por nombre o email
        user = Usuario.query.filter((Usuario.nombre==nameUser)|(Usuario.email==nameUser)).first()
        if user:
            if user.estado != 'activo':
                flash('Usuario bloqueado. Contacte al administrador.', 'danger')
                return redirect(url_for('auth.login'))
            from werkzeug.security import check_password_hash
            if check_password_hash(user.password, passwordUser):
                login_user(user)
                flash("Bienvenido, {}!".format(user.nombre), "success")
                # Redirigir según rol
                if user.rol == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))
                elif user.rol == 'cliente':
                    return redirect(url_for('cliente.cliente_dashboard'))
                elif user.rol == 'proveedor':
                    return redirect(url_for('proveedor.proveedor_dashboard'))
                elif user.rol == 'vendedor':
                    return redirect(url_for('vendedor.vendedor_dashboard'))
                else:
                    return redirect(url_for('auth.dashboard'))
        flash('Credenciales inválidas.', 'danger')
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template("login.html")

@bp.route('/dashboard')
@login_required
def dashboard():
    # Redirige siempre al panel correcto según el rol
    if current_user.rol == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    elif current_user.rol == 'cliente':
        return redirect(url_for('cliente.cliente_dashboard'))
    elif current_user.rol == 'proveedor':
        return redirect(url_for('proveedor.proveedor_dashboard'))
    elif current_user.rol == 'vendedor':
        return redirect(url_for('vendedor.vendedor_dashboard'))
    else:
        return render_template('error.html'), 403

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
