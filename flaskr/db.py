from flaskext.mysql import MySQL
from json2html import *
from . import classes



def get_db():
    global glb_mysql
    return glb_mysql

def is_email_exist(conn, email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LOGIN_CREDENTIALS WHERE EMAIL like '{email}'".format(email = email))
    data = cursor.fetchone()
    print(data)
    print(type(data))
    if(data == None):
        return False
    else:
        return True

#returns the mysql handler
def init_db(app):
    global glb_mysql
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'sql4401943'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'AXYerx4aQP'
    app.config['MYSQL_DATABASE_DB'] = 'sql4401943'
    app.config['MYSQL_DATABASE_HOST'] = 'sql4.freemysqlhosting.net'
    mysql.init_app(app)
    glb_mysql = mysql
    return mysql

#returns the connection handle
def connect_db(mysql):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("USE sql4401943")
    return conn

def json_get_login_credentials(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from LOGIN_CREDENTIALS")
    #as of right now the data in LOGIN_CREDENTIALS are ID_MAIN, USER_NAME, PASSPHRASE, EMAIL
    string_output = ""
    json_element_template = '"ID_MAIN": "{id}", "USER_NAME": "{uname}", "PASSPHRASE": "{passph}", "EMAIL": "{email}", "API_AUTHKEY": "{apikey}"'
    json_elements = []
    while(True):
        data = cursor.fetchone()
        if(type(data) != type(tuple())):
            break
        else:
            #get USER_ID

            #print(data[0])
            #print(type(data[0]))    
            #print(json_element_template.format(id=str(data[0]), uname=str(data[1]), passph=str(data[2]), email=str(data[3])))
            json_elements.append(json_element_template.format(id=str(data[0]), uname=str(data[1]), passph=str(data[2]), email=str(data[3]), apikey = str(data[4])))
    string_output += '['
    first = True
    for json in json_elements:
        if first:
            first = False
        else:
            string_output += ','
        string_output += '{'
        string_output += json
        string_output += '}'
    string_output += ']'
    return string_output

def json_get_personal_info(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from PERSONAL_INFORMATION")
    #as of right now the data in PERSONAL_INFORMATION are USER_ID, NICKNAME, FIRST_NAME, MIDDLE_NAMES, LAST_NAME, AGE
    string_output = ""
    json_element_template = '"USER_ID": "{id}", "NICKNAME": "{nname}", "FIRST_NAME": "{fname}", "MIDDLE_NAMES": "{mnames}", "LAST_NAME": "{lname}", "AGE": "{age}"'
    json_elements = []
    while(True):
        data = cursor.fetchone()
        if(type(data) != type(tuple())):
            break
        else:
            #get USER_ID

            #print(data[0])
            #print(type(data[0]))    
            json_elements.append(json_element_template.format(id=str(data[0]), nname=str(data[1]), fname=str(data[2]), mnames=str(data[3]), lname=str(data[4]), age=str(data[5])))
    string_output += '['
    first = True
    for json in json_elements:
        if first:
            first = False
        else:
            string_output += ','
        string_output += '{'
        string_output += json
        string_output += '}'
    string_output += ']'
    return string_output

def json_get_user_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from USER_DATA")
    #as of right now the data in USER_DATA are ID_MAIN, DATE, DESCRIPTION
    string_output = ""
    json_element_template = '"USER_ID": "{id}", "DATE": "{date}", "DESCRIPTION": "{descr}"'
    json_elements = []
    while(True):
        data = cursor.fetchone()
        if(type(data) != type(tuple())):
            break
        else:
            #get USER_ID

            #print(data[0])
            #print(type(data[0]))    
            json_elements.append(json_element_template.format(id=str(data[0]), date=str(data[1]), descr=str(data[2])))
    string_output += '['
    first = True
    for json in json_elements:
        if first:
            first = False
        else:
            string_output += ','
        string_output += '{'
        string_output += json
        string_output += '}'
    string_output += ']'
    return string_output

def html_format_json(data):
    return json2html.convert(json=data)

def get_html_database(mysql):
    conn = connect_db(mysql)
    cursor = conn.cursor();
    
    string_output = ""
    string_output += '{"database_name": "sql4401943", "tables" : [{"table_name":"LOGIN_CREDENTIALS","entries":'
    string_output += json_get_login_credentials(conn)
    
    string_output += '},{"table_name":"PERSONAL_INFORMATION","entries":'

    string_output += json_get_personal_info(conn)
    
    string_output += '},{"table_name":"USER_DATA","entries":'

    string_output += json_get_user_data(conn)

    string_output += '}]}'
    conn.close()

    return html_format_json('{data}'.format(data = string_output))

def getUser(id):
    conn = connect_db(get_db())
    cursor = conn.cursor();

    command = "SELECT * FROM LOGIN_CREDENTIALS WHERE USER_ID = {uid}".format(uid=id)
    cursor.execute(command)
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        return classes.User(data[0], data[1], data[2], data[3], data[4])

def getName(id):
    conn = connect_db(get_db())
    cursor = conn.cursor();

    command = "SELECT NICKNAME FROM PERSONAL_INFORMATION WHERE USER_ID = {uid}".format(uid=id)
    cursor.execute(command)
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        return data[0]


