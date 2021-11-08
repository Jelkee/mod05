from flask import Flask, render_template, request, flash, make_response, redirect, url_for, session
from flask_socketio import SocketIO, send
from flask_mail import Mail, Message
import datetime
import socket
import requests
import psycopg2
from random import randint
import time
import multiprocessing
import operator

# import RPi.GPIO as GPIO
# import lightsensor
import string
import random


from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


automaticProcess = "null"
processList = [] 
lights = [11,12] #Enter te pins which are connected to the leds here    # 7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 35, 36, 37, 38, 40
darkness = 100000 #The amount of time needed for the sensor to 'collect enough light' to turn on the lights. #The amount of time needed for the sensor to 'collect enough light' to turn on the lights.





hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


app = Flask(__name__)
app.config.from_object(__name__)
templateData = {}

activeSensor = False

# Config SocketIO
app.config['SECRET_KEY'] = 'key' # todo: Change secret key to something more secure
socketio = SocketIO(app)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'group312021@gmail.com',
    "MAIL_PASSWORD": 'JouwMoeder2021'
}

app.config.update(mail_settings)
mail = Mail(app)
s = URLSafeTimedSerializer('thisisasecret')
broadcastMessage = False
randomSaltBroadcast = None
allemails = []
usersNotHome = []


#-------------------MAILING---------



# Send email to everyone that is a user in database
@app.route('/mail')
def mailHello():
    #you can only do this when you are admin:
    sessionID = request.cookies.get('sessionID')

    if sessionID:
        # query = f"SELECT COUNT(*),lastactive FROM mod5.sessions WHERE sessionid=\'{sessionID}\' GROUP BY lastactive"
        # result = simpleSQLquery(query)

        # print(str(simpleSQLquery("SELECT * FROM mod5.sessions")))
        # if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and return home page
        if hasValidSessionId(sessionID):
            return broadcastAll()
        else:  # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
            return resetSessionID(sessionID)
    else:  # the user doesnt have an sessionID, so go to login page
        return redirect(url_for('login'))


      
def broadcastAll():
    # encrypts a token form the email
        #randomize salt:
    global randomSaltBroadcast
    randomSaltBroadcast = randomSalt(20)
    print(randomSaltBroadcast)
    global broadcastMessage
    broadcastMessage = True
    #Get all Users Emails to send them a broadcast
    query = " SELECT email FROM mod5.users"
    result = simpleSQLquery(query)
    global allemails
    allemails = []
    for resultrow in result:
        allemails.append(resultrow[0])
    print(str(allemails))
    returnmsg = ""

    for email in allemails:
        token = s.dumps(email, salt=randomSaltBroadcast)
        linkAtHome = url_for('confirm_mail', token=token, AtHome="True", _external=True)
        linkNotHome = url_for('confirm_mail', token=token, AtHome="False", _external=True)
        msg = Message(subject="Confirm",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=[email],
                        body="Send Email using Your Flask App\n"
                            + "Are you at home? Then click on this Link {} \n".format(linkAtHome)
                            + "Are you not at Home? Then click on this link {} \n".format(linkNotHome))
        mail.send(msg)
        returnmsg+="<h1>mail has been sent to this email address: {} And with the token: {}</h1>".format(email, token)
    return returnmsg


