from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.core import Producto, Pedido
from app import db

bp = Blueprint('vendedor', __name__)

@bp.route('/vendedor')
@login_required
def vendedor_dashboard():
    if current_user.rol != 'vendedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    productos = Producto.query.filter_by(aprobado=True).all()
    pedidos = Pedido.query.all()
    return render_template('vendedor/dashboard.html', productos=productos, pedidos=pedidos)

@bp.route('/vendedor/aceptar_pedido/<int:pedido_id>')
@login_required
def aceptar_pedido(pedido_id):
    if current_user.rol != 'vendedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'aceptado'
    db.session.commit()
    flash('Pedido aceptado.', 'success')
    # Notificar al cliente
    return redirect(url_for('vendedor.vendedor_dashboard'))

@bp.route('/vendedor/solicitar_stock', methods=['POST'])
@login_required
def solicitar_stock():
    if current_user.rol != 'vendedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    # Lógica para solicitar a proveedor lo que falta
    flash('Solicitud enviada al proveedor.', 'success')
    return redirect(url_for('vendedor.vendedor_dashboard'))
