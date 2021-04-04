#this is the py that deals with curl commands

import flaskr.db as db
import flaskr.weatherapi as weatherapi
import flaskr.crypticarts as crypticarts
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify
)
from flask_login import LoginManager, current_user, login_required, current_user
import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/')
def test():
    return "Hi",200

@bp.route('/reminder_get<authkey>')
def get_reminders(authkey):
    #idea here is that the authkey will authenticate the user 
    #due to lack of time this is not very secure, not encrypted or anything. If the authkey gets out then its a problem
    
    #let's find the user with this authkey
    entries, error = db.getEntries_auth(authkey)
    if error is not None:
        return jsonify({"error":error}),500
    else:
        #we need to convert the entries into json from disctionary
        return jsonify(entries),200


@bp.route('/reminder_add', methods=('GET','POST'))
def add_reminder():
    if request.method == 'POST':
        #do stuff
        #print(request.json)
        try:
            authkey = request.json['apiauthkey']
            print(authkey)
        except:
            return jsonify({"error":"authkey parsing failed"}),500
        try:
            date = request.json['date']
            datime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            print(date)
        except:
            return jsonify({"error":"Date parsing failed"}),500
        try:
            desc = request.json['description']
            print(desc)
        except:
            return jsonify({"error":"Description parsing failed"}),500

        #okay so no errors so far and we can gotten all data from the json
        #see if the user exists
        uid = db.get_authkey_user(authkey)
        if uid is None:
            return jsonify({"error":"Wrong authkey"}),500
        
        #so user exists and have added a new entry, let's save it in the database
        command = "INSERT INTO USER_DATA (USER_ID, DATE_T, DESC_T) VALUES ({uid}, '{date}', '{desc}')"
        mysql = db.get_db()
        conn = db.connect_db(mysql)
        cursor = conn.cursor()
        cursor.execute(command.format(
            uid=uid,
            date=crypticarts.encrypt(str(datime)),
            desc=crypticarts.encrypt(desc))
        )        
        conn.commit()
        cursor.execute('SELECT * FROM USER_DATA WHERE DESC_T = "{desc}"'.format(desc = crypticarts.encrypt(desc)))
        data = cursor.fetchone()
        conn.close()
        return jsonify({"success":"Reminder added", "id": crypticarts.encrypt(str(data[0]))}), 200
    else:
#        #tell how to use the add api
        usage = 'curl --header "Content-Type: application/json" --request POST --data \'{\"apiauthkey\":\"key\",\"date\":\"%Y-%m-%d %H:%M:%S\", \"description\":\"short description of what the reminder is about\"}\' url_base/api/reminder_add'
        example = 'curl --header "Content-Type: application/json" --request POST --data "{\"apiauthkey\":\"1231123417824619dgf08712\",\"date\":\"2021-04-05 23:59:00\", \"description\":\"whatever text\"}" 127.0.0.1:5000/api/reminder_add'
        disc = 'Depending on operating system, the commands might need extra backslash characters before the \" characters.'
        return "Usage: "+usage+"<br>Example: "+example+"<br><br>"+disc,200