def randomSalt(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/confirm_mail/<token>/<AtHome>', methods=['GET'])
def confirm_mail(token, AtHome):
    # decrypts the token from email
    # and get the info for home or not
    
    global broadcastMessage
    print("Broadcast is:"+str(broadcastMessage))
    if broadcastMessage:
        try:
            # first check if the token is still valid with max_age.
            print("check email")
            global randomSaltBroadcast
            email = s.loads(token, salt=randomSaltBroadcast, max_age=120)  # in seconds
            # then check if valid email and if its not registered yet if user is home or not
            validemail = allemails.count(email)
            alreadyregistered = usersNotHome.count(email)
            print("check validation for emails: {} + count: {} and usersNotHome: {} + count: {}".format(str(allemails), str(validemail) ,str(usersNotHome), str(alreadyregistered)))
            if validemail == 1 and alreadyregistered == 0:  # means a user with this email exists and not yet registered
                print(AtHome)
                if AtHome == "False":  # means user is not home
                    usersNotHome.append(email)
                    print("append mail in usersNotHome: {}".format(str(usersNotHome)))
                    # when the everyone is not at home, then you can turn all the lights off:
                    if len(usersNotHome) == len(allemails):  # means everyone has replied
                        print("Everyone has replied")
                        broadcastMessage = False
                        # turn automatic sensor and lights off
                       
                        for process in processList:
                            process[1].terminate()
                            process[1].join()
                        #TODO: now turn off all the LIGHTS!

                        # turn_off_lights()
                        return ("you have succesfully registered with email: {} such that you are Not at Home!\n".format(email) +
                           "everyone has replied that they are not at home, therefore all lights will be turned off")
                               
                    else: #not everyone has not yer replied to broadcast
                        print(usersNotHome)
                        return "you have succesfully registered with email: {} such that you are Not at Home!".format(email)

                elif AtHome == "True":  # someone is atHome, therefore don't turn any light off and disable broadcast
                    broadcastMessage = False
                    randomSaltBroadcast=None
                    return "you have succesfully registered with email: {} such that you are at Home! \nTherefore no lights will be turned off".format(email)
                else:  # THere is other Value then expected, stop searching
                    return "Invalid registration"
            elif validemail == 1 and alreadyregistered == 1:  # means user with this email but already registered
                return "you have already registered with your email"
            elif validemail == 0:
                return "Invalid registration"
        except SignatureExpired:
            # , if token expired, then you can stop the broadcasting
            broadcastMessage = False
            randomSaltBroadcast =None
            return "token is expired with AtHome value: {}".format(AtHome)
    else:  # no need to do anything because broacasting is off
        return "there is no ongoing broadcasting messaging right now"

#-----------------MAILING----------------^^^^^^


def hasValidSessionId(sessionID):
    if sessionID:
        query = f"SELECT COUNT(*),lastactive FROM mod5.sessions WHERE sessionid=\'{sessionID}\' GROUP BY lastactive"
        result = simpleSQLquery(query)
        # if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and forward home page
        if (result !=[]  and result[0][0] == 1 and not lastActiveTimeout(sessionID, result[0][1])):
            return True
        else: 
            return False
    else:
        return False


def resetSessionID(sessionID):
    datetimeTimeOut = datetime.now() - timedelta(minutes=5)
    # query= f"DELETE FROM mod5.sessions WHERE sessionid=\'{sessionID}\'"
    query= f"DELETE FROM mod5.sessions WHERE lastactive <=\'{datetimeTimeOut}\'"
    SQLqueryInsert(query)
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('sessionID', expires=0)
    return resp

#check for inactive, and if no timeout(5 minutes, 300 seconds) yet, change lastactive time to current:
#this function will only be checked if the sessionID is in the table!! because of logical and
def lastActiveTimeout(sessionID, lastactivedb):
    #returns true if timeout or invalid sessionID therefore sessionID is invalid
    #returns false if no timeout and extends your time with updating the lastactive time
    
    # lastActive = datetime.strptime(result[0][0], "%Y-%m-%d %H:%M:%S.%f")
    diff = (datetime.now() - lastactivedb).total_seconds()
    print(diff)
    if diff > 300: #invalid
        return True
    else: #it is still valid, so change the lastactive to now
        now = datetime.now()
        query = f"UPDATE mod5.sessions SET lastactive = \'{now}\' WHERE sessionid=\'{sessionID}\'"
        SQLqueryInsert(query)
        print(f"Change the lastactive time to now,{now} , for sessionID: {sessionID}")
        return False




@app.route('/')
def redirectToHome():
    SQLqueryInsert("DELETE FROM mod5.sessions")
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            return redirect('/home/0')
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

# Redirect to home
@app.route('/home')
def redirect_to_home():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            return redirect('/home/0')
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))


@app.route('/home/<int:id>', methods = ['GET'])
def home(id):
     #get the sessionID and check there even an sessionID
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        

        # print(str(simpleSQLquery("SELECT * FROM mod5.sessions")))
        #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and return home page
        if hasValidSessionId(sessionID):
            return render_template('views/home.html', activeRoomId=id, rooms=fetchAllRooms(), selected=id, components=fetchAllComponents())
        else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
            return resetSessionID(sessionID)
    else: #the user doesnt have an sessionID, so go to login page
        return redirect(url_for('login'))

# Rooms CRUD
def fetchAllRooms():
    roomList = []
    query = 'SELECT * FROM "mod5"."rooms";'
    result = simpleSQLquery(query)

    # Convert tuple to dict
    for i in range(len(result)):
        id = result[i][0]
        name = result[i][1]
        description = result[i][2]
        roomList.append({'id': id, 'name': name, 'description': description})
    roomList.sort(key=operator.itemgetter('id'))
    return roomList

@app.route('/rooms')
def rooms():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            return render_template('views/rooms.html', rooms=fetchAllRooms(), showModal=-2)
        else:
            return resetSessionID(sessionID)
    else:    
        return redirect(url_for('login'))

