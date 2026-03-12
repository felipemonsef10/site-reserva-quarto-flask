from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Usuario
from app import db, bcrypt


class CadastroUserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=128)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=40)])
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    btn_submit = SubmitField('Cadastrar')

    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
            raise ValidationError('E-mail já cadastrado. Faça login para continuar.')

    def cadastrar(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        
        usuario = Usuario(
            nome=self.nome.data,
            email=self.email.data,
            senha=senha
        )

        db.session.add(usuario)
        db.session.commit()

        return usuario


class LoginUserForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btn_submit = SubmitField('Fazer Login')

    def login(self):
        user = Usuario.query.filter_by(email=self.email.data).first()
        if user:
            senha = user.senha
            if bcrypt.check_password_hash(senha, self.senha.data):
                print('Logado com sucesso.')
                return user
        else:
            return False