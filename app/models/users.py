from flask_login import UserMixin
from app import db

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    idUser = db.Column(db.Integer, primary_key=True)
    nameUser = db.Column(db.String(80), unique=True, nullable=False)
    passwordUser = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def get_id(self):
        return str(self.idUser)