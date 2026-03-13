from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(20), nullable=False)


class Quarto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(25), nullable=False)
    numero_quarto = db.Column(db.Integer, nullable=False, unique=True)
    hospede = db.Column(db.String(50), nullable=False, default='Quarto Vago')
    status = db.Column(db.Boolean, nullable=False, default=False)
