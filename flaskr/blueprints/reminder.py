import flaskr.db as db
import flaskr.crypticarts as crypticarts
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from flask_login import LoginManager, current_user, login_required, current_user
import datetime

bp = Blueprint('reminder', __name__, url_prefix='/reminder')
#string date
def timeRemaining(date):
    if type(date) != type("string"): #error handling
        return ""

    now = datetime.datetime.now()
    #print(now)
    datet = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    #print(datet)
    remainder = datet - now
    #print(remainder)
    days, remainderh = divmod(remainder.total_seconds(), 3600*24)
    hours, remainderm = divmod(remainderh, 3600)
    mins, remainders = divmod(remainderm, 60)
    return str(int(days)) + " Days, " + str(int(hours)) + " Hours, " + str(int(mins)) + " Mins"

#string date
def inFuture(date):
    datime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    diff = datime - now
    if diff.total_seconds() >= 0:
        return True
    else:
        return False
 
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    userID = current_user.id
    error = None

    if request.method == 'POST':
        day = request.form['reminder_add_day']
        month = request.form['reminder_add_month']
        year = request.form['reminder_add_year']
        hour = request.form['reminder_add_hour']
        minutes = request.form['reminder_add_minutes']
        description = request.form['reminder_add_description']

        if not day:
            error = 'Day required'
        if not month:
            error = 'Month required'
        if not year:
            error = 'Year required'
        if not description:
            error = 'Description required'
        if not month.isnumeric():
            error = 'Invalid month'
        elif (int(month) < 0) or (int(month) > 12):
            error = 'Out of bounds month'
        if not year.isnumeric():
            error = 'Invalid year'
        elif (int(year) < 0) or (int(year) > 9999):
            error = 'Out of bounds year'
        if not hour.isnumeric():
            error = 'Invalid hour'
        elif (int(hour) < 0) or (int(hour) > 23):
            error = 'Out of bounds hour'
        if not minutes.isnumeric():
            error = 'Invalid minutes'
        elif (int(minutes) < 0) or (int(minutes) > 59):
            error = 'Out of bounds minutes'
        if not day.isnumeric():
            error = 'Invalid day'
        elif (int(day) < 0) or (int(day) > 31):
            error = 'Out of bounds day'

        if error is None:
            date = datetime.date(int(year), int(month), 1)
            time = datetime.time(int(hour), int(minutes))
            datime = datetime.datetime.combine(date, time)
            #print(datetime)
            datime += datetime.timedelta(days=(int(day)-1))
            if int(month) < datime.month:
                error = "Not that many days in that month" 
            elif datime.date() < datetime.datetime.now().date():
                error = "Date given is not a future date" 

        if error is None:     
            command = "INSERT INTO USER_DATA (USER_ID, DATE_T, DESC_T) VALUES ({uid}, '{date}', '{desc}')"
            mysql = db.get_db()
            conn = db.connect_db(mysql)
            cursor = conn.cursor()
            cursor.execute(command.format(
                uid=current_user.id,
                date=crypticarts.encrypt(str(datime)),
                desc=crypticarts.encrypt(description))
            )        
            conn.commit()
            conn.close()
            flash("Entry added")
            return render_template('reminder/add.html',
            reminder_add_day_placeholder = " ",
            reminder_add_month_placeholder=" ",
            reminder_add_year_placeholder=" ",
            reminder_add_hour_placeholder=" ",
            reminder_add_minutes_placeholder=" ",
            reminder_add_description_placeholder = " ",
            user_name = crypticarts.decrypt(current_user.uname))

        #this is when there was an error in the post
        flash(error)
        return render_template('reminder/add.html',
            reminder_add_day_placeholder = day,
            reminder_add_month_placeholder=month,
            reminder_add_year_placeholder=year,
            reminder_add_hour_placeholder=hour,
            reminder_add_minutes_placeholder=minutes,
            reminder_add_description_placeholder = description,
            user_name = crypticarts.decrypt(current_user.uname))
    #this was a get request
    return render_template('reminder/add.html',
            reminder_add_day_placeholder = "",
            reminder_add_month_placeholder="",
            reminder_add_year_placeholder="",
            reminder_add_hour_placeholder="",
            reminder_add_minutes_placeholder="",
            reminder_add_description_placeholder = "",
            user_name = crypticarts.decrypt(current_user.uname))

@bp.route('/modify')
@login_required
def modify():
    reminderRaw = db.getEntries(current_user.id)
    if reminderRaw is not None:
        return render_template('reminder/modify.html',
            reminderdataJSON=reminderRaw,
            timeRemaining=timeRemaining)
    
    return render_template('reminder/modify.html',
        timeRemaining=timeRemaining)