@app.route('/rooms/add', methods=['GET', 'POST'])
def addRoom():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            if request.method == 'POST': # If new room is added
                name = request.form['name']
                query= f"INSERT INTO mod5.rooms (name) VALUES (\'{name}\');"
                SQLqueryInsert(query)
                return redirect('/rooms')
            else: # If rooms page is visited
                return render_template('views/rooms.html', rooms=fetchAllRooms(), showModal=-1)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

@app.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
def editRoom(id):
    sessionID = request.cookies.get('sessionID')
    if sessionID:

        if hasValidSessionId(sessionID):
            if request.method == 'POST':
                name = request.form['name']
                query= f"UPDATE mod5.rooms SET name = \'{name}\'WHERE roomid={id};"
                SQLqueryInsert(query)
                return redirect('/rooms')
            else:
                return render_template('views/rooms.html', rooms=fetchAllRooms(), showModal=id)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

def isRoomReferenced(id):
    query = f"SELECT * FROM mod5.rooms WHERE roomid={id};"
    result = simpleSQLquery(query)
    print(result)
    return (len(result) > 0) # Check if room still contains lights

@app.route('/rooms/delete/<int:id>')
def deleteRoom(id):
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            # if(isRoomReferenced(id)):
            #     flash("Please remove all lights from the room before removing it", "info")
            #     return render_template('views/rooms.html', rooms=fetchAllRooms(), showModal=-2)
            # else:
            query = f"DELETE FROM mod5.rooms WHERE roomid={id} RETURNING *;"
            SQLqueryInsert(query)
            return redirect('/rooms')
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

# Lights CRUD
@app.route('/components')
def components():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            return render_template('views/components.html', components=fetchAllComponents(), rooms=fetchAllRooms(), showModal=-2)
        else:
            return resetSessionID(sessionID)
    else:    
        return redirect(url_for('login'))

def fetchAllComponents():
    componentList = []
    queryLights = 'SELECT * FROM mod5.lights;'
    querySensors = 'SELECT * FROM mod5.lightsensor;'
    lights = simpleSQLquery(queryLights)
    sensors = simpleSQLquery(querySensors)

    # Convert tuple to dict
    for i in range(len(lights)):
        id = lights[i][0]
        name = lights[i][1]
        status = lights[i][2]
        room = lights[i][3]
        gpio = lights[i][4]
        type = 'light'
        componentList.append({'id': id, 'name': name, 'status': status, 'room': room, 'gpio': gpio, 'type': type})
    
    for i in range(len(sensors)):
        id = sensors[i][0]
        name = sensors[i][1]
        room = sensors[i][2]
        gpio = sensors[i][3]
        connected = sensors[i][4]
        status = sensors[i][5]
        type = 'sensor'
        componentList.append({'id': id, 'name': name, 'room': room, 'gpio': gpio, 'connected': connected, 'status': status, 'type': type})

    componentList.sort(key=operator.itemgetter('id'))
    return componentList

@app.route('/components/add', methods=['GET', 'POST'])
def addComponent():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            if request.method == 'POST': # If new component is added
                name = request.form['name']
                room = request.form['room']
                gpio = request.form['gpio']
                type = request.form['type']
                if type == 'sensor':
                    connected = request.form['connected']
                    query = f"INSERT INTO mod5.lightsensor(name, roomid, gpio, lightid, status) VALUES (\'{name}\', \'{room}\', \'{gpio}\', \'{connected}\', \'OFF\')"
                else: # Type == 'light'
                    query= f"INSERT INTO mod5.lights (name, status, roomid, gpio) VALUES (\'{name}\', \'OFF\', \'{room}\', \'{gpio}\');"
                    
                SQLqueryInsert(query)
                return redirect('/components')
            else: # If components page is visited
                return render_template('views/components.html', components=fetchAllComponents(), rooms=fetchAllRooms(), showModal=-1)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

@app.route('/components/edit/<type>/<int:id>', methods=['GET', 'POST'])
def editComponent(id, type):
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            if request.method == 'POST':
                name = request.form['name']
                room = request.form['room']
                gpio = request.form['gpio']
                if type == 'sensor':
                    connected = request.form['connected']
                    query= f"UPDATE mod5.lightsensor SET name = \'{name}\', roomid = \'{room}\', gpio = \'{gpio}\', lightid = \'{connected}\' WHERE sensorid={id};"
                else:
                    query= f"UPDATE mod5.lights SET name = \'{name}\', roomid = \'{room}\', gpio = \'{gpio}\' WHERE lightid={id};"
                SQLqueryInsert(query)
                return redirect('/components')
            else:
                return render_template('views/components.html', components=fetchAllComponents(), rooms=fetchAllRooms(), showModal=id, compType=type)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

