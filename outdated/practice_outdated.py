#!#/usr/bin/python3

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flaskext.mysql import MySQL

app = Flask(__name__)
#add modules here
#app.register_blueprint(index_page)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sql4401943'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AXYerx4aQP'
app.config['MYSQL_DATABASE_DB'] = 'sql4401943'
app.config['MYSQL_DATABASE_HOST'] = 'sql4.freemysqlhosting.net'
mysql.init_app(app)

@app.route('/')
def hello():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("USE sql4401943")
    cursor.execute("SELECT * from LOGIN_CREDENTIALS")
    string_output = ""
    while(True): #scary gotta rework
        data = cursor.fetchone()
        print(data)
        print(type(data))
        if(type(data) != type(tuple())):
            break
        else:
            string_output += str(data)
            string_output += "<br>"

    cursor.execute("SELECT * from PERSONAL_INFORMATION")
    string_output += "<br><br>"
    while(True): #scary gotta rework
        data = cursor.fetchone()
        print(data)
        print(type(data))
        if(type(data) != type(tuple())):
            break
        else:
            string_output += str(data)
            string_output += "<br>"
    
    cursor.execute("SELECT * from USER_DATA")
    string_output += "<br><br>"
    while(True): #scary gotta rework
        data = cursor.fetchone()
        print(data)
        print(type(data))
        if(type(data) != type(tuple())):
            break
        else:
            string_output += str(data)
            string_output += "<br>"

    string_output += "<a href=\"/register\"> Register </a>"

    conn.close()

    return 'Hello World!<br> {data}'.format(data = string_output), 200

@app.route('/register') #basic form for the registration process
def register():
    html_str = "";
    html_str += '<form action="/register/complete" method="post">'
    html_str += 'Username:        <input name="registry_field_username" type="text" size="40" placeholder="" required><br>'
    html_str += 'Password:        <input name="v" type="password" size="40" placeholder="" required><br>'
    html_str += 'Verify password: <input name="registry_field_passphrase_verification" type="password" size="40" placeholder="" required><br>'
    html_str += 'Email:           <input name="registry_field_email" type="email" size=60 placeholder="" required><br>'
    html_str += '<input type="submit" value="Register">'
    html_str += '</form>'
    return html_str, 200

@app.route('/register/complete', methods=['POST']) #ideally this is where we can access the form
def check_registration():
    username = request.form['registry_field_username']
    passphrase = generate_password_hash(str(request.form['registry_field_passphrase']))
    passphrase_ver = generate_password_hash(str(request.form['registry_field_passphrase_verification']))
    email = request.form['registry_field_email']

    ##check for username validity and remove illegal character 
    re1 = re.compile(r"[<>/{}[\]~'\"]")
    if re1.search(username):
        return jsonify({'error': 'Username contained invalid characters'}), 500
    
    if not check_password_hash(passphrase, str(request.form['registry_field_passphrase_verification'])):
        return jsonify({'error': 'Passphrases did not match'}), 500

    

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("USE sql4401943")

    cursor.execute("SELECT ID_MAIN, USER_NAME, PASSPHRASE, EMAIL FROM LOGIN_CREDENTIALS WHERE EMAIL like '{email}'".format(email = email))
    data = cursor.fetchone()
    if(type(data) == type(tuple())):
        return jsonify({'error': 'Email is already in the system. Log in instead.'}), 500

    command = "INSERT INTO LOGIN_CREDENTIALS (USER_NAME, PASSPHRASE, EMAIL) VALUES ('{username}', '{passphrase}', '{email}')".format(username = str(username), passphrase = str(passphrase), email = str(email))
    cursor.execute(command)
    conn.commit() #goddamn line that was missing and kept giving me issues
    conn.close()
    return jsonify({'Success': 'User registered'}), 201
