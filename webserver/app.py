from flask import Flask, render_template, request, make_response, redirect, url_for, session
from flask_socketio import SocketIO, send
from flask_mail import Mail, Message
import datetime
import socket
import requests
import psycopg2
from random import randint
import time
import multiprocessing

# Commented out because I keep getting errors when installing
# import RPi.GPIO as GPIO
# import lightsensor



automaticProcess = "null"
processList = []
lights = [12] #Enter the pins which are connected to the leds here
darkness = 100000 #The amount of time needed for the sensor to 'collect enough light' to turn on the lights. #The amount of time needed for the sensor to 'collect enough light' to turn on the lights.
enableLoopSensor = True





hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


app = Flask(__name__)
app.config.from_object(__name__)
templateData = {}

activeSensor = False

# Config SocketIO
app.config['SECRET_KEY'] = 'key' # todo: Change secret key to something more secure
socketio = SocketIO(app)

rooms = [{'id': '1', 'name': 'Living room'}, {'id': '2', 'name': 'Kitchen'}]

# ? Is this still necessary?
#render with template and templateData
@app.route('/')
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
    print("reset cookies")
    requests.session().cookies.clear()
    resp = make_response(render_template('main.html', **templateData))

    print(request.cookies)
    resp.set_cookie('sessionID', expires=0)
    return resp

@app.route('/home/<int:id>', methods = ['GET'])
def home(id):
     #get the sessionID and check there even an sessionID
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        query =  "SELECT COUNT(*) FROM mod5.sessions WHERE sessionid=\'"+sessionID+"\'"
        result = simpleSQLquery(query)

        # print(str(simpleSQLquery("SELECT * FROM mod5.sessions")))
        #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and return home page
        if(result[0][0] == 1):
            return render_template('views/home.html', activeRoomId=id, rooms=rooms, selected=id)
        else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
            
            resp = make_response(redirect(url_for('login')))
            resp.set_cookie('sessionID', expires=0)
            return resp
    else: #the user doesnt have an sessionID, so go to login page
        return redirect(url_for('login'))

@app.route('/components')
def components():
    components = [{'id': '0', 'name': 'Light in living room', 'gpio': '14', 'room': '1'}]
    return render_template('views/components.html', components=components, rooms=rooms)

@app.route('/users')
def users():
    return render_template('views/users.html', users=users)

# Chat
messages = [{'id': '0', 'username': 'User', 'content': 'Hello World'}]
onlineUsers = {}

@app.route('/chat/<int:id>', methods=['GET', 'POST'])
def chat(id):
    users = [{'id': '0', 'username': 'bob', 'email': 'bob@user.com'}, 
    {'id': '1', 'username': 'bobby', 'email': 'bobby@user.com'},
    {'id': '2', 'username': 'bobbo', 'email': 'bobbo@user.com'},
    
    ]
    return render_template('views/chat.html', messages=messages, users=users)    

# todo: When recipient is offline, message should be stored in database. When recipient online, recipient should receive message in real time
@socketio.on('message sent by user')
def handle_message(msg):
    print(msg)
    messages.append(msg)

    if(msg['to'] in onlineUsers):
        recipientSessionId = onlineUsers[msg['to']]
        socketio.emit('message sent to user', msg, room=recipientSessionId)
    return redirect(url_for('chat', id=msg['to']|int))
    
@socketio.on('user_connected')
def handle_join():
    # todo: Show online message
    print('user connected:')
    username = session["username"]
    onlineUsers[username] = request.sid
    print(onlineUsers)

@socketio.on('user_disconnected')
def handleDisconnect(user):
    print('user disconnected')
    del onlineUsers[user.username]
    print(onlineUsers)

# End of chat

