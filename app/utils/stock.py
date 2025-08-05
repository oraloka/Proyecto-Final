from app.models.core import Producto, DetallePedido, EnvioProveedor
from app import db

def descontar_stock_por_pedido(detalles):
    for detalle in detalles:
        producto = Producto.query.get(detalle.id_producto)
        if producto and producto.stock >= detalle.cantidad:
            producto.stock -= detalle.cantidad
        else:
            raise Exception(f'Stock insuficiente para {producto.nombre}')
    db.session.commit()

def reponer_stock_por_envio(envio):
    producto = Producto.query.get(envio.id_producto)
    if producto:
        producto.stock += envio.cantidad
        db.session.commit()
