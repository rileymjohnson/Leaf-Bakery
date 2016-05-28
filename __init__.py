from flask import Flask, render_template, request, session, redirect, url_for, make_response
import MySQLdb as mdb
from flask_sslify import SSLify
import json
import operator
import decimal
import datetime
import calendar
import smtplib
import math
import hashlib
import requests
app = Flask(__name__)

#random functions
def toModifiedDayOfWeek(day): #this function is just used for converting a python day number to a js day number
	if day == 6:
		return 0
	else:
		return day + 1
def getHour(hour):
	if hour > 12:
		return str(hour - 12) + " p.m."
	return str(hour) + " a.m."
def kToF(t):
	#return (t*9/5.0)-459.67
	return t - 273
def chunks(l, n):
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]
def getColor(a):
	colors = ["#f44336", "#e91e63", "#9c27b0", "#673ab7", "#3f51b5", "#2196f3", "#03a9f4", "#00bcd4", "#009688", "#4caf50", "#8bc34a", "#cddc39", "#ffeb3b", "#ffc107", "#ff9800", "#ff5722", "#795548", "#9e9e9e", "#607d8b"]
	return colors[a % len(colors)]
def getHighlights(a):
	highlights = ["#ef5350", "#ec407a ", "#ab47bc", "#7e57c2", "#5c6bc0", "#42a5f5", "#29b6f6", "#26c6da", "#26a69a", "#66bb6a", "#9ccc65", "#d4e157", "#ffee58", "#ffca28", "#ffa726", "#ff7043", "#8d6e63", "#bdbdbd", "#78909c"]
	return highlights[a % len(highlights)]
def numToDay(num):
	days = []
	days.append('mon')
	days.append('tue')
	days.append('wed')
	days.append('thu')
	days.append('fri')
	days.append('sat')
	days.append('sun')
	return days[num-1]
def monthToNum(date):
	return{'Jan' : 1,'Feb' : 2,'Mar' : 3,'Apr' : 4,'May' : 5,'Jun' : 6,'Jul' : 7,'Aug' : 8,'Sep' : 9, 'Oct' : 10,'Nov' : 11,'Dec' : 12}[date]
def numToMonth(n):
	t = []
	t.append("January")
	t.append("Frebruary")
	t.append("March")
	t.append("April")
	t.append("May")
	t.append("June")
	t.append("July")
	t.append("August")
	t.append("September")
	t.append("October")
	t.append("November")
	t.append("December")
	return t[n-1]

def send_email(user, pwd, recipient, subject, body):
	gmail_user = user
	gmail_pwd = pwd
	FROM = user
	TO = recipient if type(recipient) is list else [recipient]
	SUBJECT = subject
	TEXT = body
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
	except:
		print "failed to send mail"

