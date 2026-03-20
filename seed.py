from app import app, db, bcrypt
from app.models import Usuario

with app.app_context():
    senha = bcrypt.generate_password_hash('admin')

    user = Usuario(username="admin", senha=senha)

    db.session.add(user)
    db.session.commit()