import functools
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import flaskr.db as db
import flaskr.crypticarts as crypticarts
from flask_login import login_user, current_user, login_required, logout_user


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
        re1 = re.compile(r"[<>/{}[\]~' \"]")

        if not user.username:
            error = 'Username is required.'
        elif len(user.username) < 6:
            error = 'Username should be longer than 6 characters'
        elif re1.search(user.username):
            error = 'Invalid characters. No sql database dropping for you.'
        elif not request.form['registry_field_passphrase']:
            error = 'Password is required.'
        elif len(request.form['registry_field_passphrase']) < 8:
            error = 'Password should be 8 or more characters longer'
        elif not check_password_hash(user.passhash, request.form['registry_field_passphrase_verification']):
            error = 'Passwords do not match'
        elif db.is_email_exist(conn, user.email):
            error = 'Email {} is already registered.'.format(user.email)

        if error is None:
            cursor = conn.cursor()
            command = "INSERT INTO LOGIN_CREDENTIALS (USER_NAME, PASSPHRASE, EMAIL, API_AUTHKEY) VALUES ('{username}', '{passphrase}', '{email}', '{api_autkey}')".format(username = crypticarts.encrypt(user.username), passphrase = user.passhash, email = crypticarts.encrypt(user.email), api_autkey=crypticarts.encrypt(crypticarts.gen_auth_key()))
            print(command)
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

        cursor.execute("SELECT * FROM LOGIN_CREDENTIALS WHERE USER_NAME = '{uname}'".format(uname = crypticarts.encrypt(username)))        
        user = cursor.fetchone()
        #print(user)
        conn.close()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], request.form['login_field_passphrase']):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user[0])  
            userClass = db.getUser(user[0])
            login_user(userClass)
            conn = db.connect_db(mysql)
            cursor = conn.cursor()          
            cursor.execute("SELECT * FROM PERSONAL_INFORMATION WHERE USER_ID = {id}".format(id = user[0]))
            found = cursor.fetchone()
            #print(found)
            if found is None:
                return redirect(url_for('auth.persinf'))
            else:
                return redirect(url_for('logged_in.dashboard'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/persinf', methods=('GET', 'POST'))
@login_required
def persinf():
    userID = current_user.id

    mysql = db.get_db()
    error = None
    conn = db.connect_db(mysql)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PERSONAL_INFORMATION WHERE USER_ID = '{uid}'".format(uid = userID))        
    persinf = cursor.fetchone()
    #print(user)
    conn.close() 
    user = db.getUser(userID)

    if request.method == 'POST':
        nickname = request.form['persinf_nickname']
        fname = request.form['persinf_fname']
        mnames = request.form['persinf_mnames']
        lname = request.form['persinf_lname']
        age = request.form['persinf_age']


        if not nickname:
            error = 'Please enter display name.'
        try: 
            age = int(age)
        except:
            error = 'Entered age is not a number'
        
        if error is None:
            conn = db.connect_db(mysql)
            cursor = conn.cursor()
            if persinf is not None:
                #then we need to adjust the database data                
                command = "UPDATE PERSONAL_INFORMATION SET NICKNAME = '{nick}', FIRST_NAME = '{fname}', MIDDLE_NAMES = '{mnames}', LAST_NAME = '{lname}', AGE = '{age}'".format(
                    nick = crypticarts.encrypt(nickname),
                    fname = crypticarts.encrypt(fname) if fname else "",
                    mnames = crypticarts.encrypt(mnames) if mnames else "",
                    lname = crypticarts.encrypt(lname) if lname else "",
                    age = crypticarts.encrypt(str(age)) if str(age) else ""
                )
            else:
                command = "INSERT INTO PERSONAL_INFORMATION (USER_ID, NICKNAME, FIRST_NAME, MIDDLE_NAMES, LAST_NAME, AGE) VALUES ({uid}, '{nick}', '{fname}', '{mnames}', '{lname}', '{age}')".format(
                    uid = userID,
                    nick = crypticarts.encrypt(nickname),
                    fname = crypticarts.encrypt(fname) if fname else "",
                    mnames = crypticarts.encrypt(mnames) if mnames else "",
                    lname = crypticarts.encrypt(lname) if lname else "",
                    age = crypticarts.encrypt(str(age)) if str(age) else ""
                )
            #print(command)
            cursor.execute(command)   
            conn.commit()
            conn.close()

            return redirect(url_for('logged_in.dashboard'))

        flash(error)
    else:
        if persinf is not None:            
            return render_template('auth/pers_inf.html',
                persinf_nickname_placeholder = crypticarts.decrypt(persinf[2]) if persinf[2] is not None else "",
                persinf_fname_placeholder = crypticarts.decrypt(persinf[3]) if persinf[3] is not None else "",
                persinf_mnames_placeholder = crypticarts.decrypt(persinf[4]) if persinf[4] is not None else "",
                persinf_lname_placeholder = crypticarts.decrypt(persinf[5]) if persinf[5] is not None else "",
                persinf_age_placeholder = crypticarts.decrypt(persinf[6]) if persinf[6] is not None else "",
                user_name = crypticarts.decrypt(user.uname))
        else:
            return render_template('auth/pers_inf.html',
                persinf_nickname_placeholder = "",
                persinf_fname_placeholder = "",
                persinf_mnames_placeholder = "",
                persinf_lname_placeholder = "",
                persinf_age_placeholder="",
                user_name = crypticarts.decrypt(user.uname))
    
@bp.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/authkey', methods=('GET', 'POST'))
@login_required
def authkey():
    return render_template('auth/authkey.html')