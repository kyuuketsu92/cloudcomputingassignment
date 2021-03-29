import os
from flaskext.mysql import MySQL
from flask import Flask
from . import db


def create_app(test_config=None): 

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    return app