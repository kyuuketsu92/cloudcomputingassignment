import os
from flaskext.mysql import MySQL
from flask import Flask, request, jsonify
import requests
from . import db


def create_app(test_config=None):

    

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import auth
    app.register_blueprint(auth.bp) 

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
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

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

    #techincally a log on only part of the website that for now as a test is being stored and handled here
    @app.route('/dashboard')
    def dashboard():
        return "Eventually going to be the dashboard for the calendar entry system or whatever. For now just handled as such."

    return app