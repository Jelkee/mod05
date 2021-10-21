from flask import Flask, render_template, request, make_response, redirect, url_for
import datetime
import socket
import requests
import psycopg2

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text




hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


app = Flask(__name__)
templateData = {}

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

@app.route('/home')
def home():
    sessionID = request.cookies.get('sessionID')
    if sessionID:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        #if logged in already, then go to home
        sessionID = request.cookies.get('sessionID')
        if sessionID:
            return redirect(url_for('home'))
        else: # user trying to log in
            #first get the username and password of login page.

            username = request.form['username']
            password = request.form['password']


            #then check database
            #if credentitials correct, then create session token

            print("username: %s     password: %s ", username, password )


            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('sessionID', "5")
            return resp

    else:
        return render_template('login.html')





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
url = "postgresql://" + dbUser + ":" + dbPass + "@" + dbhost + ":5432/" + dbName

app.config['SQLALCHEMY_DATABASE_URI'] = url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# test the database
@app.route('/database')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text



"""pip install psycopg2
connection between flask and database by Psycopg2
"""
@app.route('/db2')
def condb():
    result = ""
    try:

        try:
            print('PostgreSQL database version of psycopg2:')
            conn = psycopg2.connect(
            host=dbhost,
            database=dbUser,
            user=dbUser,
            password=dbPass)
        except:
            print("unable to connect to the database via psycopg2")

        # create a cursor
        cursor = conn.cursor()

        query = "SELECT * FROM mod5.users"
        # query = "SELECT VERSION()"
        cursor.execute(query)

        # cursor.execute("CREATE TABLE mod5.test (id serial PRIMARY KEY, num integer, data varchar);")

        # display the PostgreSQL database server version
        result = cursor.fetchone()
        print(str(result))
        # close the communication with the PostgreSQL
        cursor.close()
    except Exception as e:
        print(e)
        return str(result)
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)




print(local_ip)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


# with requests.session() as s:
#     # fetch the login page
#     s.get(url)

#     # post to the login form
#     r = s.post(url1, data=payload)
#     print(r.text)