@app.route('/components/delete/<type>/<int:id>')
def deleteComponent(id, type):
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            if type == 'sensor':
                query = f"DELETE FROM mod5.lightsensor WHERE sensorid={id} RETURNING *;"
            else:
                query = f"DELETE FROM mod5.lights WHERE lightid={id} RETURNING *;"
            SQLqueryInsert(query)
            return redirect('/components')
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

# Users CRUD
def fetchAllUsers():
    userList = []
    query = 'SELECT * FROM "mod5"."users";'
    result = simpleSQLquery(query)

    # Convert tuple to dict
    for i in range(len(result)):
        id = result[i][0]
        username = result[i][1]
        type = result[i][3]
        email = result[i][4]
        userList.append({'id': id, 'username': username, 'email': email, 'type': type})
    userList.sort(key=operator.itemgetter('id'))
    return userList

@app.route('/users')
def users():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            userList = fetchAllUsers()
            return render_template('views/users.html', users=userList, showModal=-2)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

@app.route('/users/add', methods=['GET', 'POST'])
def addUser():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            if request.method == 'POST': # If new component is added
                email = request.form['email']
                username = request.form['username']
                password = request.form['password']
                type = request.form['type']
                query= f"INSERT INTO mod5.users (username, password, type, email) VALUES (\'{username}\', \'{password}\', \'{type}\', \'{email}\');"
                SQLqueryInsert(query)
                return redirect('/users')
            else: # If components page is visited
                return render_template('views/users.html', users=fetchAllUsers(), showModal=-1)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def editUser(id):
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            if request.method == 'POST':
                email = request.form['email']
                username = request.form['username']
                password = request.form['password']
                type = request.form['type']
                query= f"UPDATE mod5.users SET email = \'{email}\', username = \'{username}\', password = \'{password}\', type = \'{type}\' WHERE uid={id};"
                SQLqueryInsert(query)
                return redirect('/users')
            else:
                return render_template('views/users.html', users=fetchAllUsers(), showModal=id)
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

@app.route('/users/delete/<int:id>')
def deleteUser(id):
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        if hasValidSessionId(sessionID):
            query = f"DELETE FROM mod5.users WHERE uid={id} RETURNING *;"
            SQLqueryInsert(query)
            return redirect('/users')
        else:
            return resetSessionID(sessionID)
    else:
        return redirect(url_for('login'))

# Chat CRUD
messages = []
onlineUsers = {}

@app.route('/chat/<int:id>', methods=['GET', 'POST'])
def chat(id):
    userList = fetchAllUsers()
    return render_template('views/chat.html', messages=messages, users=userList)    

# todo: When recipient is offline, message should be stored in database. When recipient online, recipient should receive message in real time
@socketio.on('message sent by user')
def handle_message(msg):
    print(msg)
    messages.append(msg)

    if(msg['to'] in onlineUsers):
        recipientSessionId = onlineUsers[msg['to']]
        socketio.emit('message sent to user', msg, room=recipientSessionId)
    # return redirect(url_for('chat', id=msg['to']))
    
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

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/chat-new')
def chatNew():
    return render_template('views/chat-3.html')

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
                    now = datetime.now()
                    query = f"INSERT INTO mod5.sessions (lastactive, uid, sessionid) VALUES (\'{now}\',\'{userID}\', \'{sessionToken}\')"
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
           
            #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and forward home page
            if hasValidSessionId(sessionID):
                return redirect('/home/0')
            else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
                return resetSessionID(sessionID)
        else: #the user doesnt have an sessionID, so go to login page
            return render_template('views/login.html')

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(render_template('views/login.html'))
    resp.set_cookie('sessionID', expires=0)
    return resp

# @app.route('/light', methods = ['POST'])
# def switchlight():
#     #check if user is logged in already for the GET login page
    
#     sessionID = request.cookies.get('sessionID')
#     if sessionID:
      
#         #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and switch light:
#         if hasValidSessionId(sessionID):
            
#             #switch light....
#             print("now switch the light chosen: ")
            
            
#             json_data = request.json

#             switchTo = json_data["switchTo"]
#             lightID = json_data["lightID"]

#             print("Trying to switch the lightID: " + str(lightID))

