from flask import Flask, render_template, request, url_for, redirect, session
# import pymysql
import mysql
import mysql.connector
import hashlib

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               #password='marcoli',
                               database='air_ticket_reservation_system')

@app.route('/')
def public_view(): 
    return render_template("public_view.html")

@app.route('/agent_login', methods = ["GET", "POST"])
def agent_login():
    return render_template('agent_login.html')

@app.route('/agent_register', methods = ["GET", "POST"])
def agent_register():
    return render_template('agent_register.html')

@app.route('/agent_logged_in', methods = ["GET", "POST"])
def agent_logged():
    cursor = conn.cursor()
    if request.form['action'] == 'register':
        email = request.form.get('email')
        password = str(request.form.get('password'))
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        print(password)
        cursor.execute("select COUNT(booking_agent_id) from booking_agent")
        booking_agent_id = cursor.fetchone()
        if not booking_agent_id:
            booking_agent_id = 0
        cursor.execute("select * from booking_agent where email = '{}'".format(email))
        existing_agent = cursor.fetchall()
        if existing_agent:
            error = 'The email already existed, please use another one.'
            return render_template('agent_register.html', error=error)
        else:
            cursor.execute("INSERT INTO booking_agent VALUES ('{}', '{}', '{}');".format(email, password, booking_agent_id))
            conn.commit()
            cursor.close()
            return render_template('agent_login.html')

    elif request.form['action'] == 'login':
        email = request.form['email']
        password = request.form['password']
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        print(password)
        cursor.execute("select * from booking_agent where email = '{}' and password = '{}'".format(email, password))
        existing_agent = cursor.fetchall()
        if existing_agent:
            cursor.close()
            session['email'] = email
            return redirect('/agent_home')            
        else:
            error = 'Invalid login. Please register or try again'
            return render_template('agent_login.html', error = error)

@app.route('/agent_home', methods = ["GET", "POST"])
def agent_home():
    return render_template('agent_view_flights.html')

app.secret_key = 'I am secret'
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug = True)