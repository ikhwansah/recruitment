from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from app import db, login_manager
from app.models import *
from app.auth.picture_handler import add_profile_pic

access = Blueprint('access',__name__)

@access.route("/respon",methods=['GET', 'POST'])
def respon():
    return render_template('register.html')

@access.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":
        respon = {}
        apidata = request.form
        checkemail = Access.query.filter_by(email=apidata['email']).first()
        checkusername = Access.query.filter_by(username=apidata['name']).first()
        if checkemail is None:
            if checkusername is None:
                Access()._insert(apidata['name'], apidata['email'], apidata['password'])
                respon['response'] = 'Registration Successful'
            else:
                respon['response'] = 'Username already used. Please use another username'
        else:
            respon['response'] = 'Email already used. Please use another email'
    return jsonify(respon)

@access.route("/registeruser",methods=['GET','POST'])
def registeruser():
    if request.method == "POST":
        respon = {}
        respon['status'] = '400'
        apidata = request.form
        if 'name' in apidata and 'phonenumber' in apidata and 'password' in apidata and 'email' in apidata and 'gender' in apidata and 'religion' in apidata and 'client_id' in apidata:
                checkemail = User.query.filter_by(email=apidata['email']).first()
                if checkemail is None:
                    User()._register(apidata['name'], apidata['phonenumber'], apidata['password'], apidata['email'], apidata['gender'], apidata['religion'], apidata['client_id'])
                    respon['response'] = 'Registration Successful'
                    respon['status'] = '200'
                else:
                    respon['response'] = 'Email already used. Please use another email'
                    respon['status'] = '400'
        else:
                respon['message'] = 'Incomplete Data'
                respon['status'] = '400'                                           
    return jsonify(respon)

@access.route('/api/V1.0/loginuser', methods = ['GET','POST'])
def loginuser():
    if request.method == "POST":    
        respon = {}
        respon['response'] = 'success'
        user = User.query.filter_by(email=request.form['email']).first()
        if user is None:            
            client = clients.query.filter_by(email=request.form['email']).first()
            if client is None:
                respon['response'] = 'Wrong Username!!'
            elif client.check_password(request.form['password']):
                respon['token'] = client.generate_token()           
                respon['cur_user'] = client.id        
                respon['name'] = client.name        
                respon['email'] = client.email
                respon['status'] = '200'  
                respon['client'] = True
                session['client'] = True   
                login_user(client)  
            else:
                respon['response'] = 'Wrong Password!!'
        elif user.check_password(request.form['password']) :            
            respon['token'] = user.generate_token()           
            respon['cur_user'] = user.id 
            respon['name'] = user.name        
            respon['email'] = user.email
            respon['status'] = '200'       
            respon['client'] = False
            session['client'] = False   
            login_user(user)  
            respon['list_access'] = role()._datauseraccess(current_user.id, current_user.client_id)
        else :
            respon['response'] = 'Wrong Password!!'
        return jsonify(respon)

@access.route('/api/V1.0/login',methods=['GET','POST'])
def apilogin():
    if request.method == "POST":    
        respon = {}
        respon['response'] = 'success'
        access = Access.query.filter_by(email=request.form['email']).first()
        if access is None:            
            client = clients.query.filter_by(email=request.form['email']).first()
            if client is None:
                respon['response'] = 'The username you entered is wrong'
            elif client.check_password(request.form['password']):
                respon['token'] = client.generate_token()           
                respon['cur_user'] = client.id        
                respon['name'] = client.name        
                respon['email'] = client.email
                respon['status'] = '200'  
                respon['client'] = True
                session['client'] = True   
                login_user(client)  
            else:
                respon['response'] = 'The password you entered is wrong'
        elif access.check_password(request.form['password']) :            
            respon['token'] = access.generate_token()
            respon['cur_user'] = access.id 
            respon['name'] = access.name        
            respon['email'] = access.email
            respon['phone'] = access.phone_number
            respon['nik'] = access.nik
            respon['password'] = access.password_hash
            respon['status'] = '200'
            respon['client'] = False
            session['client'] = False
            login_user(access)  
            respon['list_access'] = role()._datauseraccess(current_user.id, current_user.client_id)
        else :
            respon['response'] = 'Wrong Password!!'
        return jsonify(respon)

@access.route("/logout")
def logout():    
    logout_user()
    return redirect(url_for("access.login"))

@access.route("/login")
def login():
    return render_template('auth/login.html', title='Signin')

@access.route("/")
def home():
    return render_template('pages/index.html', title='index')

@access.route("/job_listing")
def job_listing():
    job_listing = Jobvacancy.query.filter_by(status = True)
    return render_template('pages/job_listing.html', job_listing=job_listing)

@access.route("/job_details")
def job_details():
    return render_template('pages/job_details.html')

@access.route("/about")
def about():
    return render_template('pages/about.html')

@access.route("/contact")
def contact():
    return render_template('pages/contact.html')