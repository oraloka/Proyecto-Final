from app import create_app, db
import os
from app.models import Producto  # Asegúrate de importar el modelo Producto

app = create_app()

with app.app_context():
    db.create_all()
    # Si no hay productos, crear algunos de ejemplo
    if not Producto.query.first():

        productos_demo = [
            Producto(nombre='Cemento Portland', descripcion='Bolsa de 50kg', tipo='Cemento', precio=180.0, stock=100, imagen_url='/static/imagenes/cemento.jpg'),
            Producto(nombre='Ladrillo Hueco', descripcion='Ladrillo cerámico 18x18x33', tipo='Ladrillo', precio=25.0, stock=200, imagen_url='/static/imagenes/ladrillo.jpg'),
            Producto(nombre='Hierro 8mm', descripcion='Barra de hierro de 8mm', tipo='Hierro', precio=90.0, stock=150, imagen_url='/static/imagenes/hierro.jpg'),
            Producto(nombre='Arena', descripcion='M3 de arena fina', tipo='Árido', precio=350.0, stock=50, imagen_url='/static/imagenes/arena.jpg'),
            Producto(nombre='Cal Hidratada', descripcion='Bolsa de 25kg de cal hidratada', tipo='Cal', precio=120.0, stock=80, imagen_url='/static/imagenes/cal.jpg'),
            Producto(nombre='Pintura Blanca', descripcion='Latex interior 20L', tipo='Pintura', precio=450.0, stock=60, imagen_url='/static/imagenes/pintura.jpg'),
            Producto(nombre='Clavo 2"', descripcion='Caja de 1kg', tipo='Ferretería', precio=30.0, stock=300, imagen_url='/static/imagenes/clavo.jpg'),
            Producto(nombre='Madera Pino', descripcion='Tablón 2x4x3m', tipo='Madera', precio=200.0, stock=40, imagen_url='/static/imagenes/madera.jpg'),
        ]
        db.session.bulk_save_objects(productos_demo)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))