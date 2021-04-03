import flaskr.db as db
import flaskr.crypticarts as crypticarts
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json
)
from flask_login import LoginManager, current_user, login_required, current_user
from flaskr.blueprints.reminder import timeRemaining, inFuture

bp = Blueprint('logged_in', __name__, url_prefix='/logged_in')

@bp.route('/dashboard')
@login_required
def dashboard():
    placeholderWeatherJson='{"name":"Weather forecast", "location":"London", "days":[ {"day" : "02 Apr", "max" : "15", "min":"8"},{"day" : "03 Apr", "max" : "13", "min":"5"},{"day" : "04 Apr", "max" : "11", "min":"3"}]}'
    reminderRaw = db.getEntries(current_user.id)
    if reminderRaw is not None:
        reminderFuture = []
        for element in reminderRaw:
            if inFuture(element["date"]):
                reminderFuture.append(element)
        if len(reminderFuture) > 0:
            return render_template('logged_in/dashboard.html',
                weatherdataJSONtable=db.html_format_json(placeholderWeatherJson),
                reminderdataJSON=reminderFuture,
                timeRemaining=timeRemaining)
    
    return render_template('logged_in/dashboard.html',
        weatherdataJSONtable=db.html_format_json(placeholderWeatherJson),
        timeRemaining=timeRemaining)

