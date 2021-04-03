import os
from flaskext.mysql import MySQL
from flask import Flask, request, jsonify, redirect, render_template, url_for
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import requests
from . import db
from . import crypticarts
from flask_login import LoginManager, current_user, login_required, current_user

def create_app(test_config=None):

    

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    #check if keyfile is there, and if not generate a new one. (If the program generates a new keyfile )
    if(crypticarts.is_keyfile_exists() == False):
        crypticarts.gen_keyfile()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        #print('This ran')
        return db.getUser(int(user_id))

    #test to see if encryption works from module as well
    #ct = crypticarts.encrypt("erkjNOEJJC Veipucvbe[kocnasm'cioabc <- random size text")
    #print(ct)
    #print(crypticarts.decrypt(ct))

    from flaskr.blueprints import auth, logged_in, reminder, api
    app.register_blueprint(auth.bp) 
    app.register_blueprint(logged_in.bp)
    app.register_blueprint(reminder.bp)
    app.register_blueprint(api.bp)

    mysql = db.init_db(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index_redirect():
        return redirect(url_for('index'))

    @app.route('/index')
    def index():
        return render_template('welcome_page.html')


    # This is a testing only function that helps us visualise the database status 
    # Not suited for real time production environments
    @app.route('/test-db')
    def display_database():
        return db.get_html_database(mysql),200

    # this is a test for an upcoming weather API where we use an external API to get location information
    @app.route('/test-ipdata')
    def display_ipdata():
        ip_address = request.remote_addr
        #ip_address = '90.194.108.13'
        #print('http://ip-api.com/json/{ip}'.format(ip=ip_address))
        response = requests.get('http://ip-api.com/json/{ip}'.format(ip=ip_address))
        data = response.json()
        #print(json_data.text)

        #example on how to get the longitude and latitude coordinates from successful responses
        #if(data["status"] != "fail"):
        #    print(data["lat"])
        #    print(data["lon"])
        #else:
        #    print("failed")
        return ("User_ip_address:"+ip_address+"<br>"+db.html_format_json(data)),200

    return app