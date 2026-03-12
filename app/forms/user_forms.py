from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import Usuario
from app import db, bcrypt


class CadastroUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=128)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=40)])
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    btn_submit = SubmitField('Cadastrar')


    def cadastrar(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        
        usuario = Usuario(
            username=self.username.data,
            senha=senha
        )

        db.session.add(usuario)
        db.session.commit()

        return usuario


class LoginUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btn_submit = SubmitField('Fazer Login')

    def login(self):
        user = Usuario.query.filter_by(username=self.username.data).first()
        if user:
            senha = user.senha
            if bcrypt.check_password_hash(senha, self.senha.data):
                return user
        else:
            return False