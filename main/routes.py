from flask import render_template
from flask_login import current_user

from . import main_bp

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_user=current_user)
@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html',current_user=current_user)

@main_bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', current_user=current_user)


