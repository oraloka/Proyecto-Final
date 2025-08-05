from flask import Blueprint, render_template, redirect, url_for
from app.models.core import Producto

bp = Blueprint('publico', __name__)

@bp.route('/')
def home():
    from flask_login import current_user
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Redirigir a dashboard según rol
        if getattr(current_user, 'rol', None) == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif getattr(current_user, 'rol', None) == 'cliente':
            return redirect(url_for('cliente.cliente_dashboard'))
        elif getattr(current_user, 'rol', None) == 'proveedor':
            return redirect(url_for('proveedor.proveedor_dashboard'))
        elif getattr(current_user, 'rol', None) == 'vendedor':
            return redirect(url_for('vendedor.vendedor_dashboard'))
    productos = Producto.query.filter_by(aprobado=True).all()
    return render_template('publico/catalogo_publico.html', productos=productos)

@bp.route('/hacer_pedido')
def hacer_pedido():
    return redirect(url_for('auth.login'))
