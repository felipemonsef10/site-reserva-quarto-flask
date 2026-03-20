# seed.py
from app import app, db, bcrypt
from app.models import Usuario

def seed_database():
    with app.app_context():
        # Verifica se o admin já existe para não criar duplicado
        admin_existente = Usuario.query.filter_by(username='admin').first()
        
        if not admin_existente:
            hash_senha = bcrypt.generate_password_hash('admin').decode('utf-8')
            novo_admin = Usuario(username='admin', senha=hash_senha)
            db.session.add(novo_admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe no banco.")

if __name__ == "__main__":
    seed_database()