from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Quarto
from app import db, bcrypt


class CadastroQuartoForm(FlaskForm):
    numero_quarto = IntegerField('Número do Quarto', validators=[DataRequired()])
    btn_submit = SubmitField('Cadastrar')


    def cadastrar(self):    
        quarto = Quarto(
            numero_quarto=self.numero_quarto.data,
        )

        db.session.add(quarto)
        db.session.commit()

        return quarto