@bp.route('/reminder_modify', methods=('GET','POST'))
def modify_reminder():
    if request.method == 'POST':
        #do stuff
        #print(request.json)
        try:
            authkey = request.json['apiauthkey']
            #print(authkey)
        except:
            return jsonify({"error":"authkey parsing failed"}),500
        try:
            entry_id = request.json['entry_id']
            #print(entry_id)
        except:
            return jsonify({"error":"Entry ID parsing failed"}),500
        try:
            date = request.json['date']
            datime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            #print(date)
        except:
            return jsonify({"error":"Date parsing failed"}),500
        try:
            desc = request.json['description']
            #print(desc)
        except:
            return jsonify({"error":"Description parsing failed"}),500

        #okay so no errors so far and we can gotten all data from the json
        #see if the user exists
        uid = db.get_authkey_user(authkey)
        if uid is None:
            return jsonify({"error":"Wrong authkey"}),500
        

        #let's see if the entry exists
        mysql = db.get_db()
        conn = db.connect_db(mysql)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USER_DATA WHERE ENTRY_ID = {id}'.format(id = crypticarts.decrypt(entry_id)))
        data = cursor.fetchone()
        conn.close()
        if data is not None:
            #okay data exists, lets update it
            conn = db.connect_db(mysql)
            cursor = conn.cursor()
            #so user exists and have added a new entry, let's save it in the database
            command = "UPDATE USER_DATA SET USER_ID = '{uid}', DATE_T = '{date}', DESC_T = '{desc}' WHERE ENTRY_ID = {id}".format(
                uid=data[1],
                date=crypticarts.encrypt(str(datime)),
                desc=crypticarts.encrypt(desc),
                id = crypticarts.decrypt(entry_id))

            cursor.execute(command)       
            conn.commit()
            conn.close()
            return jsonify({"success":"Reminder modified"}), 200
        else:
            return jsonify({"error":"No such entry"}),500
    else:
#        #tell how to use the modify api
        usage = 'curl --header "Content-Type: application/json" --request POST --data \'{\"apiauthkey\":\"key\", \"entry_id\":\"id\", \"date\":\"%Y-%m-%d %H:%M:%S\", \"description\":\"short description of what the reminder is about\"}\' url_base/api/reminder_modify'
        example = 'curl --header "Content-Type: application/json" --request POST --data "{\"apiauthkey\":\"1231123417824619dgf08712\", \"entry_id\":\"2341223ff134123451\", \"date\":\"2021-04-05 23:59:00\", \"description\":\"whatever text\"}" 127.0.0.1:5000/api/reminder_modify'
        disc = 'Depending on operating system, the commands might need extra backslash characters before the \" characters.'
        return "Usage: "+usage+"<br>Example: "+example+"<br><br>"+disc,200


@bp.route('/reminder_delete', methods=('GET','DELETE'))
def delete_reminder():  
    if request.method == 'DELETE':
        try:
            authkey = request.json['apiauthkey']
            #print(authkey)
        except:
            return jsonify({"error":"authkey parsing failed"}),500
        try:
            entry_id = request.json['entry_id']
            #print(entry_id)
        except:
            return jsonify({"error":"Entry ID parsing failed"}),500

        #okay so no errors so far and we can gotten all data from the json
        #see if the user exists
        uid = db.get_authkey_user(authkey)
        if uid is None:
            return jsonify({"error":"Wrong authkey"}),500

        #let's see if the entry exists
        mysql = db.get_db()
        conn = db.connect_db(mysql)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USER_DATA WHERE ENTRY_ID = {id}'.format(id = crypticarts.decrypt(entry_id)))
        data = cursor.fetchone()
        conn.close()
        if data is not None:
            #okay data exists, lets update it
            conn = db.connect_db(mysql)
            cursor = conn.cursor()
            #so user exists and have added a new entry, let's save it in the database
            command = "DELETE FROM USER_DATA WHERE ENTRY_ID = {id}".format(id = crypticarts.decrypt(entry_id))
            cursor.execute(command)       
            conn.commit()
            conn.close()
            return jsonify({"success":"Reminder deleted"}), 200
        else:
            return jsonify({"error":"No such entry"}),500
        
    else:
        #tell how to use the delete api
        usage = 'curl --header "Content-Type: application/json" --request DELETE --data \'{\"apiauthkey\":\"key\", \"entry_id\":\"id\"}\' url_base/api/reminder_delete'
        example = 'curl --header "Content-Type: application/json" --request DELETE --data "{\"apiauthkey\":\"1231123417824619dgf08712\", \"entry_id\":\"2341223ff134123451\"}" 127.0.0.1:5000/api/reminder_delete'
        disc = 'Depending on operating system, the commands might need extra backslash characters before the \" characters.'
        return "Usage: "+usage+"<br>Example: "+example+"<br><br>"+disc,200

@bp.route('/weather')
def weather():
    return weatherapi.get_weather_json(),200