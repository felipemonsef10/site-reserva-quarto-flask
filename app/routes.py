from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.models import Quarto, Usuario
from app.forms.user_forms import LoginUserForm, CadastroUserForm
from app.forms.quarto_forms import CadastroQuartoForm, ReservarQuartoForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET', 'POST'])
def main():
    contex = {}
    contex['current_user'] = current_user.is_authenticated
    
    quartos = Quarto.query.all()

    cidade = request.args.get('cidade', '')
    if cidade:
        contex['cidade'] = cidade
        quartos = [quarto for quarto in quartos if cidade == quarto.cidade.replace(' ', '')]
    
    contex['quartos'] = quartos

    return render_template('index.html', contex=contex)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginUserForm()

    if form.validate_on_submit():
        user = form.login()

        if user:
            login_user(user, remember=True)
            flash('Login bem sucedido!', 'alert-success')
            return redirect(url_for('main'))
        else:
            flash('Erro! Usuário não autenticado.', 'alert-danger')
    
    return render_template('form_login.html', form=form)


@app.route('/cadastrar-usuario/', methods=['GET', 'POST'])
@login_required
def cadastro_user():    
    form = CadastroUserForm()

    if form.validate_on_submit():
        senha = bcrypt.generate_password_hash(form.senha.data)
        user = Usuario(username=form.username.data, senha=senha)

        db.session.add(user)
        db.session.commit()

        flash('Cadastro bem sucedido!', 'alert-success')
        return redirect(url_for('main'))
    
    return render_template('form_cadastro_user.html', form=form)


@app.route('/quarto/cadastro/', methods=['GET', 'POST'])
@login_required
def cadastro_quartos():
    form = CadastroQuartoForm()
    if form.validate_on_submit():
        quarto = form.cadastrar()

        flash('Quarto cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('main'))

    return render_template('form_cadastro_quarto.html', form=form)


@app.route('/quarto/<int:id>/reserva', methods=['GET', 'POST'])
@login_required
def reservar_quarto(id):
    form = ReservarQuartoForm()
    quarto = Quarto.query.get(id)

    if form.validate_on_submit():
        quarto.hospede = form.hospede.data
        quarto.status = True

        db.session.commit()

        flash('Quarto reservado com sucesso!', 'alert-success')
        return redirect(url_for('main'))
    
    return render_template('form_reservar_quarto.html', form=form, quarto=quarto)


@app.route('/quarto/<int:id>/cancelar_reserva', methods=['GET', 'POST'])
@login_required
def cancelar_reserva(id):
    quarto = Quarto.query.get(id)

    quarto.hospede = 'Quarto Vago'
    quarto.status = False

    db.session.commit()
    flash('Reserva cancelada com sucesso!', 'alert-warning')
    return redirect(url_for('main'))


@app.route('/quarto/<int:id>/delete')
@login_required
def excluir_quarto(id):
    quarto = Quarto.query.get(id)

    if not quarto:
        flash('Quarto não encontrado!', 'alert-danger')
        return redirect(url_for('main'))
    
    else:
        db.session.delete(quarto)
        db.session.commit()

        flash(f'Quarto {quarto.numero_quarto} {quarto.cidade} excluído com sucesso!', 'alert-info')
        return redirect(url_for('main'))


@app.route('/logout/')
def logout():
    logout_user()

    flash('Logout bem sucedido!', 'alert-success')
    return redirect(url_for('login'))