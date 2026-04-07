from flask import render_template

from . import auth_bp
from .forms import LoginForm, RegisterForm
from .models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
    return render_template('login.html', form = form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.username.data)

    return render_template('register.html', form = form)