from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Usuario
from app import bcrypt


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
        

class CadastroUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btn_submit = SubmitField('Cadastrar Usuário')

    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Nome de usuário já cadastrado!')