import functools
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

import flaskr.db as db

bp = Blueprint('auth', __name__, url_prefix='/auth')

class obj_USER:
    def __init__(self, username, passphrase_hashed, email):
        self.username = username
        self.passhash = passphrase_hashed
        self.email = email

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user = obj_USER(
            request.form['registry_field_username'],
            generate_password_hash(request.form['registry_field_passphrase']),
            request.form['registry_field_email'])
        
        mysql = db.get_db()
        conn = db.connect_db(mysql)
        error = None

        ##check for username validity and remove illegal character 
        re1 = re.compile(r"[<>/{}[\]~'\"]")

        if not user.username:
            error = 'Username is required.'
        elif re1.search(username):
            error = 'Invalid characters. No sql database dropping for you.'
        elif not request.form['registry_field_passphrase']:
            error = 'Password is required.'
        elif not check_password_hash(user.passhash, request.form['registry_field_passphrase_verification']):
            error = 'Passwords do not match'
        elif db.is_email_exist(conn, user.email):
            error = 'Email {} is already registered.'.format(user.email)

        if error is None:
            cursor = conn.cursor()
            command = "INSERT INTO LOGIN_CREDENTIALS (USER_NAME, PASSPHRASE, EMAIL) VALUES ('{username}', '{passphrase}', '{email}')".format(username = user.username, passphrase = user.passhash, email = user.email)
            cursor.execute(command)
            conn.commit()
            conn.close()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['login_field_username']
        mysql = db.get_db()
        error = None

        conn = db.connect_db(mysql)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM LOGIN_CREDENTIALS WHERE USER_NAME = '{uname}'".format(uname = username))
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], request.form['login_field_passphrase']):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user[0])
            return redirect(url_for('hello'))

        flash(error)

    return render_template('auth/login.html')

