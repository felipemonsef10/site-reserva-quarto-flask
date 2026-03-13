from flask import render_template, redirect, url_for, flash
from app import app, db
from app.models import Quarto
from app.forms.user_forms import LoginUserForm
from app.forms.quarto_forms import CadastroQuartoForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def main():
    quartos = Quarto.query.all()
    contex = {'quartos': quartos}
    
    if current_user.is_authenticated:
        contex['current_user'] = True
    else:
        contex['current_user'] = False

    return render_template('index.html', contex=contex)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginUserForm()

    if form.validate_on_submit():
        user = form.login()

        if user:
            login_user(user)
            flash('Login bem sucedido!', 'alert-success')
            return redirect(url_for('main'))
        else:
            flash('Erro! Usuário não autenticado.', 'alert-danger')
    
    return render_template('form_login.html', form=form)


@app.route('/quarto/cadastro/', methods=['GET', 'POST'])
@login_required
def cadastro_quartos():
    form = CadastroQuartoForm()
    if form.validate_on_submit():
        quarto = form.cadastrar()

        flash('Quarto cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('main'))

    return render_template('form_cadastro_quarto.html', form=form)


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

        flash('Quarto Excluído com Sucesso', 'alert-warning')
        return redirect(url_for('main'))


@app.route('/logout/')
def logout():
    logout_user()

    flash('Logout bem sucedido!', 'alert-success')
    return redirect(url_for('login'))