@app.route('/login', methods = ['POST', 'GET'])
def login(): # * Same account can currently be signed in with unlimited different sessions
    results = ""
    sessionID = request.cookies.get('sessionID')
    if request.method == "POST" and not sessionID:
        #only when you do POST with no sessionID, then you can try to login with an giving sessionTOken
    
        #first get the username and password of login page.
    


        username = request.form['username']
        password = request.form['password']
        session["username"] = username
        #then check database, if credentitials correct, then create session token
        print("username: %s     password: %s ", username, password )
        
        query = f"SELECT uid FROM mod5.users WHERE username = \'{username}\' AND password = \'{password}\'"

        results = simpleSQLquery(query)

        print(str(results))
        #create session token and check if already exist session token exist
        if (results):
            userID = results[0][0] 
            print("credentitials correct!\n")
            while(True):
                sessionToken = randint(1,1000)
                print(sessionToken)

                #check if already exist
                query =  f"SELECT COUNT(*) FROM mod5.sessions WHERE sessionid=\'{sessionToken}\'"
                result = simpleSQLquery(query)
                #if the session does not yet exist, then the result should give an 0 count
                if(result[0][0] == 0):
                    query = f"INSERT INTO mod5.sessions (uid, sessionid) VALUES (\'{userID}\', \'{sessionToken}\')"
                    resultInsert = SQLqueryInsert(query)
                    if(resultInsert == "Succeeded!"): #means no Exceptions and everything went well
                        resp = make_response(redirect(url_for('home', id=0)))
                        resp.set_cookie('sessionID', str(sessionToken))
                        session["sessionId"] = sessionToken
                        #you are done and you can visit the home with an valid session token!
                        return resp
                    else: # there is an exception return it
                        resp = make_response("Something went wrong with the database: " + str(resultInsert))
                        #someting went wrong so try later agian
                        return resp 
                        
                #session does exist, so make another sessionToken, start the loop 


        else:
            resp = make_response("wrong credentitials, try again ")
        return resp


    #the rest that will be POST with a sessionID, or GET methods with/without sessionID        
    else: #check if user is logged in already for the GET login page

        sessionID = request.cookies.get('sessionID')
        if sessionID:
            query =  f"SELECT COUNT(*) FROM mod5.sessions WHERE sessionid=\'{sessionID}\'"
            result = simpleSQLquery(query)
            #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and forward home page
            if(result[0][0] == 1):
                return redirect('/home/0')
            else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
                resp = make_response(render_template('login.html'))
                resp.set_cookie('sessionID', expires=0)
                return resp
        else: #the user doesnt have an sessionID, so go to login page

            return render_template('views/login.html')

@app.route('/logout')
def logout():
    session.clear()
    # return redirect(url_for('login'))
    resp = make_response(render_template('views/login.html'))
    resp.set_cookie('sessionID', expires=0)
    return resp

# @app.route('/light', methods = ['POST'])
def switchlight():
    #check if user is logged in already for the GET login page
    print("Trying to switch light")
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        query =  f"SELECT COUNT(*) FROM mod5.sessions WHERE sessionid=\'{sessionID}\'"
        result = simpleSQLquery(query)
        #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and switch light:
        if(result[0][0] == 1):
            
            #switch light....
            print("now switch the light chosen: ")
            
            
            json_data = request.json

            switchTo = json_data["switchTo"]

            # if switchTo == "True":
            #     turn_on_lights()
            # elif switchTo == "False":
            #     turn_off_lights()

            return  switchTo


        else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
            resp = make_response(redirect(url_for('login')))
            resp.set_cookie('sessionID', expires=0)
            return resp
    
    #the user doesnt have an sessionID, therefore not privileges to chance lights

# @app.route('/lightsensor', methods = ['POST'])
def switchAutomatic():
    #check if user is logged in already for the GET login page
    print("Trying to switch light")
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        query =  f"SELECT COUNT(*) FROM mod5.sessions WHERE sessionid=\'{sessionID}\'"
        result = simpleSQLquery(query)
        #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and switch light:
        if(result[0][0] == 1):
            
            
            json_data = request.json

            switchTo = json_data["switchTo"]

            # if switchTo == "True":
            #     enableLoopSensor = True
            #     automaticProcess = multiprocessing.Process(target=automatic_lights)
            #     automaticProcess.start()
            #     processList.append(automaticProcess)
            #     return str(getStatusLight())
            # elif switchTo == "False":
            #     enableLoopSensor = False
            #     for process in processList:
            #         process.terminate()
            #     return str(getStatusLight())
                #stop the automatic-lights thread 
                


        else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
            resp = make_response(redirect(url_for('login')))
            resp.set_cookie('sessionID', expires=0)
            return resp
    
    #the user doesnt have an sessionID, therefore not privileges to chance lights

# def getStatusLight():
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setwarnings(False)
#     GPIO.setup(lights[0],GPIO.OUT)
#     return GPIO.input(lights[0])
    