#             #get the GPIO PIN:
#             query = f"SELECT gpio FROM mod5.lights WHERE lightid = \'{lightID}\'"
#             result = simpleSQLquery(query)
#             if result !=[]:
#                 gpioPin = result[0][0]
#                 alternate = ""
#                 if switchTo == "True":
#                     alternate = "Turn On"
#                     turn_on_light(gpioPin)
#                       query = f"UPDATE mod5.lights SET status = \'ON\' WHERE lightid=\'{lightID}\'"
#                       SQLqueryInsert(query)
#                 elif switchTo == "False":
#                     alternate = "Turn Off"
#                     turn_off_light(gpioPin)
#                       query = f"UPDATE mod5.lights SET status = \'OFF\' WHERE lightid=\'{lightID}\'"
#                       SQLqueryInsert(query) 
#                 print(alternate +"the light for lightid: "+str(lightID) + ", GPIO pin: " + str(gpioPin) +
#                 " and Now the status is: "+str(getStatusLight(gpioPin)))
                
#                 return  switchTo
#             else:
#                 return "couldn't find the gpio pin for this light"
            

#         else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
#             return resetSessionID(sessionID)
#     else: #the user doesnt have an sessionID, therefore not privileges to chance lights
#         return redirect(url_for('login'))

# @app.route('/lightsensor', methods = ['POST'])
# def switchAutomatic():
#     #check if user is logged in already for the GET login page
#     print("Trying to switch light")
#     sessionID = request.cookies.get('sessionID')
#     if sessionID:
#         #if the sessionID is exist and it is valid(within timeout), then the result should give an 1 count and switch light:
#         if hasValidSessionId(sessionID):
            
#             json_data = request.json

#             switchTo = json_data["switchTo"]
#             lightID = json_data["lightID"] #of the light that you want to automate
#             #searching for a automatic sensor that this lightid
#             query = f"SELECT l.gpio, s.gpio, s.sensorid FROM mod5.lights l, mod5.lightsensor s WHERE l.lightid=\'{lightID}\' AND l.lightid=s.lightid"
#             result = simpleSQLquery(query)
#             lightgpio = result[0][0]
#             sensorgpio = result[0][1]
#               sensorId = result[0][2]
#             print("lightGPIO: "+ str(lightgpio) + " and sensorGPIO: "+str(sensorgpio))

#             if switchTo == "True":
#                 #still need to know when the automatic is already on, dont create another process
#                 #delete the old ones and add new process
#                 for process in processList:
#                     if(process[0] == lightgpio):
#                         process[1].terminate()
#                         processList.remove(process)
#                         print("delete process of lightgpio: " + str(lightgpio))

#                 automaticProcess = multiprocessing.Process(target=automatic_lights, args=(lightgpio, sensorgpio))
#                 automaticProcess.start()
#                 processList.append([lightgpio, automaticProcess])
#                 print("after enable process: "+str(processList))
#                   query = f"UPDATE mod5.lightsensor SET status = \'ON\' WHERE sensorid=\'{sensorId}\'"
#                   SQLqueryInsert(query)
#                 return str(getStatusLight(lightgpio))
#             elif switchTo == "False":
#                 for process in processList:
#                     if(process[0] == lightgpio):
#                         process[1].terminate()
#                         process[1].join()
#                         processList.remove(process)
#                 print("After disable process: "+str(processList))
#                   query = f"UPDATE mod5.lightsensor SET status = \'OFF\' WHERE sensorid=\'{sensorId}\'"
#                   SQLqueryInsert(query)
#                 return str(getStatusLight(lightgpio))
#                 #stop the automatic-lights thread 
                

#         else: # the sessionID is invalid therefore maybe delete invalid id in database? but especially for the user
#             return hasValidSessionId(sessionID)
    
#     else: #the user doesnt have an sessionID, therefore not privileges to chance lights
#         return resetSessionID(sessionID)

# def getStatusLight(pin):
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setwarnings(False)
#     GPIO.setup(pin,GPIO.OUT)
#     return GPIO.input(pin)
    
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



# def automatic_lights(lightPin, sensorPin):
#     turn_off_light(lightPin)
#     while True:
#         timeget = lightsensor.get_light(sensorPin)
#         print("Time to get light: "+str(timeget))
#         if timeget > darkness:
#             turn_on_light(lightPin)
#             print("Lights are on")
#         else:
#             turn_off_light(lightPin)
#             print("Lights are off")
#         # print(GPIO.input(lightPin))
#         time.sleep(1)







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
    socketio.run(app, debug=True, host="0.0.0.0", port=8080)

# with requests.session() as s:
#     # fetch the login page
#     s.get(url)

#     # post to the login form
#     r = s.post(url1, data=payload)
#     print(r.text)