@bp.route('/modify/<key>', methods=('GET', 'POST'))
@login_required
def modifyKey(key):
    userID = current_user.id
    error = None

    #the deal here is: we have an existing entry to modify 
    command = "SELECT * FROM USER_DATA WHERE ENTRY_ID = {key}".format(key = crypticarts.decrypt(key))
    mysql = db.get_db()
    conn = db.connect_db(mysql)
    cursor = conn.cursor()
    cursor.execute(command)
    data = cursor.fetchone()
    conn.close()

    #let's check if the user accessing this data is the correct user
    #you can never be to careful afterall :D
    if data is not None:
        #we foound the entry in question
        if userID == data[1]:
            error = None;
        else:
            error = "Wrong Access"
            return redirect(url_for("reminder.modify"))
    else:
        error = "No such entry"
        return redirect(url_for("reminder.modify"))

    if request.method == 'POST':
        day = request.form['reminder_add_day']
        month = request.form['reminder_add_month']
        year = request.form['reminder_add_year']
        hour = request.form['reminder_add_hour']
        minutes = request.form['reminder_add_minutes']
        description = request.form['reminder_add_description']

        if not day:
            error = 'Day required'
        if not month:
            error = 'Month required'
        if not year:
            error = 'Year required'
        if not description:
            error = 'Description required'
        if not month.isnumeric():
            error = 'Invalid month'
        elif (int(month) < 0) or (int(month) > 12):
            error = 'Out of bounds month'
        if not year.isnumeric():
            error = 'Invalid year'
        elif (int(year) < 0) or (int(year) > 9999):
            error = 'Out of bounds year'
        if not hour.isnumeric():
            error = 'Invalid hour'
        elif (int(hour) < 0) or (int(hour) > 23):
            error = 'Out of bounds hour'
        if not minutes.isnumeric():
            error = 'Invalid minutes'
        elif (int(minutes) < 0) or (int(minutes) > 59):
            error = 'Out of bounds minutes'
        if not day.isnumeric():
            error = 'Invalid day'
        elif (int(day) < 0) or (int(day) > 31):
            error = 'Out of bounds day'

        if error is None:
            date = datetime.date(int(year), int(month), 1)
            time = datetime.time(int(hour), int(minutes))
            datime = datetime.datetime.combine(date, time)
            #print(datetime)
            datime += datetime.timedelta(days=(int(day)-1))
            if int(month) < datime.month:
                error = "Not that many days in that month" 
            elif datime.date() < datetime.datetime.now().date():
                error = "Date given is not a future date" 

        if error is None:     
            command = "UPDATE USER_DATA SET USER_ID = '{uid}', DATE_T = '{date}', DESC_T = '{desc}' WHERE ENTRY_ID = {id}".format(
                uid=userID,
                date=crypticarts.encrypt(str(datime)),
                desc=crypticarts.encrypt(description),
                id = data[0])
            mysql = db.get_db()
            error = None
            conn = db.connect_db(mysql)
            cursor = conn.cursor()
            cursor.execute(command)        
            conn.commit()
            conn.close()
            flash("Entry updated")
            return redirect(url_for("reminder.modify"))

        #this is when there was an error in the post
        flash(error)
        return render_template('reminder/add.html',
            reminder_add_day_placeholder = day,
            reminder_add_month_placeholder=month,
            reminder_add_year_placeholder=year,
            reminder_add_hour_placeholder=hour,
            reminder_add_minutes_placeholder=minutes,
            reminder_add_description_placeholder = description,
            user_name = crypticarts.decrypt(current_user.uname))
    #this was a get request
    print(crypticarts.decrypt(data[3]))
    datet = datetime.datetime.strptime(crypticarts.decrypt(data[2]), '%Y-%m-%d %H:%M:%S')
    return render_template('reminder/add.html',
            reminder_add_day_placeholder = str(datet.day),
            reminder_add_month_placeholder=str(datet.month),
            reminder_add_year_placeholder=str(datet.year),
            reminder_add_hour_placeholder=str(datet.hour),
            reminder_add_minutes_placeholder=str(datet.minute),
            reminder_add_description_placeholder = crypticarts.decrypt(data[3]),
            user_name = crypticarts.decrypt(current_user.uname))

@bp.route('/delete/<key>')
@login_required
def deleteKey(key):
    userID = current_user.id
    error = None

    #the deal here is: we have an existing entry to modify 
    command = "SELECT * FROM USER_DATA WHERE ENTRY_ID = {key}".format(key = crypticarts.decrypt(key))
    mysql = db.get_db()
    conn = db.connect_db(mysql)
    cursor = conn.cursor()
    cursor.execute(command)
    data = cursor.fetchone()
    conn.close()

    #let's check if the user accessing this data is the correct user
    #you can never be to careful afterall :D
    if data is not None:
        #we foound the entry in question
        if userID == data[1]:
            #correct user access
            error = None;
            mysql = db.get_db()
            conn = db.connect_db(mysql)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM USER_DATA WHERE ENTRY_ID = {id}".format(id = data[0]))
            conn.commit()
            conn.close()
            flash("Entry deleted")
            return redirect(url_for("reminder.modify"))
        else:
            error = "Wrong Access"
    else:
        error = "No such entry"
    flash(error)
    return redirect(url_for("reminder.modify"))

    