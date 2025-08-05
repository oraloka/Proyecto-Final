
# --- IMPORTS Y BLUEPRINT AL INICIO ---
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.core import Usuario, Pedido, EnvioProveedor, Factura
from app import db
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__)

# --- AGREGAR PRODUCTO (stock 100 por defecto, editable por proveedor) ---
@bp.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    from app.models.core import Usuario, Producto
    proveedores = Usuario.query.filter_by(rol='proveedor').all()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock']) if request.form['stock'] else 100
        id_proveedor = int(request.form['id_proveedor']) if request.form['id_proveedor'] else None
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, id_proveedor=id_proveedor)
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/nuevo_producto.html', proveedores=proveedores)

# --- CRUD USUARIOS ---
@bp.route('/admin/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        rol = request.form['rol']
        estado = request.form['estado']
        password = request.form['password']
        if not password:
            flash('La contraseña es obligatoria.', 'danger')
            return render_template('admin/usuario_form.html', usuario=None)
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'danger')
            return render_template('admin/usuario_form.html', usuario=None)
        usuario = Usuario(
            nombre=nombre,
            email=email,
            rol=rol,
            estado=estado,
            password=generate_password_hash(password)
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/usuario_form.html', usuario=None)

@bp.route('/admin/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']
        usuario.rol = request.form['rol']
        usuario.estado = request.form['estado']
        password = request.form['password']
        if password:
            usuario.password = generate_password_hash(password)
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/usuario_form.html', usuario=usuario)

@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    filtro = request.args.get('filtro', '').strip()
    rol_filtro = request.args.get('rol', '').strip()
    pedidos = Pedido.query.all()
    envios = EnvioProveedor.query.all()
    estado_filtro = request.args.get('estado', '').strip()
    query = Usuario.query
    if filtro:
        query = query.filter(Usuario.nombre.ilike(f'%{filtro}%'))
    if rol_filtro:
        query = query.filter(Usuario.rol == rol_filtro)
    if estado_filtro:
        query = query.filter(Usuario.estado == estado_filtro)
    usuarios = query.all()
    return render_template('admin/dashboard.html', pedidos=pedidos, envios=envios, usuarios=usuarios, filtro=filtro, rol_filtro=rol_filtro, estado_filtro=estado_filtro)

@bp.route('/admin/aceptar_pedido/<int:pedido_id>')
@login_required
def aceptar_pedido(pedido_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'aceptado'
    db.session.commit()
    flash('Pedido aceptado.', 'success')
    # Notificar al cliente por email
    from app.utils.notificaciones import enviar_notificacion_email
    if pedido.cliente and pedido.cliente.email:
        enviar_notificacion_email(
            pedido.cliente.email,
            'Pedido aceptado',
            f'Tu pedido #{pedido.id} ha sido aceptado. Pronto recibirás tu factura.'
        )
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/rechazar_pedido/<int:pedido_id>')
@login_required
def rechazar_pedido(pedido_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'rechazado'
    db.session.commit()
    flash('Pedido rechazado.', 'warning')
    # Notificar al cliente por email
    from app.utils.notificaciones import enviar_notificacion_email
    if pedido.cliente and pedido.cliente.email:
        enviar_notificacion_email(
            pedido.cliente.email,
            'Pedido rechazado',
            f'Tu pedido #{pedido.id} ha sido rechazado. Consulta con el administrador.'
        )
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/envios', methods=['GET'])
@login_required
def admin_envios():
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    from app.models.core import EnvioProveedor
    envios = EnvioProveedor.query.order_by(EnvioProveedor.fecha.desc()).all()
    return render_template('admin/envios.html', envios=envios)

@bp.route('/admin/aceptar_envio/<int:envio_id>')
@login_required
def aceptar_envio(envio_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    from app.models.core import EnvioProveedor, Producto, Usuario
    from app.utils.notificaciones import enviar_notificacion_email
    envio = EnvioProveedor.query.get_or_404(envio_id)
    envio.estado = 'aceptado'
    # Sumar stock al producto
    producto = Producto.query.get(envio.id_producto)
    if producto:
        producto.stock += envio.cantidad
    # Notificar por email al proveedor
    proveedor = Usuario.query.get(envio.id_proveedor)
    if proveedor and proveedor.email:
        enviar_notificacion_email(
            proveedor.email,
            'Envío aceptado',
            f'Su envío de {envio.cantidad} unidades del producto "{producto.nombre if producto else ''}" ha sido aceptado y el stock ha sido actualizado.'
        )
    db.session.commit()
    flash('Envío aceptado y stock actualizado.', 'success')
    return redirect(url_for('admin.admin_envios'))

@bp.route('/admin/rechazar_envio/<int:envio_id>')
@login_required
def rechazar_envio(envio_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    from app.models.core import EnvioProveedor
    envio = EnvioProveedor.query.get_or_404(envio_id)
    envio.estado = 'rechazado'
    db.session.commit()
    flash('Envío rechazado.', 'warning')
    return redirect(url_for('admin.admin_envios'))

@bp.route('/admin/eliminar_usuario/<int:usuario_id>')
@login_required
def eliminar_usuario(usuario_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado.', 'info')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/bloquear_usuario/<int:usuario_id>')
@login_required
def bloquear_usuario(usuario_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.estado = 'bloqueado'
    db.session.commit()
    flash('Usuario bloqueado.', 'warning')
    # Notificar al usuario por email si es necesario
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/desbloquear_usuario/<int:usuario_id>')
@login_required
def desbloquear_usuario(usuario_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.estado = 'activo'
    db.session.commit()
    flash('Usuario desbloqueado.', 'success')
    # Notificar al usuario por email si es necesario
    return redirect(url_for('admin.admin_dashboard'))
