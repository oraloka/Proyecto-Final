from app import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin, cliente, proveedor, vendedor
    estado = db.Column(db.String(20), default='activo')  # activo, bloqueado

    def get_id(self):
        return str(self.id)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    tipo = db.Column(db.String(50), nullable=False, default='General')
    imagen_url = db.Column(db.String(255), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    proveedor = db.relationship('Usuario', foreign_keys=[id_proveedor])

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, aceptado, rechazado, entregado, en camino
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    id_admin = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    cliente = db.relationship('Usuario', foreign_keys=[id_cliente])
    vendedor = db.relationship('Usuario', foreign_keys=[id_vendedor])
    admin = db.relationship('Usuario', foreign_keys=[id_admin])

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    pedido = db.relationship('Pedido', backref='detalles')
    producto = db.relationship('Producto')

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    url_pdf = db.Column(db.String(255))
    pedido = db.relationship('Pedido')

class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    mensaje = db.Column(db.String(255))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    leida = db.Column(db.Boolean, default=False)
    usuario = db.relationship('Usuario')

class EnvioProveedor(db.Model):
    __tablename__ = 'envio_proveedor'
    id = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, aceptado, rechazado
    id_admin = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    proveedor = db.relationship('Usuario', foreign_keys=[id_proveedor])
    admin = db.relationship('Usuario', foreign_keys=[id_admin])
    producto = db.relationship('Producto')