def send_email_member(user, pwd, recipient, subject, body):
	gmail_user = user
	gmail_pwd = pwd
	FROM = user
	mems = getMembers()
	m = []
	for i in mems:
		m.append(i['email'])
	#TO = recipient if type(recipient) is list else [recipient]
	#TO = ['rileymillerjohnson@gmail.com', 'rmjohnson@students.chccs.k12.nc.us']
	TO = m
	SUBJECT = subject
	TEXT = body
	message = """\From: %s\nTO: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
	except:
		print "failed to send mail"

def send(email, phone, subject, message):
	m = getEmail()
	message = "Email: " + email + "\n" + "Phone: " + phone + "\n" + "Subject: " + subject + "\n" + "Message: " + message
	send_email("norepleyleaf@gmail.com", "visibilitymatters", m, "Customer Contact", message)

def sendToMembers(message):
	send_email_member("norepleyleaf@gmail.com", "visibilitymatters", "sample", "Leaf Loyalty Program", message)

def encrypt(a):
	return hashlib.sha512(a).hexdigest()

#ordering functions
def addItem(i, t, notes, amount):
	it = {}
	it["id"] = i
	it["type"] = t
	it["notes"] = notes
	it["amount"] = str(amount)
	if 'order' in session:
		it["number"] = len(session["order"])
		session["order"].append(it)
	else:
		it["number"] = 0
		session["order"] = []
		session["order"].append(it)

#database query functions
def getItems(option): #returns list of any type of food. ex: appetizers
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from " + option + " where status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getItemItem(option, i): #returns certain food
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from " + option + " where ID =" + str(i) + " and status = 1;"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getItem(option, i): #returns certain food
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from " + option + " where ID=" + str(i) + ";"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows
def getEvents(): #returns list of event
	#gets current dates
	today = datetime.date.today()
	test = today.strftime('We are the %d, %b %Y')
	day = str(today.strftime('%d'))
	mo = today.strftime('%b')
	month = str(monthToNum(mo))
	year = str(today.strftime('%Y'))

	#gets database info
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from events where year > " + year + " or (year = " + year + " and month > " + month + ") or (year = " + year + " and month = " + month + " and day >= " + day + ")"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	values = sorted(rows, key = lambda user: (user['year'], user['month'], user['day']))
	return values
def getSpecficEvent(i): #returns a single event
	#gets current dates
	today = datetime.date.today()
	test = today.strftime('We are the %d, %b %Y')
	day = str(today.strftime('%d'))
	mo = today.strftime('%b')
	month = str(monthToNum(mo))
	year = str(today.strftime('%Y'))
	#gets database info
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from events where (year > " + year + " or (year = " + year + " and month > " + month + ") or (year = " + year + " and month = " + month + " and day >= " + day + ")) and id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	values = sorted(rows, key = lambda user: (user['year'], user['month'], user['day']))
	return values
def getEmail(): #gets the admin email
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from email"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]["email"]
def getUser(): #returns the user name
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from user"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]["user"]
def getPassword(): #returns the password
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from password"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]["password"]

def insertOrder(t, name, address, notes, j): #adds an order
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into orders (type, name, address, note, items) values ('" + t + "', '" + name + "', '" + address + "', '" + notes + "', '" + j + "');"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def addReservation(name, phone, people, details, time, day, month, year): #adds a reservation
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into reservations (name, phone, people, details, time, day, month, year) values ('" + name + "', '" + phone + "', " + people + ", '" + details + "', '" + time + "', " + day + ", " + month + ", " + year + ")"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def getAdmins(name): #gets all the admins
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from admin where name = '" + name + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def addToStats(t, day, amount, i): #add to the stats tables
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update " + t + "num set " + day + " = " + day + " + " + amount + " where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def addToStats(t, day, amount, i): #add to the stats tables
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update " + t + "num set " + day + " = " + day + " + " + amount + " where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def getItemInfo(t): #gets all the admins
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from " + t + "num where status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getNumberOfItems(t): #gets all the admins
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from " + t + " where status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return len(rows)

def getItemName(i, cat): #gets all the admins
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select name from " + cat + " where ID = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]['name']

def getItemNames(cat): #gets all the admins
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select name from " + cat + " where status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getReservations(): #gets all the reservations
	today = datetime.date.today()
	test = today.strftime('We are the %d, %b %Y')
	day = str(today.strftime('%d'))
	mo = today.strftime('%b')
	month = str(monthToNum(mo))
	year = str(today.strftime('%Y'))
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from reservations where year > " + year + " or (year = " + year + " and month > " + month + ") or (year = " + year + " and month = " + month + " and day >= " + day + ")"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	values = sorted(rows, key = lambda user: (user['year'], user['month'], user['day']))
	return values

def getOrders(): #gets all the orders
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from orders where date >= curdate()"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getSpecificOrder(i): #gets a specific order
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from orders where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getSpecificItem(cat, i): #gets a specific item
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select name from " + cat + " where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def deleteOrder(i): #deletes an order based on its id
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "delete from orders where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getHours(): #get list of hours
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from hours"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def updateHour(day, start, end, o): #updates one houe
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update hours set start = " + start + ", end = " + end + ", open = " + o + " where day = '" + day + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getUsers(): #gets all the users
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from admin"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def ifUserExists(n): #if user exists
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select name from admin where name = '" + n + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return len(rows)

def addUser(name, password): #adds a user
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into admin (name, password) values ('" + name + "', '" + encrypt(password) + "')"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def deleteUser(i): #deletes a user
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "delete from admin where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def chosenUpdate(): #if user exists
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select name, id from admin"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getPasswordForCheck(i): #gets the user password
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select password from admin where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def changePassword(i, password): #changes a users password
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update admin set password = '" + encrypt(password) + "' where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def addEvent(name, description, year, month, day): #adds an event
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into events (name, des, year, month, day) values ('" + name + "', '" + description + "', " + year + ", " + month + ", " + day + ")"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def deleteEvent(i): #deletes an event
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "delete from events where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def getEmail(): #gets the admin email address
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select email from email"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[0]['email']

def updateEmail(email): #updates the admin email address
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update email set email = '" + email + "'"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def addmenuitem(category, name, shortdes, longdes, price): #adds a menu item
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into " + category + " (name, shortDes, longDes, location, price) values ('" + name + "', '" + shortdes + "', '" + longdes + "', '../static/menu/img.jpg', " + price + ")"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def getMenuItemId(category): #adds a menu item
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select id from " + category
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows[len(rows)-1]['id']


def addNumRecord(category, i): #updates the admin email address
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into " + category + "num (id, mon, tue, wed,thu, fri, sat, sun) values (" + i + ",0,0,0,0,0,0,0)"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def changeLocation(category, i): #changes the image file location in the database
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update " + category + " set location = '/tmp/menu/" + category + "/img" + i + ".jpg' where id = " + i
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def addMember(name, email, phone): #adds a member
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into members values ('" + name + "', '" + email + "', '" + phone + "')"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

def getMembers(): #gets a list of the members
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from members"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

#app error pages
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('errorpages/error.html', error="500", desc="Internal Server Error"), 500

@app.errorhandler(410)
def gone(e):
	return render_template('errorpages/error.html', error="410", desc="Page Was Deleted"), 410

@app.errorhandler(405)
def method_not_allowed(e):
	return render_template('errorpages/error.html', error="405", desc="Method Not Allowed"), 405

@app.errorhandler(404)
def pages_not_found(e):
	return render_template('errorpages/error.html', error="404", desc="Page Not Found"), 404

@app.errorhandler(403)
def forbidden(e):
	return render_template('errorpages/error.html', error="403", desc="Forbidden"), 403

@app.errorhandler(402)
def payment_required(e):
	return render_template('errorpages/error.html', error="402", desc="Payment Required"), 402

@app.errorhandler(401)
def unauthorized(e):
	return render_template('errorpages/error.html', error="401", desc="Unauthorized"), 401

@app.errorhandler(400)
def bad_request(e):
	return render_template('errorpages/error.html', error="400", desc="Bad Request"), 400

#app pages
@app.route('/')
def index():
	hours = getHours()
	hourComplete = []
	for i in hours:
		if i['open'] == 0:
			hourComplete.append(["false", 0, 0])
		else:
			hourComplete.append(['true', getHour(i['start']), getHour(i['end'])])
	return render_template("index.html", hours=hourComplete)

@app.route('/contact', methods=["GET", "POST"])
def contact():
	if request.method == "GET":
		return render_template("contact.html")
	if request.method == "POST":
		opt = request.form
		email = opt["email"]
		phone = opt["phone"]
		subject = opt["subject"]
		message = opt["message"]
		send(email, phone, subject, message)
		session["justcontact"] = "true"
		return redirect("/success")

@app.route('/success')
def success():
	if 'justcontact' in session:
		session.pop('justcontact', None)
		return render_template("emailsuccess.html")
	else:
		return redirect("/")

@app.route('/menu')
def menu():
	menupage = True
	return render_template("menu.html", menupage=menupage)

#Admin Panel Files Imports End
@app.route('/order', methods=['GET', 'POST'])
def order():
	if request.method == "GET":
		if "order" in session:
			t = []
			for i in session["order"]:
				s = {}
				s["notes"] = i["notes"]
				s["number"] = i["number"]
				s["amount"] = i["amount"]
				n = getItem(i["type"], i["id"])
				s["name"] = n[0]["name"]
				s["price"] = n[0]["price"]
				t.append(s)
			totalprice = 0
			for p in t:
				totalprice += float(p['price']) * int(p['amount'])
			return render_template("order.html", items=t, totalprice='%.2f' % totalprice)
		else:
			return render_template("orderBad.html")
	if request.method == "POST":
		i = request.form["id"]
		t = request.form["type"]
		amount = request.form["amount"]
		notes = request.form["notes"]
		addItem(i, t, notes, amount)
		if "order" in session:
			t = []
			for i in session["order"]:
				s = {}
				s["notes"] = i["notes"]
				s["amount"] = i["amount"]
				n = getItem(i["type"], i["id"])
				s["name"] = n[0]["name"]
				s["price"] = n[0]["price"]
				t.append(s)
			totalprice = 0
			for p in t:
				totalprice += float(p['price']) * int(p['amount'])
			return render_template("order.html", items=t, totalprice='%.2f' % totalprice)
		else:
			return render_template("orderBad.html")

@app.route('/confirmorder')
def orderreviewflask():
	if "order" in session:
		t = []
		for i in session["order"]:
			s = {}
			s["notes"] = i["notes"]
			s["number"] = i["number"]
			s["amount"] = i["amount"]
			n = getItem(i["type"], i["id"])
			s["name"] = n[0]["name"]
			s["price"] = n[0]["price"]
			t.append(s)
		total = 0
		for p in t:
			total += float(p['price']) * int(p['amount'])
		return render_template("orderreview.html", items=t, total='%.2f' % total)
	else:
		return render_template("orderBad.html")

@app.route('/orderdetails')
def orderdetailsflask():
	session['ordering'] = "true"
	return render_template("orderdetails.html")

@app.route('/ordered', methods=['POST'])
def orderedflask():
	if 'ordering' in session:
		for item in session['order']:
			t = item['type']
			i = item['id']
			amount = item['amount']
			day = numToDay(int(datetime.date.today().strftime("%w")))
			addToStats(t, day, amount, i)
		session.pop("ordering", None)
		if request.form['option'] == "pick":
			opt = "pick"
			name = request.form['pickname']
			comment = request.form['pickcomments']
			if comment == "":
				comment = "No notes"
			order = json.dumps(session['order'])
			insertOrder("pick", name, "false", comment, order)
			session.pop("order", None)
			return render_template("ordercomplete.html")
		if request.form['option'] == "deliv":
			opt = "deliv"
			address = request.form['address']
			comment = request.form['delivcomments']
			if comment == "":
				comment = "No notes"
			order = json.dumps(session['order'])
			insertOrder("deliv", "false", address, comment, order)
			session.pop("order", None)
			return render_template("ordercomplete.html")
	else:
		return redirect("/")

@app.route('/category', methods=['GET'])
def categorys():
	option = request.args
	try:
		t = option["type"]
		types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
		boo = False
		for i in types:
			if t == i:
				boo = True
		if boo:
			original = getItems(t)
			if len(original) == 0:
				return render_template("noitems.html", item=t)
			c = chunks(original, 4)
			return render_template("menuTemplate.html", l = c, t=t)
		else:
			return render_template("error.html")
	except:
		return render_template("error.html")

@app.route('/item')
def item():
	option = request.args
	try:
		ident = option["id"]
		t = option["type"]
		types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
		boo = False
		for i in types:
			if t == i:
				boo = True
		if boo:
			it = getItemItem(t, ident)[0]
			n = it["name"]
			return render_template("orderItem.html", name=n, id=ident, type=t)
		else:
			return render_template("error.html")
	except:
		return render_template("error.html")

@app.route('/description')
def description():
	option = request.args
	try:
		ident = option["id"]
		t = option["type"]
		types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
		boo = False
		for i in types:
			if t == i:
				boo = True
		if boo:
			it = getItemItem(t, ident)[0]
			name = it["name"]
			ldes = it["longDes"]
			price = it["price"]
			src = it["location"]
			return render_template("itemTemplate.html", name=name, l=ldes, price=price, src=src, id=ident, type=t)
		else:
			return render_template("error.html")
	except:
		return render_template("error.html")

@app.route('/orderdelete', methods=['GET', 'POST'])
def deleteanitem():
	if request.method == "GET":
		return redirect("/order")
	if request.method == "POST":
		a = int(request.form["i"])
		x = 0
		session["order"].pop(a)
		if not session["order"]:
			session.pop('order', None)
		y = 0
		if 'order' in session:
			for i in session["order"]:
				i["number"] = y
				y+=1
		return redirect("/order")

@app.route('/addorder', methods=['GET', 'POST'])
def addanitem():
	if request.method == "GET":
		return redirect("/order")
	if request.method == "POST":
		i = request.form["id"]
		t = request.form["type"]
		amount = request.form["amount"]
		notes = request.form["notes"]
		if notes == "":
			notes = "no notes"
		addItem(i, t, notes, amount)
		return redirect("/order")
@app.route('/resetorder', methods=['POST'])
def resetorder():
	session.pop('order', None)
	return redirect("/order")

@app.route('/updateorder', methods=['GET', 'POST'])
def updateorder():
	if request.method == "POST":
		option = request.form
		notes = option['notes']
		if notes == "":
			notes = "no notes"
		amount = option['amount']
		num = int(option['num'])
		session["order"][num]["notes"] = notes
		session["order"][num]["amount"] = amount
		return redirect("/order")
	if request.method == "GET":
		option = request.args
		num = int(option['i'])
		it = session["order"][num]
		notes = it["notes"]
		amount = it["amount"]
		num = str(it["number"])
		n = getItem(it["type"], it["id"])
		name = n[0]["name"]
		return render_template("updateItem.html", name=name, amount=amount, num=num, notes=notes)

@app.route('/events', methods=['GET', 'POST'])
def events():
	if request.method == "GET":
		values = getEvents()
		if len(values) == 0:
			return render_template("noevents.html")
		threes = chunks(values, 3)[0]
		one = threes[0]
		one["month"] = numToMonth(one["month"])
		twobad = "false"
		if len(threes) > 1:
			two = threes[1]
			two["month"] = numToMonth(two["month"])
		else:
			two = threes[0]
			twobad = "true"
		threebad = "false"
		if len(threes) > 2:
			three = threes[2]
			three["month"] = numToMonth(three["month"])
		else:
			three = threes[0]
			threebad = "true"
		l = len(values)
		groups = int(math.ceil(l/3.0))
		return render_template("events.html", one=one, two=two, three=three, groups=groups, twobad=twobad, threebad=threebad)
	if request.method == "POST":
		opt = int(request.args['i'])
		values = getEvents()
		sel = chunks(values, 3)[opt - 1]
		sel[0]["month"] = numToMonth(sel[0]["month"])
		if len(sel) > 1:
			sel[1]["month"] = numToMonth(sel[1]["month"])
		if len(sel) > 2:
			sel[2]["month"] = numToMonth(sel[2]["month"])
		return json.dumps(sel)

@app.route('/directions')
def directions():
	return render_template("directions.html")

@app.route('/reservations')
def reservations():
	session['reservation'] = "true"
	hours = getHours()
	bad = []
	x = 0
	for i in hours:
		if i['open'] == 0:
			bad.append(str(toModifiedDayOfWeek(x)))
		x += 1
	return render_template("reservations.html", bad=bad)

@app.route("/reservations/api")
def reservationsapi():
	day = int(request.args['day'])
	return str(json.dumps(getHours()[day]))

@app.route('/reserved', methods=['POST'])
def reserved():
	if "reservation" in session:
		session.pop("reservation", None)
		name = request.form['name']
		phone = request.form['phone']
		if phone == "":
			phone = "no phone"
		number = request.form['people']
		details = request.form['message']
		if details == "":
			details = "no details"
		day = str(int(request.form['day']) + 1)
		month = str(int(request.form['month']) + 1)
		year = request.form['year']
		time = request.form['time']
		addReservation(name, phone, number, details, time, day, month, year)
		return render_template("reserved.html")
	else:
		return redirect("/")

@app.route('/chef')
def chef():
	return render_template("chef.html")

#admin login functions
def adminLogIn():
	session['admin'] = "true"

def adminLogOut():
	session.pop('admin', None)

def adminIsIn():
	if 'admin' in session:
		return True
	else:
		return False

def canLogIn(name, password):
	admins = getAdmins(name)
	if len(admins) == 1:
		if admins[0]['password'] == encrypt(password):
			return True
		else:
			return False
	else:
		return False

#admin panel
@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if request.method == "GET":
		if adminIsIn():
			return redirect("/admin/home")
		else:
			return render_template("admin/login.html")
	if request.method == "POST":
		username = request.form['name']
		password = request.form['pass']
		if canLogIn(username, password):
			adminLogIn()
			return "true"
		else:
			return "false"

@app.route('/login')
def login():
	return redirect('/admin')

@app.route('/admin/')
def admins():
	return redirect('/admin')

@app.route("/admin/home")
def adminhomeflask():
	if adminIsIn():
		appetizers = getItemInfo("appetizers")
		soups = getItemInfo("soups")
		salads = getItemInfo("salads")
		kids = getItemInfo("kids")
		entrees = getItemInfo("entrees")
		breads = getItemInfo("breads")
		desserts = getItemInfo("desserts")
		drinks = getItemInfo("drinks")
		amount = {}
		amount["appetizers"] = 0
		amount["soups"] = 0
		amount["salads"] = 0
		amount["kids"] = 0
		amount["entrees"] = 0
		amount["breads"] = 0
		amount["drinks"] = 0
		amount["desserts"] = 0
		days = {}
		days["mon"] = 0
		days["tue"] = 0
		days["wed"] = 0
		days["thu"] = 0
		days["fri"] = 0
		days["sat"] = 0
		days["sun"] = 0
		donut = {}
		donut["appetizers"] = []
		donut["soups"] = []
		donut["salads"] = []
		donut["kids"] = []
		donut["entrees"] = []
		donut["breads"] = []
		donut["drinks"] = []
		donut["desserts"] = []
		highest = 0
		for i in appetizers:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["appetizers"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["appetizers"] += i['mon']
			amount["appetizers"] += i['tue']
			amount["appetizers"] += i['wed']
			amount["appetizers"] += i['thu']
			amount["appetizers"] += i['fri']
			amount["appetizers"] += i['sat']
			amount["appetizers"] += i['sun']
		for i in soups:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["soups"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["soups"] += i['mon']
			amount["soups"] += i['tue']
			amount["soups"] += i['wed']
			amount["soups"] += i['thu']
			amount["soups"] += i['fri']
			amount["soups"] += i['sat']
			amount["soups"] += i['sun']
		for i in salads:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["salads"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["salads"] += i['mon']
			amount["salads"] += i['tue']
			amount["salads"] += i['wed']
			amount["salads"] += i['thu']
			amount["salads"] += i['fri']
			amount["salads"] += i['sat']
			amount["salads"] += i['sun']
		for i  in kids:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["kids"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["kids"] += i['mon']
			amount["kids"] += i['tue']
			amount["kids"] += i['wed']
			amount["kids"] += i['thu']
			amount["kids"] += i['fri']
			amount["kids"] += i['sat']
			amount["kids"] += i['sun']
		for i in entrees:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["entrees"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["entrees"] += i['mon']
			amount["entrees"] += i['tue']
			amount["entrees"] += i['wed']
			amount["entrees"] += i['thu']
			amount["entrees"] += i['fri']
			amount["entrees"] += i['sat']
			amount["entrees"] += i['sun']
		for i in breads:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["breads"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["breads"] += i['mon']
			amount["breads"] += i['tue']
			amount["breads"] += i['wed']
			amount["breads"] += i['thu']
			amount["breads"] += i['fri']
			amount["breads"] += i['sat']
			amount["breads"] += i['sun']
		for i in drinks:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["drinks"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["drinks"] += i['mon']
			amount["drinks"] += i['tue']
			amount["drinks"] += i['wed']
			amount["drinks"] += i['thu']
			amount["drinks"] += i['fri']
			amount["drinks"] += i['sat']
			amount["drinks"] += i['sun']
		for i in desserts:
			num = i["mon"] + i["tue"] + i["wed"] + i["thu"] + i["fri"] + i["sat"] + i["sun"]
			donut["desserts"].append(num)
			days["mon"] += i["mon"]
			days["tue"] += i["tue"]
			days["wed"] += i["wed"]
			days["thu"] += i["thu"]
			days["fri"] += i["fri"]
			days["sat"] += i["sat"]
			days["sun"] += i["sun"]
			amount["desserts"] += i['mon']
			amount["desserts"] += i['tue']
			amount["desserts"] += i['wed']
			amount["desserts"] += i['thu']
			amount["desserts"] += i['fri']
			amount["desserts"] += i['sat']
			amount["desserts"] += i['sun']
		if len(donut["appetizers"]) > highest:
			highest = len(donut["appetizers"])
		if len(donut["soups"]) > highest:
			highest = len(donut["soups"])
		if len(donut["salads"]) > highest:
			highest = len(donut["salads"])
		if len(donut["kids"]) > highest:
			highest = len(donut["kids"])
		if len(donut["entrees"]) > highest:
			highest = len(donut["entrees"])
		if len(donut["breads"]) > highest:
			highest = len(donut["breads"])
		if len(donut["drinks"]) > highest:
			highest = len(donut["drinks"])
		if len(donut["desserts"]) > highest:
			highest = len(donut["desserts"])
		donut["appetizers"] += [0] * (highest - len(donut["appetizers"]))
		donut["soups"] += [0] * (highest - len(donut["soups"]))
		donut["salads"] += [0] * (highest - len(donut["salads"]))
		donut["kids"] += [0] * (highest - len(donut["kids"]))
		donut["entrees"] += [0] * (highest - len(donut["entrees"]))
		donut["breads"] += [0] * (highest - len(donut["breads"]))
		donut["drinks"] += [0] * (highest - len(donut["drinks"]))
		donut["desserts"] += [0] * (highest - len(donut["desserts"]))
		temp = requests.get("http://api.openweathermap.org/data/2.5/weather?id=5128638&appid=27419410c55037f38ee2ebc62deaa5b7").json()
		temperature = str(int(kToF(temp['main']['temp'])))
		return render_template("admin/index.html", temp=temperature, amount=amount, days=days, donut=donut, highest=highest)




		mon = 0
		tue = 0
		wed = 0
		thu = 0
		fri = 0
		sat = 0
		sun = 0
		appetizers = 0
		for i in getItemInfo('appetizers'):
			appetizers += i['mon']
			appetizers += i['tue']
			appetizers += i['wed']
			appetizers += i['thu']
			appetizers += i['fri']
			appetizers += i['sat']
			appetizers += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		soups = 0
		for i in getItemInfo('soups'):
			soups += i['mon']
			soups += i['tue']
			soups += i['wed']
			soups += i['thu']
			soups += i['fri']
			soups += i['sat']
			soups += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		salads = 0
		for i in getItemInfo('salads'):
			salads += i['mon']
			salads += i['tue']
			salads += i['wed']
			salads += i['thu']
			salads += i['fri']
			salads += i['sat']
			salads += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		kids = 0
		for i in getItemInfo('kids'):
			kids += i['mon']
			kids += i['tue']
			kids += i['wed']
			kids += i['thu']
			kids += i['fri']
			kids += i['sat']
			kids += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		entrees = 0
		for i in getItemInfo('entrees'):
			entrees += i['mon']
			entrees += i['tue']
			entrees += i['wed']
			entrees += i['thu']
			entrees += i['fri']
			entrees += i['sat']
			entrees += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		breads = 0
		for i in getItemInfo('breads'):
			breads += i['mon']
			breads += i['tue']
			breads += i['wed']
			breads += i['thu']
			breads += i['fri']
			breads += i['sat']
			breads += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		drinks = 0
		for i in getItemInfo('drinks'):
			drinks += i['mon']
			drinks += i['tue']
			drinks += i['wed']
			drinks += i['thu']
			drinks += i['fri']
			drinks += i['sat']
			drinks += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		desserts = 0
		for i in getItemInfo('desserts'):
			desserts += i['mon']
			desserts += i['tue']
			desserts += i['wed']
			desserts += i['thu']
			desserts += i['fri']
			desserts += i['sat']
			desserts += i['sun']
			mon += i['mon']
			tue += i['tue']
			wed += i['wed']
			thu += i['thu']
			fri += i['fri']
			sat += i['sat']
			sun += i['sun']
		total = appetizers + soups + salads + kids + entrees + breads + drinks + desserts
		temp = requests.get("http://api.openweathermap.org/data/2.5/weather?id=5128638&appid=27419410c55037f38ee2ebc62deaa5b7").json()
		temperature = str(int(kToF(temp['main']['temp'])))
		return render_template("admin/index.html", temp=temperature, appetizers=appetizers, soups=soups, salads=salads, kids=kids, entrees=entrees, breads=breads, drinks=drinks, desserts=desserts, total=total, mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, sun=sun)
	else:
		return redirect("/admin")

@app.route("/admin/logout")
def adminlogoutflask():
	adminLogOut()
	return redirect("/admin")

@app.route("/admin/stats")
def adminstatsflask():
	if adminIsIn():
		return render_template("admin/stats.html")
	else:
		return redirect("/admin")

@app.route("/admin/stats/donutmod")
def adminstatsdonut():
	if adminIsIn():
		appetizers =  str(getNumberOfItems('appetizers'))
		soups =  str(getNumberOfItems('soups'))
		salads =  str(getNumberOfItems('salads'))
		kids =  str(getNumberOfItems('kids'))
		entrees =  str(getNumberOfItems('entrees'))
		breads =  str(getNumberOfItems('breads'))
		drinks =  str(getNumberOfItems('drinks'))
		desserts =  str(getNumberOfItems('desserts'))
		return render_template("admin/donut.html", appetizers=appetizers, soups=soups, salads=salads, kids=kids, entrees=entrees, breads=breads, drinks=drinks, desserts=desserts)
	else:
		return redirect("/admin")

def getRemakeDonut(t): #gets the donut data
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select " + t + ".name, " + t + "num.* from " + t + ", " + t + "num where " + t + ".id = " + t + "num.id and " + t + ".status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

@app.route("/admin/stats/donut")
def adminstatsdonutremake():
	if adminIsIn():
		appetizers = getRemakeDonut("appetizers")
		soups = getRemakeDonut("soups")
		salads = getRemakeDonut("salads")
		kids = getRemakeDonut("kids")
		entrees = getRemakeDonut("entrees")
		breads = getRemakeDonut("breads")
		drinks = getRemakeDonut("drinks")
		desserts = getRemakeDonut("desserts")
		out = 0
		for i in appetizers:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in soups:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in salads:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in kids:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in entrees:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in breads:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in drinks:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		for i in desserts:
			out += i['mon']
			out += i['tue']
			out += i['wed']
			out += i['thu']
			out += i['fri']
			out += i['sat']
			out += i['sun']
		return render_template("admin/donutremake.html", appetizers=appetizers, soups=soups, salads=salads, kids=kids, entrees=entrees, breads=breads, drinks=drinks, desserts=desserts, out=out)
	else:
		return redirect("/admin")

@app.route("/admin/stats/donutitem")
def adminstatsdonutitem():
	if adminIsIn():
		types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
		t = request.args['t']
		for i in types:
			if i == t:
				ar = []
				n = []
				names = []
				iter = 0
				for i in getItemInfo(t):
					n.append(str(int(i['id'])))
					ar.append([int(i['mon']) + int(i['tue']) + int(i['wed']) + int(i['thu']) + int(i['fri']) + int(i['sat']) + int(i['sun']), getColor(iter), getHighlights(iter), getItemName(str(int(i['id'])), t)])
					iter += 1
				total = 0
				for tot in ar:
					total += tot[0]
				return render_template("admin/donutitem.html", ar=ar, total=total)
		return render_template('errorpages/error.html', error="404", desc="Page Not Found"), 404
	else:
		return redirect("/admin")

@app.route("/admin/stats/bar")
def adminstatsbar():
	if adminIsIn():
		appetizers =  str(getNumberOfItems('appetizers'))
		soups =  str(getNumberOfItems('soups'))
		salads =  str(getNumberOfItems('salads'))
		kids =  str(getNumberOfItems('kids'))
		entrees =  str(getNumberOfItems('entrees'))
		breads =  str(getNumberOfItems('breads'))
		drinks =  str(getNumberOfItems('drinks'))
		desserts =  str(getNumberOfItems('desserts'))
		return render_template("admin/bar.html", appetizers=appetizers, soups=soups, salads=salads, kids=kids, entrees=entrees, breads=breads, drinks=drinks, desserts=desserts)
	else:
		return redirect("/admin")

@app.route("/admin/stats/baritem")
def adminstatsbaritem():
	if adminIsIn():
		types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
		t = request.args['t']
		for i in types:
			if i == t:
				ar = []
				n = []
				names = []
				for i in getItemInfo(t):
					n.append(str(int(i['id'])))
					ar.append(int(i['mon']) + int(i['tue']) + int(i['wed']) + int(i['thu']) + int(i['fri']) + int(i['sat']) + int(i['sun']))
				for j in n:
					names.append(getItemName(j, t))
				return render_template("admin/baritem.html", names=names, ar=ar)
		return render_template('errorpages/error.html', error="404", desc="Page Not Found"), 404
	else:
		return redirect("/admin")

@app.route("/admin/stats/line")
def adminstatsline():
	if adminIsIn():
		appetizers =  str(getNumberOfItems('appetizers'))
		soups =  str(getNumberOfItems('soups'))
		salads =  str(getNumberOfItems('salads'))
		kids =  str(getNumberOfItems('kids'))
		entrees =  str(getNumberOfItems('entrees'))
		breads =  str(getNumberOfItems('breads'))
		drinks =  str(getNumberOfItems('drinks'))
		desserts =  str(getNumberOfItems('desserts'))
		return render_template("admin/line.html", appetizers=appetizers, soups=soups, salads=salads, kids=kids, entrees=entrees, breads=breads, drinks=drinks, desserts=desserts)
	else:
		return redirect("/admin")

@app.route("/admin/stats/lineitem")
def adminstatslineitem():
	if adminIsIn():
		types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
		t = request.args['t']
		for i in types:
			if i == t:
				data = getItemInfo(t)
				mon = 0
				tue = 0
				wed = 0
				thu = 0
				fri = 0
				sat = 0
				sun = 0
				for i in data:
					mon += int(i['mon'])
					tue += int(i['tue'])
					wed += int(i['wed'])
					thu += int(i['thu'])
					fri += int(i['fri'])
					sat += int(i['sat'])
					sun += int(i['sun'])
				return render_template("admin/lineitem.html", mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, sun=sun)
		return render_template('errorpages/error.html', error="404", desc="Page Not Found"), 404
	else:
		return redirect("/admin")

@app.route("/admin/stats/stats")
def adminstatsstats():
	if adminIsIn():
		appetizers = getItemInfo('appetizers')
		iter = 0
		while iter < len(appetizers):
			appetizers[iter]['name'] = getItemName(str(int(appetizers[iter]['id'])), "appetizers")
			iter += 1
		soups = getItemInfo('soups')
		iter = 0
		while iter < len(soups):
			soups[iter]['name'] = getItemName(str(int(soups[iter]['id'])), "soups")
			iter += 1
		salads = getItemInfo('salads')
		iter = 0
		while iter < len(salads):
			salads[iter]['name'] = getItemName(str(int(salads[iter]['id'])), "salads")
			iter += 1
		kids = getItemInfo('kids')
		iter = 0
		while iter < len(kids):
			kids[iter]['name'] = getItemName(str(int(kids[iter]['id'])), "kids")
			iter += 1
		entrees = getItemInfo('entrees')
		iter = 0
		while iter < len(entrees):
			entrees[iter]['name'] = getItemName(str(int(entrees[iter]['id'])), "entrees")
			iter += 1
		breads = getItemInfo('breads')
		iter = 0
		while iter < len(breads):
			breads[iter]['name'] = getItemName(str(int(breads[iter]['id'])), "breads")
			iter += 1
		drinks = getItemInfo('drinks')
		iter = 0
		while iter < len(drinks):
			drinks[iter]['name'] = getItemName(str(int(drinks[iter]['id'])), "drinks")
			iter += 1
		desserts = getItemInfo('desserts')
		iter = 0
		while iter < len(desserts):
			desserts[iter]['name'] = getItemName(str(int(desserts[iter]['id'])), "desserts")
			iter += 1
		return render_template("admin/statsstats.html", appetizers=appetizers, soups=soups, salads=salads, kids=kids, entrees=entrees, breads=breads, drinks=drinks, desserts=desserts)
	else:
		return redirect("/admin")

@app.route("/admin/download")
def downloadfileflask():
	if adminIsIn():
		output = ""
		appetizersnames = getItemNames("appetizers")
		iter = 0
		for i in getItemInfo("appetizers"):
			output += "\'" + appetizersnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter += 1
		soupsnames = getItemNames("soups")
		iter = 0
		for i in getItemInfo("soups"):
			output += "\'" + soupsnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter += 1
		saladsnames = getItemNames("salads")
		iter = 0
		for i in getItemInfo("salads"):
			output += "\'" + saladsnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter += 1
		kidsnames = getItemNames("kids")
		iter = 0
		for i in getItemInfo("kids"):
			output += "\'" + kidsnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter += 1
		entreesnames = getItemNames("entrees")
		iter = 0
		for i in getItemInfo("entrees"):
			output += "\'" + entreesnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter += 1
		breadsnames = getItemNames("breads")
		iter = 0
		for i in getItemInfo("breads"):
			output += "\'" + breadsnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter =+ 1
		drinksnames = getItemNames("drinks")
		iter = 0
		for i in getItemInfo("drinks"):
			output += "\'" + drinksnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter +=1
		dessertsnames = getItemNames("desserts")
		iter = 0
		for i in getItemInfo("desserts"):
			output += "\'" + dessertsnames[iter]['name'] + "\", "
			output += "\'" + str(i['mon']) + "\", "
			output += "\'" + str(i['tue']) + "\", "
			output += "\'" + str(i['wed']) + "\", "
			output += "\'" + str(i['thu']) + "\", "
			output += "\'" + str(i['fri']) + "\", "
			output += "\'" + str(i['sat']) + "\", "
			output += "\'" + str(i['sun']) + "\"\n"
			iter = 0
		response = make_response(output)
		response.headers["Content-Disposition"] = "attachment; filename=log.csv"
		return response
	else:
		return "false"

@app.route("/admin/reservations")
def adminreservations():
	if adminIsIn():
		reservations = getReservations()
		if len(reservations) == 0:
			return render_template("admin/reservationsbad.html")
		return render_template("admin/reservations.html", reservations=reservations)
	else:
		return redirect("/admin")
@app.route("/admin/orders")
def adminorderflask():
	if adminIsIn():
		orders = getOrders()
		if len(orders) == 0:
			return render_template("admin/ordersbad.html")
		return render_template("admin/orders.html", orders=orders)
	else:
		return redirect("/admin")

@app.route("/admin/orderitem")
def adminorderitemflask():
	if adminIsIn():
		i = request.args['id']
		o = getSpecificOrder(i)
		orders = []
		for i in json.loads(o[0]['items']):
			orders.append(i)
		x = 0
		while x < len(orders):
			orders[x]['real'] = getSpecificItem(orders[x]['type'], str(orders[x]['id']))[0]['name']
			x += 1
		return render_template("admin/orderitem.html", orders=orders)
	else:
		return redirect("/admin")
	
@app.route("/admin/api/deleteorder", methods=['POST'])
def adminapideleteorder():
	if adminIsIn():
		i = request.form['id']
		deleteOrder(i)
		return "true"
	else:
		return redirect("/admin")

@app.route("/admin/hours")
def adminhours():
	if adminIsIn():
		translate = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday', 'sat': 'Saturday', 'sun': 'Sunday'}
		return render_template("admin/hours.html", hours=getHours(), translate=translate)
	else:
		return redirect("/admin")

@app.route("/admin/api/hours", methods=['POST'])
def adminapihours():
	if adminIsIn():
		start = json.loads(request.form['start'])
		end = json.loads(request.form['end'])
		o = json.loads(request.form['open'])
		days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
		for day in days:
			updateHour(day, start[day], end[day], str(o[day]))
		return "true"
	else:
		return "false"

@app.route("/admin/members")
def adminmembers():
	if adminIsIn():
		return render_template("admin/members.html", members=getMembers())
	else:
		return redirect("/admin")

@app.route("/admin/members/email", methods=['POST'])
def adminmembersemail():
	sendToMembers(request.form['message'])
	return "true"


@app.route("/admin/passwords")
def adminspasswords():
	if adminIsIn():
		return render_template("admin/passwords.html", users=getUsers())
	else:
		return redirect("/admin")

@app.route("/admin/api/adduser", methods=['POST'])
def adminapiadduser():
	if adminIsIn():
		name = request.form['name']
		password = request.form['password']
		if ifUserExists(name) > 0:
			return "false"
		else:
			addUser(name, password)
			return "true"
	else:
		return "false"

@app.route("/admin/api/deleteuser", methods=['POST'])
def adminapideleteuser():
	if adminIsIn():
		password = request.form['password']
		if (getPasswordForCheck(request.form['id'])[0]['password'] == encrypt(password)):
			deleteUser(request.form['id'])
			return "true"
		else:
			return "false"
	else:
		return "false"

@app.route("/admin/api/chosen")
def adminapichosen():
	if adminIsIn():
		return str(json.dumps(chosenUpdate()))
	else:
		return "false"

@app.route("/admin/api/changeuser", methods=['POST'])
def adminapichangeuser():
	if adminIsIn():
		old = request.form['old']
		i = request.form['id']
		if (getPasswordForCheck(i)[0]['password'] == encrypt(old)):
			changePassword(i, request.form['new'])
			return "true"
		else:
			return "incorrect"
	else:
		return "false"

@app.route("/admin/events")
def adminevents():
	return render_template("admin/events.html", events=getEvents(), email=getEmail())

@app.route("/admin/api/addevent", methods=['POST'])
def adminapiaddevent():
	if adminIsIn():
		addEvent(request.form['name'], request.form['description'], request.form['year'], request.form['month'], request.form['day'])
		return "true"
	else:
		return "false"

@app.route("/admin/api/deleteevent", methods=['POST'])
def adminapideleteevent():
	i = request.form['id']
	deleteEvent(i)
	return "true"

@app.route("/admin/api/getevents")
def adminapigetevents():
	if adminIsIn():
		return str(json.dumps(getEvents()))
	else:
		return "false"
@app.route("/admin/api/getchange")
def adminapigetchange():
	return str(json.dumps(getSpecficEvent(request.args['id'])))

@app.route("/admin/api/changeevent", methods=['POST'])
def adminapichangeevent():
	name = request.form['name']
	description = request.form['description']
	i = request.form['id']
	year = request.form['year']
	month = request.form['month']
	day = request.form['day']
	deleteEvent(i)
	addEvent(name, description, year, month, day)
	return "true"

@app.route("/admin/api/email", methods=['POST'])
def adminapiemail():
	updateEmail(request.args['email'])
	return "true"

@app.route("/download")
def downloadpdf():
	return redirect(url_for('static', filename='print.pdf'))

@app.route("/reviews")
def reviews():
	return render_template("reviews.html")

@app.route("/loyalty", methods=['GET', 'POST'])
def loyalty():
	if request.method == "GET":
		return render_template("loyalty.html")
	if request.method == "POST":
		addMember(request.form['name'], request.form['email'], request.form['phone'])
		return "true"

@app.route("/admin/add")
def adminaddflask():
	if adminIsIn():
		return render_template("admin/addnew.html")
	else:
		return redirect("/admin")

def addMenuItemQuery(category, name, short, longDes, location, price): #deletes an event
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into " + category + " (name, shortDes, longDes, location, price) values ('" + name + "', '" + short + "', '" + longDes + "', '" + location + "', " + price + ")"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		cur.execute("select last_insert_id()")
		rows = cur.fetchall()
		return rows

def addMenuItemQueryNum(category, i): #adds to stats table
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "insert into " + category + "num values(" + str(i) + ",0,0,0,0,0,0,0,1)"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)

@app.route("/admin/api/additem", methods=["POST"])
def adminapiadditemflask():
	if adminIsIn():
		name = request.form["name"]
		price = request.form["price"]
		shortDes = request.form["shortDes"]
		longDes = request.form["longDes"]
		location = request.form["location"]
		category = request.form["category"]
		out = addMenuItemQuery(category, name, shortDes, longDes, location, price)[0]["last_insert_id()"]
		addMenuItemQueryNum(category, out)
		return "true"
	else:
		return "false"

@app.route("/admin/delete")
def adminapideleteitemflask():
	if adminIsIn():
		return render_template("/admin/deletenew.html")
	else:
		return redirect("/admin")

def getItemsForDeletion(option): #returns list of any type of food. ex: appetizers
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select id, name from " + option + " where status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

@app.route("/admin/api/deletecategory")
def adminapideleteitemflaskapi():
	if adminIsIn():
		items = getItemsForDeletion(request.args["category"])
		return str(json.dumps(items))
	else:
		return "false"

def deleteItemByTurnOff(category, item): #deletes/disabled an item
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update " + category + " set status = 0 where id = " + item
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		cur.execute("update " + category + "num set status = 0 where id = " + item)

@app.route("/admin/api/deleteitem", methods=["POST"])
def adminapideleteitemflaskapinext():
	if adminIsIn():
		item = request.form["item"]
		category = request.form["category"]
		deleteItemByTurnOff(category, item)
		return "true"
	else:
		return "false"

@app.route("/admin/modify")
def adminmodify():
	return render_template("admin/modifynew.html")

def getSpecifItemForJson(category, item):
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "select * from " + category + " where id = " + item + " and status = 1"
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)
		rows = cur.fetchall()
	return rows

def decimal_default(obj): #allows json dumps to serialize decimals
	if isinstance(obj, decimal.Decimal):
		return float(obj)
	raise TypeError

@app.route("/admin/api/modify", methods=["POST"])
def adminapimodifygetvalues():
	if adminIsIn():
		category = request.form["category"]
		item = request.form["item"]
		out = getSpecifItemForJson(category, item)
		return json.dumps(out, default=decimal_default)
	else:
		return "false"

def updateSpecificItem(category, name, price, location, shortDes, longDes, item):
	con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
	query = "update " + category + " set name = '" + name + "', price = " + price + ", location = '" + location + "', shortDes = '" + shortDes + "', longDes = '" + longDes + "' where id = " + item
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(query)


@app.route("/admin/api/itemmodify", methods=["POST"])
def adminapimodifyitemflaskupdate():
	if adminIsIn():
		category = request.form["category"]
		item = request.form["item"]
		name = request.form["name"]
		price = request.form["price"]
		shortDes = request.form["shortDes"]
		longDes = request.form["longDes"]
		location = request.form["location"]
		updateSpecificItem(category, name, price, location, shortDes, longDes, item)
		return "true"
	else:
		return "false"

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTDALKSFJLDSKJFKLSDJF'