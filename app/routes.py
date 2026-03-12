from flask import render_template, redirect, url_for, flash
from app import app
from app.models import Usuario
from app.forms.user_forms import CadastroUserForm, LoginUserForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def main():
    quartos = [
        {'id': '1', 'Descrição': 'Quarto 1', 'Status': 'vazio'},
        {'id': '2', 'Descrição': 'Quarto 2', 'Status': 'vazio'},
        {'id': '3', 'Descrição': 'Quarto 3', 'Status': 'vazio'},
        {'id': '4', 'Descrição': 'Quarto 4', 'Status': 'vazio'},
        {'id': '5', 'Descrição': 'Quarto 5', 'Status': 'vazio'},
        {'id': '6', 'Descrição': 'Quarto 6', 'Status': 'vazio'},
    ]
    
    contex = {'quartos': quartos}

    return render_template('index.html', contex=contex)


@app.route('/users/cadastro/', methods=['GET', 'POST'])
@login_required
def cadastro_usuario():
    form = CadastroUserForm()
    if form.validate_on_submit():
        user = form.cadastrar()

        return redirect(url_for('main'))

    return render_template('form_cadastro_user.html', form=form)


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


@app.route('/logout/')
def logout():
    logout_user()

    flash('Logout bem sucedido!', 'alert-success')
    return redirect(url_for('login'))