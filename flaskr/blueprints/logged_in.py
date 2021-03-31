import flaskr.db as db
import flaskr.crypticarts as crypticarts
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from flask_login import LoginManager, current_user, login_required, current_user

bp = Blueprint('logged_in', __name__, url_prefix='/logged_in')

@bp.route('/dashboard')
@login_required
def dashboard():
    userID = current_user.id
    return render_template('logged_in/dashboard.html')
