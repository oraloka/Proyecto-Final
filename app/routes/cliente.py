from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.core import Producto, Pedido, DetallePedido, Factura
from app import db

bp = Blueprint('cliente', __name__)

@bp.route('/cliente')
@login_required
def cliente_dashboard():
    if current_user.rol != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    # Búsqueda y filtro
    q = request.args.get('q', '').strip()
    tipo = request.args.get('tipo', '').strip()
    productos_query = Producto.query
    if q:
        productos_query = productos_query.filter(Producto.nombre.ilike(f"%{q}%"))
    if tipo:
        productos_query = productos_query.filter(Producto.tipo == tipo)
    productos = productos_query.all()
    # Para el filtro: obtener todos los tipos únicos
    tipos = [row[0] for row in db.session.query(Producto.tipo).distinct().all()]
    pedidos = Pedido.query.filter_by(id_cliente=current_user.id).all()
    facturas = Factura.query.join(Pedido).filter(Pedido.id_cliente==current_user.id).all()
    return render_template('cliente/dashboard.html', productos=productos, pedidos=pedidos, facturas=facturas, tipos=tipos, q=q, tipo_seleccionado=tipo)


# --- CARRITO ACUMULATIVO ---
@bp.route('/cliente/realizar_pedido', methods=['POST'])
@login_required
def realizar_pedido():
    if current_user.rol != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad', 1))
    producto = Producto.query.get(producto_id)
    if not producto or producto.stock < cantidad:
        flash('Producto no disponible o stock insuficiente.', 'danger')
        return redirect(url_for('cliente.cliente_dashboard'))

    # Buscar pedido pendiente (carrito) del usuario
    pedido = Pedido.query.filter_by(id_cliente=current_user.id, estado='pendiente').first()
    if not pedido:
        pedido = Pedido(id_cliente=current_user.id, estado='pendiente')
        db.session.add(pedido)
        db.session.commit()

    # Verificar si el producto ya está en el carrito
    detalle = DetallePedido.query.filter_by(id_pedido=pedido.id, id_producto=producto.id).first()
    if detalle:
        detalle.cantidad += cantidad
    else:
        detalle = DetallePedido(id_pedido=pedido.id, id_producto=producto.id, cantidad=cantidad, precio_unitario=producto.precio)
        db.session.add(detalle)

    # Disminuir stock y alerta si llega a 10
    producto.stock -= cantidad
    db.session.commit()

    # Alerta si stock <= 10
    if producto.stock == 10:
        from app.utils.notificaciones import enviar_notificacion_email
        from app.models.core import Usuario, Notificacion
        admins = Usuario.query.filter_by(rol='admin').all()
        vendedores = Usuario.query.filter_by(rol='vendedor').all()
        emails = [u.email for u in admins + vendedores if u.email]
        for email in emails:
            enviar_notificacion_email(
                email,
                f'Alerta de stock bajo: {producto.nombre}',
                f'El producto "{producto.nombre}" ha alcanzado un stock de 10 unidades.'
            )
        # Notificación visual
        for user in admins + vendedores:
            notif = Notificacion(
                id_usuario=user.id,
                mensaje=f'Alerta: El producto "{producto.nombre}" tiene solo 10 unidades en stock.',
            )
            db.session.add(notif)
        db.session.commit()

    flash('Producto agregado al carrito.', 'success')
    return redirect(url_for('cliente.cliente_dashboard'))

# --- VISTA DEL CARRITO ---
@bp.route('/cliente/carrito')
@login_required
def ver_carrito():
    if current_user.rol != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    pedido = Pedido.query.filter_by(id_cliente=current_user.id, estado='pendiente').first()
    carrito = []
    total = 0
    if pedido:
        for item in pedido.detalles:
            carrito.append({'producto': item.producto, 'cantidad': item.cantidad})
            total += item.cantidad * item.precio_unitario
    return render_template('cliente/carrito.html', carrito=carrito, total=total)

# --- QUITAR PRODUCTO DEL CARRITO ---
@bp.route('/cliente/carrito/quitar/<int:producto_id>')
@login_required
def quitar_del_carrito(producto_id):
    if current_user.rol != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    pedido = Pedido.query.filter_by(id_cliente=current_user.id, estado='pendiente').first()
    if not pedido:
        return redirect(url_for('cliente.ver_carrito'))
    detalle = DetallePedido.query.filter_by(id_pedido=pedido.id, id_producto=producto_id).first()
    if detalle:
        db.session.delete(detalle)
        db.session.commit()
    return redirect(url_for('cliente.ver_carrito'))

# --- CONFIRMAR PEDIDO ---
@bp.route('/cliente/carrito/confirmar', methods=['POST'])
@login_required
def confirmar_pedido():
    if current_user.rol != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    pedido = Pedido.query.filter_by(id_cliente=current_user.id, estado='pendiente').first()
    if not pedido or not pedido.detalles:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('cliente.ver_carrito'))
    pedido.estado = 'confirmado'
    db.session.commit()
    flash('¡Pedido confirmado! Espera la aprobación.', 'success')
    return redirect(url_for('cliente.cliente_dashboard'))

@bp.route('/cliente/factura/<int:factura_id>')
@login_required
def ver_factura(factura_id):
    if current_user.rol != 'cliente':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    factura = Factura.query.get_or_404(factura_id)
    return render_template('cliente/factura.html', factura=factura)
