from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models.core import Usuario
        return Usuario.query.get(int(id))

    from app.routes import auth
    from app.routes import register
    from app.routes import cliente
    from app.routes import proveedor
    from app.routes import vendedor
    from app.routes import admin
    from app.routes import perfil
    from app.routes import publico
    app.register_blueprint(auth.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(cliente.bp)
    app.register_blueprint(proveedor.bp)
    app.register_blueprint(vendedor.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(perfil.bp)
    app.register_blueprint(publico.bp)

    # Context processor para el carrito en navbar
    from app.models.core import Pedido
    from flask_login import current_user
    @app.context_processor
    def inject_carrito_count():
        count = 0
        try:
            if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and hasattr(current_user, 'id') and getattr(current_user, 'rol', None) == 'cliente':
                pedido = Pedido.query.filter_by(id_cliente=current_user.id, estado='pendiente').first()
                if pedido and hasattr(pedido, 'detalles') and pedido.detalles:
                    count = sum([d.cantidad for d in pedido.detalles])
        except Exception:
            count = 0
        return dict(carrito_count=count)

    return app