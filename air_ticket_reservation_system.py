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

@app.route('/public_search', methods=['GET', 'POST'])
def public_search():
	#grabs information from the forms
    
    arrival_city = request.form['arrival_city']
    departure_city = request.form['departure_city']
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    print(arrival_airport)
    
	#cursor used to send queries
	#executes query
    if departure_airport and arrival_airport:
        cursor = conn.cursor()
        query1 = """select airline_name, flight_num, departure_time, 
                    arrival_time,, price, status, 
                    departure_airport, a1.city as depart_city, arrival_airport, a2.city as arrive_city, airplane_id
                    from flight f
                    join airport a1 on f.departure_airport = a1.name
                    join airport a2 on f.arrival_airport = a2.name
                    where departure_airport = '{}' and arrival_port = '{}' 
                    and departure_time like '{}%' and arrval_time like '{}%'"""
        cursor.execute(query1.format(departure_airport, arrival_airport, departure_date, arrival_date))
        data = cursor.fetchall()
        cursor.close()
    elif departure_city and arrival_city:
        cursor = conn.cursor()
        query2 = """select airline_name, flight_num, departure_time, 
                    arrival_time, price, status, 
                    departure_airport, a1.city as depart_city, arrival_airport, a2.city as arrive_city, airplane_id
                    from flight f
                    join airport a1 on f.departure_airport = a1.name
                    join airport a2 on f.arrival_airport = a2.name
                    where a1.city = '{}' and a2.city = '{}' 
                    and departure_time like '{}%' and arrival_time like '{}%'"""
        cursor.execute(query2.format(departure_city, arrival_city, departure_date, arrival_date))
        data = cursor.fetchall()
        cursor.close()
    else:
        return redirect('/')
    return render_template('public_search.html', data=data)

@app.route('/customer_login', methods = ["GET", "POST"])
def cust_login():
    return render_template('customer_login.html')

@app.route('/customer_register', methods = ["GET", "POST"])
def cust_register():
    return render_template('customer_register.html')

@app.route('/customer_logged_in', methods = ["GET", "POST"])
def cust_logged():
    cursor = conn.cursor()
    if request.form['action'] == 'register':
        email = request.form.get('email')
        name = request.form.get('name')
        building_num = request.form.get('building_num')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        passport_num = request.form.get('pp_num')
        passport_exp = request.form.get('pp_exp')
        passport_country = request.form.get('pp_country')
        dob = request.form.get('dob')
        password = str(request.form.get('pw'))
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        print(password)
        cursor.execute("select * from customer where email = '{}'".format(email))
        existing_cust = cursor.fetchall()
        if existing_cust:
            error = 'The email already existed, please use another one.'
            return render_template('customer_register.html', error=error)
        else:
            cursor.execute("INSERT INTO customer VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(email, name, password, building_num, street, city, state, phone, passport_num, passport_exp, passport_country, dob))
            conn.commit()
            cursor.close()
            return render_template('customer_login.html')

    elif request.form['action'] == 'login':
        email = request.form['email']
        password = request.form['password']
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        cursor.execute("select * from customer where email = '{}' and password = '{}'".format(email, password))
        existing_cust = cursor.fetchall()
        if existing_cust:
            cursor.close()
            session['email'] = email
            return redirect('/home')            
        else:
            error = 'Invalid login. Please register or try again'
            return render_template('customer_login.html', error = error)

@app.route('/home', methods = ["GET", "POST"])
def cust_home():
    return render_template('home.html')
app.secret_key = 'I am secret'
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug = True)