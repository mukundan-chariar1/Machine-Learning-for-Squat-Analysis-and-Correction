from flask import Flask
from flask import render_template
from flask import request,redirect, url_for, session
from datetime import date, timedelta, datetime
import os

import db_edited as db
import inference_button_deep_edited as inference_button_deep

# Flask takes its templates from /templates by default. We have changed the path it takes its templates from to /templates_edited

app = Flask(__name__)

#app = Flask(__name__, template_folder='/templates_edited')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# index page
@app.route('/index')
def indexpage():
    return render_template('index.html')

######################################### Login #########################################
# Login page (first screen)
@app.route('/')
def login():
    return render_template('login.html')

# check login
@app.route('/login_check', methods = ['POST'])
def login_check():
    email = request.form['email']
    password = request.form['password']
    result = db.login_result(email, password)
    if (result):
        userNo = db.userNo(email)
        # save user no value to session
        session['userNo'] = userNo
        print(session)
        return redirect('/index')
    else:
        return redirect('/login_error')

# login error
@app.route('/login_error')
def login_error():
    return render_template('login_error.html')

# logout
@app.route('/log_out')
def log_out():
    session.pop('userNo', None)
    print(session)
    return redirect('/')

# forgot password
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/forgot_password_finish')
def forgot_password_finish():
    return render_template('forgot_password_finish.html')

# register user
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_email')
def register_email():
    return render_template('register_email.html')

@app.route('/register_pw')
def register_pw():
    return render_template('register_pw.html')

@app.route('/register_check', methods=['POST'])
def register_check():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    repeatpassword = request.form['repeatpassword']

    if (password != repeatpassword): # verify password
        return render_template('register_pw.html')  
    elif (db.member(email) != 0): # email already exists
        return render_template('register_email.html')
    else:
        db.member_add(name, email, password) # add member to db
        return redirect('/')

######################################### menu 1 graph #########################################
# shows last weeks squat graph
@app.route('/graph')
def graph():
    userNo = session['userNo']
    day = []
    n = ['6','5','4','3','2','1','0']
    for i in n:
        result = db.get_sum_of_squat_7days(i, userNo) #saved in order of number from day 6
        day.append(int(result))
    return render_template('graph.html', day=day)

######################################### menu 2 challenges #########################################
@app.route('/challenge',methods=['POST'])
def challenge():
    userNo = session['userNo']
    startdate = request.form['startdate']
    finishdate = request.form['finishdate']
    if(startdate > finishdate):
        return render_template('challenge_setting_again.html')
    count = request.form['count']
    # If you already have a challenge history, update it
    if(db.get_challenge(userNo) != 0):
        db.challenge_update(startdate,finishdate,count,userNo)
    # create new one if not
    else:
        db.challenge_add(userNo,startdate,finishdate,count)

    today = datetime.today()
    sdate = datetime.strptime(startdate,'%Y-%m-%d')
    if ((today.year==sdate.year) & (today.month==sdate.month)&(today.day==sdate.day)):
        challenge_day = '1'
    else:
        challenge_day = int("{0!s}".format(str(today-sdate).split()[0])) +1

    todaysquat = db.get_sum_of_challenge_squat(userNo, startdate, finishdate)
    return render_template('challenge.html',startdate = startdate, finishdate = finishdate, count=count
                            ,challenge_day = challenge_day,todaysquat = todaysquat)

@app.route('/challenge_setting')
def challenge_setting():
    return render_template('challenge_setting.html')

@app.route('/challenge_start')
def challenge_start():
    userNo = session['userNo']
    result = db.get_challenge(userNo)
    if (result == 0):
        return render_template('challenge_start.html')
    else:
        startdate = result['startdate']
        finishdate = result['finishdate']
        count = result['count']
        today = datetime.today()

        if (finishdate < today):
            return render_template('challenge_finish.html',startdate = startdate.strftime('%Y-%m-%d'), finishdate =finishdate.strftime('%Y-%m-%d'))
        else:
            pass

        if ((today.year == startdate.year) & (today.month == startdate.month)&(today.day == startdate.day)):
            challenge_day = '1'
        else :
            challenge_day = int("{0!s}".format(str(today-startdate).split()[0])) +1
            

        todaysquat = db.get_sum_of_challenge_squat(userNo, startdate, finishdate)
        return render_template('challenge.html',startdate = startdate.strftime('%Y-%m-%d'), finishdate =finishdate.strftime('%Y-%m-%d') , count=count
                            ,challenge_day = challenge_day,todaysquat = todaysquat)

@app.route('/challenge_finish')
def challenge_finish():
    return render_template('challenge_finish.html') 

######################################### menu 3. record search #########################################
# Plot with full history donut chart
@app.route('/show_total_graph')
def show_total_graph():
    userNo = session['userNo']
    sum_of_squat = db.get_sum_of_squat(userNo)
    return render_template('donut.html', sum_of_squat=sum_of_squat)

# View all records
@app.route('/search')
def index():
    userNo = session['userNo']
    squat_list = db.get_squat_list(userNo)
    sum_of_squat = db.get_sum_of_squat(userNo)
    return render_template('search.html', squat_list=squat_list,
                            totalCount=len(squat_list), sum_of_squat=sum_of_squat)

# Lookup a specific date
@app.route('/search_list', methods=['GET'])
def search_list():
    userNo = session['userNo']
    #Pass value in search field
    squat_date = request.args['squat_date']
    # Return records retrieved from db
    squat_list, sum_of_squat = db.search_result(squat_date, userNo)
    return render_template('search_list.html', squat_list=squat_list, totalCount=len(squat_list), 
                            squat_date = squat_date, sum_of_squat=sum_of_squat)

# Draw a specific date graph
@app.route('/showgraph_<squat_date>')
def showgraph(squat_date):
    userNo = session['userNo']
    sum_of_squat = db.get_sum_of_squat_with_date(squat_date, userNo)
    return render_template('donut.html', squat_date = squat_date, sum_of_squat=sum_of_squat)

######################################### menu 4. guide #########################################
@app.route('/guide') # Types of squats, shooting guide
def guide():
        return render_template('guide.html')

######################################### menu 5. squat #########################################
# selection screen
@app.route('/startsquat')
def startsquat():
        return render_template('squat.html')

# squat
@app.route('/startsquat_check', methods=['post'])		## take this function
def startsquat_check():
    userNo = session['userNo']
    result = int(request.form['options'])
    print(result)
    inference_button_deep.start(result, userNo)
    return render_template('index.html')

app.run(host='127.0.0.1', port=5000, debug=True)
