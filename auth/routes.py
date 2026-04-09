from flask import render_template, redirect, url_for, flash

from . import auth_bp
from .forms import LoginForm, RegisterForm
from .models import User
from __init__ import db
from flask import render_template, redirect, url_for, flash, session

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("entered username:", form.username.data)
        print("entered password:", form.password.data)
        print("db user:", user)
        if user:
            print("stored password:", user.password)
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main_bp.home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_user:
            flash('Username already exists.', 'warning')
            return redirect(url_for('auth.register'))

        existing_email = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_email:
            flash('Email already exists.', 'warning')
            return redirect(url_for('auth.register'))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)