from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from flask_login import login_required, current_user
from app.models.core import EnvioProveedor, Factura, Producto
from app import db

bp = Blueprint('proveedor', __name__)

@bp.route('/proveedor')
@login_required
def proveedor_dashboard():
    if current_user.rol != 'proveedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    envios = EnvioProveedor.query.filter_by(id_proveedor=current_user.id).all()
    facturas = Factura.query.all()  # Mostrar solo las relevantes si se requiere
    from app.models.core import Producto
    productos = Producto.query.filter_by(id_proveedor=current_user.id).all()
    return render_template('proveedor/dashboard.html', envios=envios, facturas=facturas, productos=productos)

@bp.route('/proveedor/entregar_envio', methods=['POST'])
@login_required
def entregar_envio():
    if current_user.rol != 'proveedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    # Lógica para registrar un envío de productos
    flash('Envío registrado. Espera confirmación.', 'success')
    return redirect(url_for('proveedor.proveedor_dashboard'))

@bp.route('/proveedor/nuevo_envio', methods=['GET', 'POST'])
@login_required
def nuevo_envio():
    if current_user.rol != 'proveedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    from app.models.core import Producto, EnvioProveedor
    productos = Producto.query.all()
    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        cantidad = int(request.form['cantidad'])
        envio = EnvioProveedor(
            id_proveedor=current_user.id,
            id_producto=producto_id,
            cantidad=cantidad,
            estado='pendiente'
        )
        db.session.add(envio)
        db.session.commit()
        # Notificación visual y email a admin y vendedor
        from app.models.core import Usuario, Notificacion, Producto as ProductoModel
        from app.utils.notificaciones import enviar_notificacion_email
        admins = Usuario.query.filter_by(rol='admin').all()
        vendedores = Usuario.query.filter_by(rol='vendedor').all()
        producto = ProductoModel.query.get(producto_id)
        for user in admins + vendedores:
            notif = Notificacion(
                id_usuario=user.id,
                mensaje=f'El proveedor {current_user.nombre} ha solicitado un nuevo envío de "{producto.nombre}" (cantidad: {cantidad}).'
            )
            db.session.add(notif)
            if user.email:
                enviar_notificacion_email(
                    user.email,
                    'Nuevo envío solicitado por proveedor',
                    f'El proveedor {current_user.nombre} ha solicitado un nuevo envío de "{producto.nombre}" (cantidad: {cantidad}).'
                )
        db.session.commit()
        flash('Solicitud de envío registrada. Espera confirmación del administrador.', 'success')
        return redirect(url_for('proveedor.proveedor_dashboard'))
    return render_template('proveedor/nuevo_envio.html', productos=productos)

@bp.route('/proveedor/nuevo_producto', methods=['GET', 'POST'])
@login_required
def nuevo_producto_proveedor():
    if current_user.rol != 'proveedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    from app.models.core import Producto
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        imagen = request.files.get('imagen')
        if not imagen or imagen.filename == '':
            flash('La imagen es obligatoria.', 'danger')
            return render_template('proveedor/nuevo_producto.html')
        # Validar extensión
        allowed = {'.jpg', '.jpeg', '.png', '.gif'}
        ext = os.path.splitext(imagen.filename)[1].lower()
        if ext not in allowed:
            flash('Formato de imagen no permitido. Usa JPG, PNG o GIF.', 'danger')
            return render_template('proveedor/nuevo_producto.html')
        # Guardar imagen
        filename = nombre.strip().replace(' ', '_').lower() + ext
        ruta = os.path.join('app', 'static', 'imagenes', filename)
        imagen.save(ruta)
        imagen_url = '/static/imagenes/' + filename
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            imagen_url=imagen_url,
            stock=0,
            id_proveedor=current_user.id,
            aprobado=False
        )
        db.session.add(producto)
        db.session.commit()
        # Notificación visual y email a admin
        from app.models.core import Usuario, Notificacion
        from app.utils.notificaciones import enviar_notificacion_email
        admins = Usuario.query.filter_by(rol='admin').all()
        for admin in admins:
            notif = Notificacion(
                id_usuario=admin.id,
                mensaje=f'Nuevo producto "{nombre}" enviado por proveedor para aprobación.'
            )
            db.session.add(notif)
            if admin.email:
                enviar_notificacion_email(
                    admin.email,
                    'Nuevo producto para aprobación',
                    f'El proveedor {current_user.nombre} ha enviado el producto "{nombre}" para aprobación.'
                )
        db.session.commit()
        flash('Producto enviado para aprobación del administrador.', 'success')
        return redirect(url_for('proveedor.proveedor_dashboard'))
    return render_template('proveedor/nuevo_producto.html')
