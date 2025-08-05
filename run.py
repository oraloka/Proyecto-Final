from app import create_app, db
import os
from app.models import Producto  # Asegúrate de importar el modelo Producto

app = create_app()

with app.app_context():
    db.create_all()
    # Eliminar todos los productos y usuarios existentes
    from app.models import Producto, Usuario, EnvioProveedor
    EnvioProveedor.query.delete()
    Producto.query.delete()
    Usuario.query.delete()
    db.session.commit()

    # Crear usuario admin y proveedor de prueba
    from werkzeug.security import generate_password_hash
    admin = Usuario(nombre='Admin', email='admin@demo.com', password=generate_password_hash('admin123'), rol='admin', estado='activo')
    proveedor = Usuario(nombre='Proveedor', email='proveedor@demo.com', password=generate_password_hash('proveedor123'), rol='proveedor', estado='activo')
    db.session.add(admin)
    db.session.add(proveedor)
    db.session.commit()

    # Ya no se crean productos ni envíos de prueba

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))