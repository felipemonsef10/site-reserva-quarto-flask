from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Quarto
from app import db, bcrypt


class CadastroQuartoForm(FlaskForm):
    numero_quarto = IntegerField('Número do Quarto', validators=[DataRequired()])
    cidade = RadioField('Cidade', choices=[('Pires do Rio', 'Pires do Rio'), ('Goiandira', 'Goiandira')], validators=[DataRequired()])
    btn_submit = SubmitField('Cadastrar')


    def validate_numero_quarto(self, numero_quarto):
        quarto = Quarto.query.filter_by(numero_quarto=numero_quarto.data, cidade=self.cidade.data).first()
        if quarto and self.cidade.data == quarto.cidade:
            raise ValidationError(f'Quarto já cadastrado para essa cidade! {self.cidade.data} {quarto.cidade}')


    def cadastrar(self):    
        quarto = Quarto(
            cidade=self.cidade.data,
            numero_quarto=self.numero_quarto.data
        )

        db.session.add(quarto)
        db.session.commit()

        return quarto
    

class ReservarQuartoForm(FlaskForm):
    hospede = StringField('Hóspede', validators=[DataRequired()])
    btn_submit = SubmitField('Confirmar Reserva')