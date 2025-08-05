from app.models.core import Factura, Pedido
from app import db
from datetime import datetime

def generar_factura(pedido_id, total, url_pdf=None):
    factura = Factura(
        id_pedido=pedido_id,
        fecha=datetime.utcnow(),
        total=total,
        url_pdf=url_pdf or ''
    )
    db.session.add(factura)
    db.session.commit()
    return factura

# Ejemplo de uso:
# factura = generar_factura(pedido_id=1, total=500.0, url_pdf='facturas/1.pdf')