# def turn_on_lights():
#     for led in lights:
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setwarnings(False)
#         GPIO.setup(led,GPIO.OUT)
#         GPIO.output(led,GPIO.HIGH)
       
        
# def turn_off_lights():
#     for led in lights:
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setwarnings(False)
#         GPIO.setup(led,GPIO.OUT)
#         GPIO.output(led,GPIO.LOW)

# def turn_on_light(pin):
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setwarnings(False)
#     GPIO.setup(pin,GPIO.OUT)
#     GPIO.output(pin,GPIO.HIGH)


# def turn_off_light(pin):
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setwarnings(False)
#     GPIO.setup(pin,GPIO.OUT)
#     GPIO.output(pin,GPIO.LOW)

# def automatic_lights():
#     turn_off_lights()
#     global enableLoopSensor
#     while enableLoopSensor:
#         print(lightsensor.get_light())
#         if lightsensor.get_light() > darkness:
#             turn_on_lights()
#             print(GPIO.input(12))
#             print("Lights are on")
#         else:
#             turn_off_lights()
#             print("Lights are off")
#             print(GPIO.input(12))
#         time.sleep(1)
#     print("end of automatic lights")







#for setting cookie
@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'GET':
        return render_template('setcookie.html')
    elif request.method == 'POST':
        user= request.form['nm']

        resp = make_response(redirect(url_for('viewcookie')))
        resp.set_cookie('cookie', user)
        return resp

#for viewing cookie
@app.route('/viewcookie')
def viewcookie():
    cookie = request.cookies.get('cookie')
    templateData = {
      'setCookieInfo' : cookie
      }
    return render_template('viewcookie.html', **templateData)



# database

"""
 connect database to server by Flask-SQLAlchemy
"""
dbhost = "bronto.ewi.utwente.nl"
dbName = 'dab_di20212b_189'
dbUser = "dab_di20212b_189"
dbPass = "x9kEMAy6W07IEd1i"

"""pip install psycopg2
connection between flask and database by Psycopg2
"""
@app.route('/db2')
def db2Test():
    query = "SELECT * FROM mod5.users"
    result = simpleSQLquery(query)
    return str(result) + "the first row and column of result will be the id of result[0][0]: " +  str(result[0][0])

@app.route('/db2sessions')
def dbSessions():
    query = "insert into mod5.sessions(sessionid, uid) values(\'6\',\'1\')"
    result = SQLqueryInsert(query)
    return "result of Inserting in session:     " + str(result)

#because INSERT, (UPDATE and DELETE) won't result any information, we dont fetch anything, but when there is an exception, we now something went wrong
def SQLqueryInsert(query):
    result = "Succeeded!"
    try:
        try:
            print('PostgreSQL in psycopg2 of the query:' + query)
            conn = psycopg2.connect(
            host=dbhost,
            database=dbUser,
            user=dbUser,
            password=dbPass)
        except:
            print("unable to connect to the database via psycopg2")

        # create a cursor
        cursor = conn.cursor()

        cursor.execute(query)

         #commit to confirm the transaction for INSERT UPDATE and DELETE
        conn.commit()
    
        # dont fetch result

        # close the communication with the PostgreSQL
        cursor.close()
    except Exception as e:
        result = "Exception: " +str(e)
        print(result)
    conn.close()
    return result

def simpleSQLquery(query):
    result = ""

    try:
        print('PostgreSQL in psycopg2 of the query:' + query)
        global conn
        conn = psycopg2.connect(
        host=dbhost,
        database=dbUser,
        user=dbUser,
        password=dbPass)
    

        # create a cursor
        cursor = conn.cursor()

        # query = "SELECT VERSION()"
        cursor.execute(query)

        # cursor.execute("CREATE TABLE mod5.test (id serial PRIMARY KEY, num integer, data varchar);")

        result = cursor.fetchall()
        print(str(result))
        # close the communication with the PostgreSQL
        cursor.close()
    except Exception as e:
        result = "Exception: " +str(e)
        print(result)
    conn.close()
    return result


print(local_ip)

if __name__ == '__main__':
    socketio.run(debug=True, host="0.0.0.0", port=8080)

# with requests.session() as s:
#     # fetch the login page
#     s.get(url)

#     # post to the login form
#     r = s.post(url1, data=payload)
#     print(r.text)
