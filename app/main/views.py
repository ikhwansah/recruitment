from flask import render_template,request,Blueprint, jsonify, send_from_directory, redirect, url_for, session
from flask_login import login_user, current_user, logout_user, login_required
from app.models import *
from .. import app
import json, os, base64, itertools, datetime
from ..utils import resize_files, show_image
from app import db
from ..utils import *

core = Blueprint('core',__name__)
MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'images')
@core.route('/<name>')
def template(name):
    if current_user.is_authenticated:
        if name == 'login':
                return redirect(url_for("core.template", name='dashboard'))
        else :
                if session['client'] is True:
                        return render_template('/{}'.format(name))
                else : 
                        try :
                                check_access = role()._listpermission(current_user.id)[0]
                        except:
                                return render_template('/error_pages/404.html')
                                return render_template('/main/{}'.format(name))
                        else :
                                if name in check_access:
                                        return render_template('/main/{}'.format(name))
                                else:
                                        return redirect(url_for("core.template", name='dashboard'))
    else :        
        if name == 'login':
                return render_template('/auth/{}'.format(name))
        else :
                return redirect(url_for("core.template", name='login.html'))

@core.route('/api/V1.0/dashboard', methods = ['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user'], status = True).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('view', 2):
                        response['jobseeker'] = User()._jobseeker()
                        response['shortlisted'] = User()._shortlisted()
                        response['sukses'] = User()._sukses()
                        response['gagal'] = User()._gagal()
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertaccount', methods = ['GET', 'POST'])
def addaccount():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if 'name' in apidata and 'nik' in apidata and 'phonenumber' in apidata and 'email' in apidata:
                        user_account = Access.query.filter_by(id=apidata['user_id']).first()
                        if user_account is None:
                                checkphonenumber = Access.query.filter_by(phone_number = apidata['phonenumber'], status = True).first()
                                checkemail = Access.query.filter_by(email = apidata['email'], status = True).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                if access.verify_access('insert', 3):
                                                        new_account = Access()._insert(apidata['name'], apidata['nik'], apidata['phonenumber'], apidata['email'], apidata['client_id'])
                                                        response['status'] = '200'
                                                        response['user_id'] = new_account.id
                                                else:
                                                        response['message'] = 'Akses Ditolak!'
                                                        response['status'] = '400'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                        else:
                                checkphonenumber = Access.query.filter_by(phone_number = apidata['phonenumber'], status = True).filter(Access.id != apidata['user_id']).first()
                                checkemail = Access.query.filter_by(email = apidata['email'], status = True).filter(Access.id != apidata['user_id']).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                if access.verify_access('update', 3):
                                                        Access()._update(apidata['user_id'], apidata['name'], apidata['nik'], apidata['phonenumber'], apidata['email'], apidata['client_id'])
                                                        response['status'] = '200'
                                                else:
                                                        response['message'] = 'Akses Ditolak!'
                                                        response['status'] = '400'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'                                           
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/updatepassword', methods = ['GET', 'POST'])
def addpassword():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if 'password_hash' in apidata:
                        user_account = Access.query.filter_by(id=apidata['user_id']).first()
                        if user_account is None:
                                checkphonenumber = Access.query.filter_by(phone_number = apidata['phonenumber'], status = True).first()
                                checkemail = Access.query.filter_by(email = apidata['email'], status = True).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                if access.verify_access('insert', 4):
                                                        new_account = Access()._insert(apidata['password_hash'])
                                                        response['status'] = '200'
                                                        response['user_id'] = new_account.id
                                                else:
                                                        response['message'] = 'Akses Ditolak!'
                                                        response['status'] = '400'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                        else:
                                checkphonenumber = Access.query.filter_by(phone_number = apidata['phonenumber'], status = True).filter(Access.id != apidata['user_id']).first()
                                checkemail = Access.query.filter_by(email = apidata['email'], status = True).filter(Access.id != apidata['user_id']).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                if access.verify_access('update', 4):
                                                        Access()._updatepassword(apidata['user_id'], apidata['password_hash'])
                                                        response['status'] = '200'
                                                else:
                                                        response['message'] = 'Akses Ditolak!'
                                                        response['status'] = '400'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'                                           
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/account', methods = ['GET', 'POST'])
def dataaccount():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('view', 12):
                        if session['client'] is True:
                                tempid = current_user.id
                        else:                
                                tempid = current_user.client_id
                        response['account'] = Access()._account(tempid)                        
                        response['role'] = list_role()._list(tempid)
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/accountdetail', methods = ['GET', 'POST'])
def dataformaccount():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        response['dataform'] = {}
        apidata = request.form 
        if session['client'] is True:
                tempid = current_user.id
        else:
                tempid = current_user.client_id    
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Access.query.filter_by(id = apidata['user_id']).first()
                if check is not None:
                        if access.verify_access('view', 12):
                                response['account'] = Access()._accountdetail(apidata['user_id'])
                                response['dataform']['client'] = clients()._list()
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        response['message'] = 'User Tidak Terdaftar'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/employee', methods = ['GET', 'POST'])
def dataemployee():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('view', 1):
                        if session['client'] is True:
                                tempid = current_user.id
                        else:                
                                tempid = current_user.client_id
                        response['employee'] = User()._employee(tempid)
                        response['applicantstatus'] = applicantstatus()._list()
                        response['jobvacancy'] = Jobvacancy()._list()
                        response['history_education'] = history_education()._list()
                        response['job_experience'] = job_experience()._list()
                        response['client'] = clients()._list()
                        response['status_address'] = list_status_address()._list()
                        response['level_education'] = level_education()._list()
                        response['province'] = province()._list()
                        response['role'] = list_role()._list(tempid)
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/user', methods = ['GET', 'POST'])
def datauser():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                if user.verify_access('view', 1):
                        if session['client'] is True:
                                tempid = current_user.id
                        else:                
                                tempid = current_user.client_id
                        response['employee'] = User()._employee(tempid)
                        response['applicantstatus'] = applicantstatus()._list()
                        response['jobvacancy'] = Jobvacancy()._list()
                        response['history_education'] = history_education()._list()
                        response['job_experience'] = job_experience()._list()
                        response['client'] = clients()._list()
                        response['status_address'] = list_status_address()._list()
                        response['level_education'] = level_education()._list()
                        response['province'] = province()._list()
                        response['role'] = list_role()._list(tempid)
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/userdetail', methods = ['GET', 'POST'])
def dataformuser():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        response['dataform'] = {}
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                check = User.query.filter_by(id = apidata['user_id']).first()
                if check is not None:
                        response['employee'] = User()._employeedetail(apidata['user_id'])
                        response['dataform']['applicantstatus'] = applicantstatus()._list()
                        response['dataform']['jobvacancy'] = Jobvacancy()._list()
                        response['dataform']['history_education'] = history_education()._list()
                        response['dataform']['job_experience'] = job_experience()._list()
                        response['dataform']['status_address'] = list_status_address()._list()
                        response['dataform']['level_education'] = level_education()._list()
                        response['dataform']['province'] = province()._list()
                        if 'id' in response['employee']['province_id']:
                                response['dataform']['city'] = city()._list(response['employee']['province_id']['id'])
                        if 'id' in response['employee']['city_id']:
                                response['dataform']['kecamatan'] = kecamatan()._list(response['employee']['city_id']['id'])
                        if 'id' in response['employee']['kecamatan_id']:
                                response['dataform']['kelurahan'] = kelurahan()._list(response['employee']['kecamatan_id']['id'])
                        if 'id' in response['employee']['kelurahan_id']:
                                response['dataform']['postal_code'] = postal_code()._list(response['employee']['kelurahan_id']['id'])
                        if 'province_id' in response['employee']['cor-address']:
                                if 'id' in response['employee']['cor-address']['province_id']:
                                        response['dataform']['cor-city'] = city()._list(response['employee']['cor-address']['province_id']['id'])
                                if 'id' in response['employee']['cor-address']['city_id']:
                                        response['dataform']['cor-kecamatan'] = kecamatan()._list(response['employee']['cor-address']['city_id']['id'])
                                if 'id' in response['employee']['cor-address']['kecamatan_id']:
                                        response['dataform']['cor-kelurahan'] = kelurahan()._list(response['employee']['cor-address']['kecamatan_id']['id'])
                                if 'id' in response['employee']['cor-address']['kelurahan_id']:
                                        response['dataform']['cor-postal_code'] = postal_code()._list(response['employee']['cor-address']['kelurahan_id']['id'])

                        response['dataform']['client'] = clients()._list()
                        response['status'] = '200'
                else:
                        response['message'] = 'User Tidak Terdaftar'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/employeedetail', methods = ['GET', 'POST'])
def dataformemployee():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        response['dataform'] = {}
        apidata = request.form 
        if session['client'] is True:
                tempid = current_user.id
        else:
                tempid = current_user.client_id    
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = User.query.filter_by(id = apidata['user_id']).first()
                if check is not None:
                        if access.verify_access('view', 1):
                                response['employee'] = User()._employeedetail(apidata['user_id'])
                                response['dataform']['applicantstatus'] = applicantstatus()._list()
                                response['dataform']['jobvacancy'] = Jobvacancy()._list()
                                response['dataform']['history_education'] = history_education()._list()
                                response['dataform']['job_experience'] = job_experience()._list()
                                response['dataform']['status_address'] = list_status_address()._list()
                                response['dataform']['level_education'] = level_education()._list()
                                response['dataform']['province'] = province()._list()
                                if 'id' in response['employee']['province_id']:
                                        response['dataform']['city'] = city()._list(response['employee']['province_id']['id'])
                                
                                if 'id' in response['employee']['city_id']:
                                        response['dataform']['kecamatan'] = kecamatan()._list(response['employee']['city_id']['id'])
                
                                if 'id' in response['employee']['kecamatan_id']:
                                        response['dataform']['kelurahan'] = kelurahan()._list(response['employee']['kecamatan_id']['id'])

                                if 'id' in response['employee']['kelurahan_id']:
                                        response['dataform']['postal_code'] = postal_code()._list(response['employee']['kelurahan_id']['id'])
                                
                                if 'province_id' in response['employee']['cor-address']:
                                        if 'id' in response['employee']['cor-address']['province_id']:
                                                response['dataform']['cor-city'] = city()._list(response['employee']['cor-address']['province_id']['id'])
                                        
                                        if 'id' in response['employee']['cor-address']['city_id']:
                                                response['dataform']['cor-kecamatan'] = kecamatan()._list(response['employee']['cor-address']['city_id']['id'])
                                        
                                        if 'id' in response['employee']['cor-address']['kecamatan_id']:
                                                response['dataform']['cor-kelurahan'] = kelurahan()._list(response['employee']['cor-address']['kecamatan_id']['id'])
                                                
                                        if 'id' in response['employee']['cor-address']['kelurahan_id']:
                                                response['dataform']['cor-postal_code'] = postal_code()._list(response['employee']['cor-address']['kelurahan_id']['id'])

                                response['dataform']['client'] = clients()._list()
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        response['message'] = 'User Tidak Terdaftar'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)
        
@core.route('/api/V1.0/dataforaddress', methods = ['GET', 'POST'])
def dataforaddress():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                response['province'] = province()._list()
                response['city'] = city()._listall()
                response['kecamatan'] = kecamatan()._listall()
                response['kelurahan'] = kelurahan()._listall()
                response['postal_code'] = postal_code()._listall()
                response['status'] = '200'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertemployee', methods = ['GET', 'POST'])
def addemployee():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        apifile = request.files
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if 'name' in apidata and 'nik' in apidata and 'phonenumber' in apidata and 'password_hash' in apidata and 'pin_hash' in apidata and 'email' in apidata and 'birthdate' in apidata and 'birthplace' in apidata and 'address' in apidata and 'gender' in apidata and 'religion' in apidata and 'marital' in apidata and 'province' in apidata and 'city' in apidata and 'kecamatan' in apidata and 'kelurahan' in apidata and 'postalcode' in apidata and 'rt' in apidata and 'rw' in apidata and 'client_id' in apidata and 'applicantstatus_id' in apidata and 'jobposition_id' in apidata:
                        employe = User.query.filter_by(id=apidata['user_id']).first()
                        if employe is None:
                                checkphonenumber = User.query.filter_by(phone_number = apidata['phonenumber'], status = True).first()
                                checkemail = User.query.filter_by(email = apidata['email'], status = True).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                if access.verify_access('insert', 1):
                                                        new_user = User()._insert(apidata['name'], apidata['nik'], apidata['phonenumber'], apidata['password_hash'], apidata['pin_hash'], apidata['email'], apidata['birthdate'], apidata['birthplace'], apidata['address'], apidata['gender'], apidata['religion'], apidata['marital'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['client_id'], apidata['applicantstatus_id'], apidata['jobposition_id'])
                                                        response['status'] = '200'
                                                        response['user_id'] = new_user.id
                                                else:
                                                        response['message'] = 'Akses Ditolak!'
                                                        response['status'] = '400'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                        else:
                                checkphonenumber = User.query.filter_by(phone_number = apidata['phonenumber'], status = True).filter(User.id != apidata['user_id']).first()
                                checkemail = User.query.filter_by(email = apidata['email'], status = True).filter(User.id != apidata['user_id']).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                if access.verify_access('update', 1):
                                                        User()._update(apidata['user_id'], apidata['name'], apidata['nik'], apidata['phonenumber'], apidata['email'], apidata['birthdate'], apidata['birthplace'], apidata['address'], apidata['gender'], apidata['religion'], apidata['marital'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['client_id'], apidata['applicantstatus_id'], apidata['jobposition_id'])
                                                        response['status'] = '200'
                                                else:
                                                        response['message'] = 'Akses Ditolak!'
                                                        response['status'] = '400'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'                                           
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route("/api/V1.0/checkuser", methods = ['GET','POST'])
def checkuser():
    response = {}
    apidata = request.form
    user = User.query.filter_by(id = apidata['cur_user'], status = True).first()
    if user is not None:
            response['status'] = '200'
            response['message'] = 'Successfully Apply For a Job'
    else:
            response['message'] = 'You are not logged in. Please login first.'
            response['status'] = '400'
    return jsonify(response)

@core.route("/api/V1.0/applyjob", methods = ['GET','POST'])
def applyjob():
    response = {}
    response['status'] = '400'
    apidata = request.form
    user = User.query.filter_by(id = apidata['cur_user'], status = True).first()
    if user is not None:
        if 'applicantstatus_id' in apidata and 'jobposition_id' in apidata:
                User()._applyjob(apidata['user_id'], apidata['applicantstatus_id'], apidata['jobposition_id'])
                response['status'] = '200'
                response['message'] = 'Successfully Apply For a Job'
        else:
                response['message'] = 'Data Tidak Lengkap'
                response['status'] = '400'                                           
    else:
            response['message'] = 'You are not logged in. Please login first.'
            response['status'] = '400'
    return jsonify(response)

@core.route('/api/V1.0/insertuser', methods = ['GET', 'POST'])
def adduser():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        apifile = request.files
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                if 'name' in apidata and 'nik' in apidata and 'phonenumber' in apidata and 'email' in apidata and 'birthdate' in apidata and 'birthplace' in apidata and 'address' in apidata and 'gender' in apidata and 'religion' in apidata and 'marital' in apidata and 'province' in apidata and 'city' in apidata and 'kecamatan' in apidata and 'kelurahan' in apidata and 'postalcode' in apidata and 'rt' in apidata and 'rw' in apidata and 'client_id' in apidata:
                        employe = User.query.filter_by(id=apidata['user_id']).first()
                        if employe is None:
                                checkphonenumber = User.query.filter_by(phone_number = apidata['phonenumber'], status = True).first()
                                checkemail = User.query.filter_by(email = apidata['email'], status = True).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                new_user = User()._insert(apidata['name'], apidata['nik'], apidata['phonenumber'], apidata['email'], apidata['birthdate'], apidata['birthplace'], apidata['address'], apidata['gender'], apidata['religion'], apidata['marital'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['client_id'])
                                                response['status'] = '200'
                                                response['user_id'] = new_user.id
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                        else:
                                checkphonenumber = User.query.filter_by(phone_number = apidata['phonenumber'], status = True).filter(User.id != apidata['user_id']).first()
                                checkemail = User.query.filter_by(email = apidata['email'], status = True).filter(User.id != apidata['user_id']).first()
                                if checkemail is None:
                                        if checkphonenumber is None:
                                                User()._updateuser(apidata['user_id'], apidata['name'], apidata['nik'], apidata['phonenumber'], apidata['email'], apidata['birthdate'], apidata['birthplace'], apidata['address'], apidata['gender'], apidata['religion'], apidata['marital'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['client_id'])
                                                response['status'] = '200'
                                        else:
                                                response['message'] = 'Nomer Telepon Sudah Terdaftar'
                                else:
                                        response['message'] = 'Email Sudah Terdaftar'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'                                           
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/jobvacancy', methods = ['GET', 'POST'])
def datajobvacancy():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('view', 1):
                        if session['client'] is True:
                                tempid = current_user.id
                        else:                
                                tempid = current_user.client_id
                        response['jobvacancy'] = Jobvacancy()._jobvacancy(tempid)
                        response['client'] = clients()._list()
                        response['division'] = division()._list()
                        response['jobtype'] = jobtype()._list()
                        response['branch'] = branch()._list()
                        response['experience'] = experience()._list()
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/jobvacancydetail', methods = ['GET', 'POST'])
def dataforvacancy():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        response['dataform'] = {}
        apidata = request.form 
        if session['client'] is True:
                tempid = current_user.id
        else:
                tempid = current_user.client_id    
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('view', 5):
                        response['jobvacancy'] = Jobvacancy()._jobvacancydetail(apidata['jobvacancy_id'])
                        response['dataform']['client'] = clients()._list()
                        response['dataform']['division'] = division()._list()
                        response['dataform']['jobtype'] = jobtype()._list()
                        response['dataform']['branch'] = branch()._list()
                        response['dataform']['experience'] = experience()._list()
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertjobvacancy', methods = ['GET', 'POST'])
def addjobvacancy():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if 'jobposition' in apidata and 'description' in apidata and 'client_id' in apidata and 'salary' in apidata and  'applicationdate' in apidata and 'requirement' in apidata and 'experience' in apidata and 'division_id' in apidata and 'jobtype_id' in apidata and 'branch_id' in apidata and 'experience_id' in apidata:
                        jobvacancy = Jobvacancy.query.filter_by(id=apidata['jobvacancy_id']).first()
                        if jobvacancy is None:
                                if access.verify_access('insert', 1):
                                        new_vacancy = Jobvacancy()._insert(apidata['jobposition'], apidata['description'], apidata['client_id'], apidata['salary'], apidata['applicationdate'], apidata['requirement'], apidata['experience'], apidata['division_id'], apidata['jobtype_id'], apidata['branch_id'], apidata['experience_id'])
                                        response['status'] = '200'
                                        response['jobvacancy_id'] = new_vacancy.id
                                else:
                                        response['message'] = 'Akses Ditolak!'
                                        response['status'] = '400'
                        else:
                                if access.verify_access('update', 1):
                                        Jobvacancy()._update(apidata['jobvacancy_id'], apidata['jobposition'], apidata['description'], apidata['client_id'], apidata['salary'], apidata['applicationdate'], apidata['requirement'], apidata['experience'], apidata['division_id'], apidata['jobtype_id'], apidata['branch_id'], apidata['experience_id'])
                                        response['status'] = '200'
                                else:
                                        response['message'] = 'Akses Ditolak!'
                                        response['status'] = '400'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'                                           
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertfilejv', methods = ['GET', 'POST'])
def addfilejv():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        apifile = request.files
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                jobvacancy = Jobvacancy.query.filter_by(id = apidata['jobvacancy_id']).first()
                if jobvacancy is None:
                        if access.verify_access('insert', 1):
                                if 'fotojob' in apifile:  
                                        response['fotojob'] = '200'
                                        stored_file = resize_files(apidata["jobvacancy_id"], apifile['fotojob'], int('01'))
                                        if stored_file['status'] == '200':
                                            Vacancy_Image()._insert(stored_file['name'], apidata["jobvacancy_id"], stored_file['image_id'])
                                        response = stored_file
                                if 'filejob' in apifile:
                                        stored_file = resize_cv(apidata["jobvacancy_id"], apifile['filejob'], int('02'))
                                        if stored_file['status'] == '200':
                                            Vacancy_Image()._insert(stored_file['name'], apidata["jobvacancy_id"], stored_file['image_id'])
                                        response = stored_file
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        if access.verify_access('update', 1):
                            fotojob = Vacancy_Image()._data(apidata['fotojob_id'])
                            filejob = Vacancy_Image()._data(apidata['filejob_id'])
                            if len(fotojob) > 0:                    
                                if 'fotojob' in apifile:
                                    Vacancy_Image()._remove(fotojob['id'])
                                    stored_file = resize_files(apidata["jobvacancy_id"], apifile['fotojob'], int('01'))
                                    if stored_file['status'] == '00':
                                        Vacancy_Image()._insert(stored_file['name'], apidata["jobvacancy_id"], stored_file['image_id'])
                                    response = stored_file
                            else:
                                if 'fotojob' in apifile:
                                    stored_file = resize_files(apidata["jobvacancy_id"], apifile['fotojob'], int('01'))
                                    if stored_file['status'] == '00':
                                        Vacancy_Image()._insert(stored_file['name'], apidata["jobvacancy_id"], stored_file['image_id'])
                            if len(filejob) > 0: 
                                if 'filejob' in apifile:
                                    Vacancy_Image()._remove(filejob['id'])
                                    stored_file = resize_cv(apidata["jobvacancy_id"], apifile['filejob'], int('02'))
                                    Vacancy_Image()._insert(stored_file['name'],apidata["jobvacancy_id"] , stored_file['image_id'])
                            else:
                                if 'filejob' in apifile:
                                    stored_file = resize_cv(apidata["jobvacancy_id"], apifile['filejob'], int('02'))
                                    Vacancy_Image()._insert(stored_file['name'],apidata["jobvacancy_id"], stored_file['image_id'])
                                    response = stored_file 
                            response['status'] = '200'
                        else:
                            response['message'] = 'Akses Ditolak!'
                            response['status'] = '400'                                         
        else:
            response['message'] = 'User Tidak Terverifikasi'
            response['status'] = '400'
    return jsonify(response)


@core.route('/api/V1.0/removejobvacancy', methods = ['GET','POST'])
def removejobvacancy():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('remove', 1):
                        removeid = Jobvacancy()._remove(apidata['id'])
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['status'] = '400'
                response['message'] = 'User Tidak Terverifikasi'
        return jsonify(response)

@core.route('/api/V1.0/insert_user_file', methods = ['GET', 'POST'])
def adduserfile():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        apifile = request.files
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                employe = User.query.filter_by(id = apidata['user_id']).first()
                if employe is None:
                        if 'imgcv' in apifile:
                            response['imgcv'] = '200'
                            stored_file = resize_cv(apidata["user_id"], apifile['imgcv'], int('03'))   
                            response = stored_file
                            if stored_file['status'] == '200':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                            response = stored_file
                        if 'fotoktp' in apifile:  
                            response['fotoktp'] = '200'
                            stored_file = resize_files(apidata["user_id"], apifile['fotoktp'], int('04'))
                            if stored_file['status'] == '200':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                            response = stored_file
                        if 'fotonpwp' in apifile:  
                            response['fotonpwp'] = '200'
                            stored_file = resize_files(apidata["user_id"], apifile['fotonpwp'], int('05'))
                            if stored_file['status'] == '200':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                            response = stored_file
                        if 'imgfile' in apifile:
                            stored_file = resize_files(apidata["user_id"], apifile['imgfile'], int('02'))
                            if stored_file['status'] == '200':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                            response = stored_file
                        response['status'] = '200'
                else:
                        picture = Image_Service()._data(apidata['pic_id'])
                        cv = Image_Service()._data(apidata['cv_id'])
                        ktp = Image_Service()._data(apidata['ktp_id'])
                        npwp = Image_Service()._data(apidata['npwp_id'])
                        if len(cv) > 0: 
                            if 'imgcv' in apifile:
                                Image_Service()._remove(cv['id'])
                                stored_file = resize_cv(apidata["user_id"], apifile['imgcv'], int('03'))        
                                Image_Service()._insert(stored_file['name'],apidata["user_id"] , stored_file['image_id'])
                        else:
                            if 'imgcv' in apifile:
                                stored_file = resize_cv(apidata["user_id"], apifile['imgcv'], int('03'))        
                                Image_Service()._insert(stored_file['name'],apidata["user_id"], stored_file['image_id']) 
                        if len(picture) > 0:                    
                            if 'imgfile' in apifile:
                                Image_Service()._remove(picture['id'])
                                stored_file = resize_files(apidata["user_id"], apifile['imgfile'], int('02'))
                                if stored_file['status'] == '00':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                response = stored_file
                        else:
                            if 'imgfile' in apifile:
                                stored_file = resize_files(apidata["user_id"], apifile['imgfile'], int('02'))
                                if stored_file['status'] == '00':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                response = stored_file  
                        if len(ktp) > 0:                    
                            if 'fotoktp' in apifile:
                                Image_Service()._remove(ktp['id'])
                                stored_file = resize_files(apidata["user_id"], apifile['fotoktp'], int('04'))
                                if stored_file['status'] == '00':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                response = stored_file
                        else:
                            if 'fotoktp' in apifile:
                                stored_file = resize_files(apidata["user_id"], apifile['fotoktp'], int('04'))
                                if stored_file['status'] == '00':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                response = stored_file
                        if len(npwp) > 0:                    
                            if 'fotonpwp' in apifile:
                                Image_Service()._remove(npwp['id'])
                                stored_file = resize_files(apidata["user_id"], apifile['fotonpwp'], int('05'))
                                if stored_file['status'] == '00':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                response = stored_file
                        else:
                            if 'fotonpwp' in apifile:
                                stored_file = resize_files(apidata["user_id"], apifile['fotonpwp'], int('05'))
                                if stored_file['status'] == '00':
                                    Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                response = stored_file 
                        response['status'] = '200'                                       
        else:
            response['message'] = 'User Tidak Terverifikasi'
            response['status'] = '400'
    return jsonify(response)


@core.route('/api/V1.0/insertfile', methods = ['GET', 'POST'])
def addfile():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        apifile = request.files
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                employe = User.query.filter_by(id = apidata['user_id']).first()
                if employe is None:
                        if access.verify_access('insert', 1):
                                if 'imgcv' in apifile:
                                        response['imgcv'] = '200'
                                        stored_file = resize_cv(apidata["user_id"], apifile['imgcv'], int('03'))   
                                        response = stored_file
                                        if stored_file['status'] == '200':
                                            Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                        response = stored_file
                                if 'fotoktp' in apifile:  
                                        response['fotoktp'] = '200'
                                        stored_file = resize_files(apidata["user_id"], apifile['fotoktp'], int('04'))
                                        if stored_file['status'] == '200':
                                            Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                        response = stored_file
                                if 'fotonpwp' in apifile:  
                                        response['fotonpwp'] = '200'
                                        stored_file = resize_files(apidata["user_id"], apifile['fotonpwp'], int('05'))
                                        if stored_file['status'] == '200':
                                            Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                        response = stored_file
                                if 'imgfile' in apifile:
                                        stored_file = resize_files(apidata["user_id"], apifile['imgfile'], int('02'))
                                        if stored_file['status'] == '200':
                                            Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                        response = stored_file
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        if access.verify_access('update', 1):
                            picture = Image_Service()._data(apidata['pic_id'])
                            cv = Image_Service()._data(apidata['cv_id'])
                            ktp = Image_Service()._data(apidata['ktp_id'])
                            npwp = Image_Service()._data(apidata['npwp_id'])
                            if len(cv) > 0: 
                                if 'imgcv' in apifile:
                                    Image_Service()._remove(cv['id'])
                                    stored_file = resize_cv(apidata["user_id"], apifile['imgcv'], int('03'))        
                                    Image_Service()._insert(stored_file['name'],apidata["user_id"] , stored_file['image_id'])
                            else:
                                if 'imgcv' in apifile:
                                    stored_file = resize_cv(apidata["user_id"], apifile['imgcv'], int('03'))        
                                    Image_Service()._insert(stored_file['name'],apidata["user_id"], stored_file['image_id']) 
                            if len(picture) > 0:                    
                                if 'imgfile' in apifile:
                                    Image_Service()._remove(picture['id'])
                                    stored_file = resize_files(apidata["user_id"], apifile['imgfile'], int('02'))
                                    if stored_file['status'] == '00':
                                        Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                    response = stored_file
                            else:
                                if 'imgfile' in apifile:
                                    stored_file = resize_files(apidata["user_id"], apifile['imgfile'], int('02'))
                                    if stored_file['status'] == '00':
                                        Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                    response = stored_file  
                            if len(ktp) > 0:                    
                                if 'fotoktp' in apifile:
                                    Image_Service()._remove(ktp['id'])
                                    stored_file = resize_files(apidata["user_id"], apifile['fotoktp'], int('04'))
                                    if stored_file['status'] == '00':
                                        Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                    response = stored_file
                            else:
                                if 'fotoktp' in apifile:
                                    stored_file = resize_files(apidata["user_id"], apifile['fotoktp'], int('04'))
                                    if stored_file['status'] == '00':
                                        Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                    response = stored_file
                            if len(npwp) > 0:                    
                                if 'fotonpwp' in apifile:
                                    Image_Service()._remove(npwp['id'])
                                    stored_file = resize_files(apidata["user_id"], apifile['fotonpwp'], int('05'))
                                    if stored_file['status'] == '00':
                                        Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                    response = stored_file
                            else:
                                if 'fotonpwp' in apifile:
                                    stored_file = resize_files(apidata["user_id"], apifile['fotonpwp'], int('05'))
                                    if stored_file['status'] == '00':
                                        Image_Service()._insert(stored_file['name'], apidata["user_id"], stored_file['image_id'])
                                    response = stored_file 
                            response['status'] = '200'
                        else:
                            response['message'] = 'Akses Ditolak!'
                            response['status'] = '400'                                         
        else:
            response['message'] = 'User Tidak Terverifikasi'
            response['status'] = '400'
    return jsonify(response)


@core.route('/api/V1.0/removeemployee', methods = ['GET','POST'])
def removeuser():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if access.verify_access('remove', 1):
                        removeid = User()._remove(apidata['id'])
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['status'] = '400'
                response['message'] = 'User Tidak Terverifikasi'
        return jsonify(response)

@core.route('/api/V1.0/insert_user_education', methods = ['GET', 'POST'])
def usereducation():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            if 'user_id' in apidata and 'lastedu' in apidata and 'nama_sd' in apidata and 'kota_sd' in apidata and 'jurusan_sd' in apidata and 'masuk_sd' in apidata and 'lulus_sd' in apidata and 'status_sd' in apidata and 'nama_smp' in apidata and 'kota_smp' in apidata and 'jurusan_smp' in apidata and 'masuk_smp' in apidata and 'lulus_smp' in apidata and 'status_smp' in apidata and 'nama_sma' in apidata and 'kota_sma' in apidata and 'jurusan_sma' in apidata and 'masuk_sma' in apidata and 'lulus_sma' in apidata and 'status_sma' in apidata and 'nama_s1' in apidata and 'kota_s1' in apidata and 'jurusan_s1' in apidata and 'masuk_s1' in apidata and 'lulus_s1' in apidata and 'status_s1' in apidata and 'nama_s2' in apidata and 'kota_s2' in apidata and 'jurusan_s2' in apidata and 'masuk_s2' in apidata and 'lulus_s2' in apidata and 'status_s2' in apidata and 'nama_s3' in apidata and 'kota_s3' in apidata and 'jurusan_s3' in apidata and 'masuk_s3' in apidata and 'lulus_s3' in apidata and 'status_s3' in apidata and 'bidang1' in apidata and 'penyelenggara1' in apidata and 'kota_kursus1' in apidata and 'lama_kursus1' in apidata and 'tahun_masuk1' in apidata and 'biaya1' in apidata and 'bidang2' in apidata and 'penyelenggara2' in apidata and 'kota_kursus2' in apidata and 'lama_kursus2' in apidata and 'tahun_masuk2' in apidata and 'biaya2' in apidata and 'bidang3' in apidata and 'penyelenggara3' in apidata and 'kota_kursus3' in apidata and 'lama_kursus3' in apidata and 'tahun_masuk3' in apidata and 'biaya3' in apidata and 'bidang4' in apidata and 'penyelenggara4' in apidata and 'kota_kursus4' in apidata and 'lama_kursus4' in apidata and 'tahun_masuk4' in apidata and 'biaya4' in apidata and 'bidang5' in apidata and 'penyelenggara5' in apidata and 'kota_kursus5' in apidata and 'lama_kursus5' in apidata and 'tahun_masuk5' in apidata and 'biaya5' in apidata and 'bidang6' in apidata and 'penyelenggara6' in apidata and 'kota_kursus6' in apidata and 'lama_kursus6' in apidata and 'tahun_masuk6' in apidata and 'biaya6' in apidata:
                edulist = history_education.query.filter_by(user_id = apidata['user_id']).first() 
                if edulist is None:
                        history_education()._insert(apidata['user_id'], apidata['lastedu'], apidata['nama_sd'], apidata['kota_sd'], apidata['jurusan_sd'], apidata['masuk_sd'], apidata['lulus_sd'], apidata['status_sd'], apidata['nama_smp'], apidata['kota_smp'], apidata['jurusan_smp'], apidata['masuk_smp'], apidata['lulus_smp'], apidata['status_smp'], apidata['nama_sma'], apidata['kota_sma'], apidata['jurusan_sma'], apidata['masuk_sma'], apidata['lulus_sma'], apidata['status_sma'], apidata['nama_s1'], apidata['kota_s1'], apidata['jurusan_s1'], apidata['masuk_s1'], apidata['lulus_s1'], apidata['status_s1'], apidata['nama_s2'], apidata['kota_s2'], apidata['jurusan_s2'], apidata['masuk_s2'], apidata['lulus_s2'], apidata['status_s2'], apidata['nama_s3'], apidata['kota_s3'], apidata['jurusan_s3'], apidata['masuk_s3'], apidata['lulus_s3'], apidata['status_s3'], apidata['bidang1'], apidata['penyelenggara1'], apidata['kota_kursus1'], apidata['lama_kursus1'], apidata['tahun_masuk1'], apidata['biaya1'], apidata['bidang2'], apidata['penyelenggara2'], apidata['kota_kursus2'], apidata['lama_kursus2'], apidata['tahun_masuk2'], apidata['biaya2'], apidata['bidang3'], apidata['penyelenggara3'], apidata['kota_kursus3'], apidata['lama_kursus3'], apidata['tahun_masuk3'], apidata['biaya3'], apidata['bidang4'], apidata['penyelenggara4'], apidata['kota_kursus4'], apidata['lama_kursus4'], apidata['tahun_masuk4'], apidata['biaya4'], apidata['bidang5'], apidata['penyelenggara5'], apidata['kota_kursus5'], apidata['lama_kursus5'], apidata['tahun_masuk5'], apidata['biaya5'], apidata['bidang6'], apidata['penyelenggara6'], apidata['kota_kursus6'], apidata['lama_kursus6'], apidata['tahun_masuk6'], apidata['biaya6'])
                        response['status'] = '200'
                else :
                        history_education()._update(edulist.id, apidata['lastedu'], apidata['nama_sd'], apidata['kota_sd'], apidata['jurusan_sd'], apidata['masuk_sd'], apidata['lulus_sd'], apidata['status_sd'], apidata['nama_smp'], apidata['kota_smp'], apidata['jurusan_smp'], apidata['masuk_smp'], apidata['lulus_smp'], apidata['status_smp'], apidata['nama_sma'], apidata['kota_sma'], apidata['jurusan_sma'], apidata['masuk_sma'], apidata['lulus_sma'], apidata['status_sma'], apidata['nama_s1'], apidata['kota_s1'], apidata['jurusan_s1'], apidata['masuk_s1'], apidata['lulus_s1'], apidata['status_s1'], apidata['nama_s2'], apidata['kota_s2'], apidata['jurusan_s2'], apidata['masuk_s2'], apidata['lulus_s2'], apidata['status_s2'], apidata['nama_s3'], apidata['kota_s3'], apidata['jurusan_s3'], apidata['masuk_s3'], apidata['lulus_s3'], apidata['status_s3'], apidata['bidang1'], apidata['penyelenggara1'], apidata['kota_kursus1'], apidata['lama_kursus1'], apidata['tahun_masuk1'], apidata['biaya1'], apidata['bidang2'], apidata['penyelenggara2'], apidata['kota_kursus2'], apidata['lama_kursus2'], apidata['tahun_masuk2'], apidata['biaya2'], apidata['bidang3'], apidata['penyelenggara3'], apidata['kota_kursus3'], apidata['lama_kursus3'], apidata['tahun_masuk3'], apidata['biaya3'], apidata['bidang4'], apidata['penyelenggara4'], apidata['kota_kursus4'], apidata['lama_kursus4'], apidata['tahun_masuk4'], apidata['biaya4'], apidata['bidang5'], apidata['penyelenggara5'], apidata['kota_kursus5'], apidata['lama_kursus5'], apidata['tahun_masuk5'], apidata['biaya5'], apidata['bidang6'], apidata['penyelenggara6'], apidata['kota_kursus6'], apidata['lama_kursus6'], apidata['tahun_masuk6'], apidata['biaya6'])
                        response['status'] = '200'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/inserteducation', methods = ['GET', 'POST'])
def addeducation():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
            if 'user_id' in apidata and 'lastedu' in apidata and 'nama_sd' in apidata and 'kota_sd' in apidata and 'jurusan_sd' in apidata and 'masuk_sd' in apidata and 'lulus_sd' in apidata and 'status_sd' in apidata and 'nama_smp' in apidata and 'kota_smp' in apidata and 'jurusan_smp' in apidata and 'masuk_smp' in apidata and 'lulus_smp' in apidata and 'status_smp' in apidata and 'nama_sma' in apidata and 'kota_sma' in apidata and 'jurusan_sma' in apidata and 'masuk_sma' in apidata and 'lulus_sma' in apidata and 'status_sma' in apidata and 'nama_s1' in apidata and 'kota_s1' in apidata and 'jurusan_s1' in apidata and 'masuk_s1' in apidata and 'lulus_s1' in apidata and 'status_s1' in apidata and 'nama_s2' in apidata and 'kota_s2' in apidata and 'jurusan_s2' in apidata and 'masuk_s2' in apidata and 'lulus_s2' in apidata and 'status_s2' in apidata and 'nama_s3' in apidata and 'kota_s3' in apidata and 'jurusan_s3' in apidata and 'masuk_s3' in apidata and 'lulus_s3' in apidata and 'status_s3' in apidata and 'bidang1' in apidata and 'penyelenggara1' in apidata and 'kota_kursus1' in apidata and 'lama_kursus1' in apidata and 'tahun_masuk1' in apidata and 'biaya1' in apidata and 'bidang2' in apidata and 'penyelenggara2' in apidata and 'kota_kursus2' in apidata and 'lama_kursus2' in apidata and 'tahun_masuk2' in apidata and 'biaya2' in apidata and 'bidang3' in apidata and 'penyelenggara3' in apidata and 'kota_kursus3' in apidata and 'lama_kursus3' in apidata and 'tahun_masuk3' in apidata and 'biaya3' in apidata and 'bidang4' in apidata and 'penyelenggara4' in apidata and 'kota_kursus4' in apidata and 'lama_kursus4' in apidata and 'tahun_masuk4' in apidata and 'biaya4' in apidata and 'bidang5' in apidata and 'penyelenggara5' in apidata and 'kota_kursus5' in apidata and 'lama_kursus5' in apidata and 'tahun_masuk5' in apidata and 'biaya5' in apidata and 'bidang6' in apidata and 'penyelenggara6' in apidata and 'kota_kursus6' in apidata and 'lama_kursus6' in apidata and 'tahun_masuk6' in apidata and 'biaya6' in apidata:
                edulist = history_education.query.filter_by(user_id = apidata['user_id']).first() 
                if edulist is None:
                        if access.verify_access('insert', 1):
                                history_education()._insert(apidata['user_id'], apidata['lastedu'], apidata['nama_sd'], apidata['kota_sd'], apidata['jurusan_sd'], apidata['masuk_sd'], apidata['lulus_sd'], apidata['status_sd'], apidata['nama_smp'], apidata['kota_smp'], apidata['jurusan_smp'], apidata['masuk_smp'], apidata['lulus_smp'], apidata['status_smp'], apidata['nama_sma'], apidata['kota_sma'], apidata['jurusan_sma'], apidata['masuk_sma'], apidata['lulus_sma'], apidata['status_sma'], apidata['nama_s1'], apidata['kota_s1'], apidata['jurusan_s1'], apidata['masuk_s1'], apidata['lulus_s1'], apidata['status_s1'], apidata['nama_s2'], apidata['kota_s2'], apidata['jurusan_s2'], apidata['masuk_s2'], apidata['lulus_s2'], apidata['status_s2'], apidata['nama_s3'], apidata['kota_s3'], apidata['jurusan_s3'], apidata['masuk_s3'], apidata['lulus_s3'], apidata['status_s3'], apidata['bidang1'], apidata['penyelenggara1'], apidata['kota_kursus1'], apidata['lama_kursus1'], apidata['tahun_masuk1'], apidata['biaya1'], apidata['bidang2'], apidata['penyelenggara2'], apidata['kota_kursus2'], apidata['lama_kursus2'], apidata['tahun_masuk2'], apidata['biaya2'], apidata['bidang3'], apidata['penyelenggara3'], apidata['kota_kursus3'], apidata['lama_kursus3'], apidata['tahun_masuk3'], apidata['biaya3'], apidata['bidang4'], apidata['penyelenggara4'], apidata['kota_kursus4'], apidata['lama_kursus4'], apidata['tahun_masuk4'], apidata['biaya4'], apidata['bidang5'], apidata['penyelenggara5'], apidata['kota_kursus5'], apidata['lama_kursus5'], apidata['tahun_masuk5'], apidata['biaya5'], apidata['bidang6'], apidata['penyelenggara6'], apidata['kota_kursus6'], apidata['lama_kursus6'], apidata['tahun_masuk6'], apidata['biaya6'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else :
                        if access.verify_access('update', 1):
                                history_education()._update(edulist.id, apidata['lastedu'], apidata['nama_sd'], apidata['kota_sd'], apidata['jurusan_sd'], apidata['masuk_sd'], apidata['lulus_sd'], apidata['status_sd'], apidata['nama_smp'], apidata['kota_smp'], apidata['jurusan_smp'], apidata['masuk_smp'], apidata['lulus_smp'], apidata['status_smp'], apidata['nama_sma'], apidata['kota_sma'], apidata['jurusan_sma'], apidata['masuk_sma'], apidata['lulus_sma'], apidata['status_sma'], apidata['nama_s1'], apidata['kota_s1'], apidata['jurusan_s1'], apidata['masuk_s1'], apidata['lulus_s1'], apidata['status_s1'], apidata['nama_s2'], apidata['kota_s2'], apidata['jurusan_s2'], apidata['masuk_s2'], apidata['lulus_s2'], apidata['status_s2'], apidata['nama_s3'], apidata['kota_s3'], apidata['jurusan_s3'], apidata['masuk_s3'], apidata['lulus_s3'], apidata['status_s3'], apidata['bidang1'], apidata['penyelenggara1'], apidata['kota_kursus1'], apidata['lama_kursus1'], apidata['tahun_masuk1'], apidata['biaya1'], apidata['bidang2'], apidata['penyelenggara2'], apidata['kota_kursus2'], apidata['lama_kursus2'], apidata['tahun_masuk2'], apidata['biaya2'], apidata['bidang3'], apidata['penyelenggara3'], apidata['kota_kursus3'], apidata['lama_kursus3'], apidata['tahun_masuk3'], apidata['biaya3'], apidata['bidang4'], apidata['penyelenggara4'], apidata['kota_kursus4'], apidata['lama_kursus4'], apidata['tahun_masuk4'], apidata['biaya4'], apidata['bidang5'], apidata['penyelenggara5'], apidata['kota_kursus5'], apidata['lama_kursus5'], apidata['tahun_masuk5'], apidata['biaya5'], apidata['bidang6'], apidata['penyelenggara6'], apidata['kota_kursus6'], apidata['lama_kursus6'], apidata['tahun_masuk6'], apidata['biaya6'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insert_user_job', methods = ['GET', 'POST'])
def adduserjob():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            if 'user_id' in apidata and 'npwp' in apidata and 'bpjstk' in apidata and 'bpjs' in apidata and 'aap1' in apidata and 'klasifikasi1' in apidata and 'ska1' in apidata and 'skastart1' in apidata and 'skaend1' in apidata and 'aap2' in apidata and 'klasifikasi2' in apidata and 'ska2' in apidata and 'skastart2' in apidata and 'skaend2' in apidata and 'aap3' in apidata and 'klasifikasi3' in apidata and 'ska3' in apidata and 'skastart3' in apidata and 'skaend3' in apidata and 'aap4' in apidata and 'klasifikasi4' in apidata and 'ska4' in apidata and 'skastart4' in apidata and 'skaend4' in apidata and 'aap5' in apidata and 'klasifikasi5' in apidata and 'ska5' in apidata and 'skastart5' in apidata and 'skaend5' in apidata and 'company1' in apidata and 'comaddress1' in apidata and 'work_position1' in apidata and 'starttime1' in apidata and 'endtime1' in apidata and 'ket1' in apidata and 'company2' in apidata and 'comaddress2' in apidata and 'work_position2' in apidata and 'starttime2' in apidata and 'endtime2' in apidata and 'ket2' in apidata and 'company3' in apidata and 'comaddress3' in apidata and 'work_position3' in apidata and 'starttime3' in apidata and 'endtime3' in apidata and 'ket3' in apidata and 'company4' in apidata and 'comaddress4' in apidata and 'work_position4' in apidata and 'starttime4' in apidata and 'endtime4' in apidata and 'ket4' in apidata and 'company5' in apidata and 'comaddress5' in apidata and 'work_position5' in apidata and 'starttime5' in apidata and 'endtime5' in apidata and 'ket5' in apidata and 'company6' in apidata and 'comaddress6' in apidata and 'work_position6' in apidata and 'starttime6' in apidata and 'endtime6' in apidata and 'ket6' in apidata and 'project1' in apidata and 'project_address1' in apidata and 'project_position1' in apidata and 'start_project1' in apidata and 'end_project1' in apidata and 'ket_project1' in apidata and 'project2' in apidata and 'project_address2' in apidata and 'project_position2' in apidata and 'start_project2' in apidata and 'end_project2' in apidata and 'ket_project2' in apidata and 'project3' in apidata and 'project_address3' in apidata and 'project_position3' in apidata and 'start_project3' in apidata and 'end_project3' in apidata and 'ket_project3' in apidata and 'project4' in apidata and 'project_address4' in apidata and 'project_position4' in apidata and 'start_project4' in apidata and 'end_project4' in apidata and 'ket_project4' in apidata and 'project5' in apidata and 'project_address5' in apidata and 'project_position5' in apidata and 'start_project5' in apidata and 'end_project5' in apidata and 'ket_project5' in apidata and 'project6' in apidata and 'project_address6' in apidata and 'project_position6' in apidata and 'start_project6' in apidata and 'end_project6' in apidata and 'ket_project6' in apidata:
                jobexperience = job_experience.query.filter_by(user_id = apidata['user_id']).first() 
                if jobexperience is None:
                        job_experience()._insert(apidata['user_id'], apidata['npwp'], apidata['bpjstk'], apidata['bpjs'], apidata['aap1'], apidata['klasifikasi1'], apidata['ska1'], apidata['skastart1'], apidata['skaend1'], apidata['aap2'], apidata['klasifikasi2'], apidata['ska2'], apidata['skastart2'], apidata['skaend2'], apidata['aap3'], apidata['klasifikasi3'], apidata['ska3'], apidata['skastart3'], apidata['skaend3'], apidata['aap4'], apidata['klasifikasi4'], apidata['ska4'], apidata['skastart4'], apidata['skaend4'], apidata['aap5'], apidata['klasifikasi5'], apidata['ska5'], apidata['skastart5'], apidata['skaend5'], apidata['company1'], apidata['comaddress1'], apidata['work_position1'], apidata['starttime1'], apidata['endtime1'], apidata['ket1'], apidata['company2'], apidata['comaddress2'], apidata['work_position2'], apidata['starttime2'], apidata['endtime2'], apidata['ket2'], apidata['company3'], apidata['comaddress3'], apidata['work_position3'], apidata['starttime3'], apidata['endtime3'], apidata['ket3'], apidata['company4'], apidata['comaddress4'], apidata['work_position4'], apidata['starttime4'], apidata['endtime4'], apidata['ket4'], apidata['company5'], apidata['comaddress5'], apidata['work_position5'], apidata['starttime5'], apidata['endtime5'], apidata['ket5'], apidata['company6'], apidata['comaddress6'], apidata['work_position6'], apidata['starttime6'], apidata['endtime6'], apidata['ket6'], apidata['project1'], apidata['project_address1'], apidata['project_position1'], apidata['start_project1'], apidata['end_project1'], apidata['ket_project1'], apidata['project2'], apidata['project_address2'], apidata['project_position2'], apidata['start_project2'], apidata['end_project2'], apidata['ket_project2'], apidata['project3'], apidata['project_address3'], apidata['project_position3'], apidata['start_project3'], apidata['end_project3'], apidata['ket_project3'], apidata['project4'], apidata['project_address4'], apidata['project_position4'], apidata['start_project4'], apidata['end_project4'], apidata['ket_project4'], apidata['project5'], apidata['project_address5'], apidata['project_position5'], apidata['start_project5'], apidata['end_project5'], apidata['ket_project5'], apidata['project6'], apidata['project_address6'], apidata['project_position6'], apidata['start_project6'], apidata['end_project6'], apidata['ket_project6'])
                        response['status'] = '200'
                else :
                        job_experience()._update(jobexperience.id, apidata['npwp'], apidata['bpjstk'], apidata['bpjs'], apidata['aap1'], apidata['klasifikasi1'], apidata['ska1'], apidata['skastart1'], apidata['skaend1'], apidata['aap2'], apidata['klasifikasi2'], apidata['ska2'], apidata['skastart2'], apidata['skaend2'], apidata['aap3'], apidata['klasifikasi3'], apidata['ska3'], apidata['skastart3'], apidata['skaend3'], apidata['aap4'], apidata['klasifikasi4'], apidata['ska4'], apidata['skastart4'], apidata['skaend4'], apidata['aap5'], apidata['klasifikasi5'], apidata['ska5'], apidata['skastart5'], apidata['skaend5'], apidata['company1'], apidata['comaddress1'], apidata['work_position1'], apidata['starttime1'], apidata['endtime1'], apidata['ket1'], apidata['company2'], apidata['comaddress2'], apidata['work_position2'], apidata['starttime2'], apidata['endtime2'], apidata['ket2'], apidata['company3'], apidata['comaddress3'], apidata['work_position3'], apidata['starttime3'], apidata['endtime3'], apidata['ket3'], apidata['company4'], apidata['comaddress4'], apidata['work_position4'], apidata['starttime4'], apidata['endtime4'], apidata['ket4'], apidata['company5'], apidata['comaddress5'], apidata['work_position5'], apidata['starttime5'], apidata['endtime5'], apidata['ket5'], apidata['company6'], apidata['comaddress6'], apidata['work_position6'], apidata['starttime6'], apidata['endtime6'], apidata['ket6'], apidata['project1'], apidata['project_address1'], apidata['project_position1'], apidata['start_project1'], apidata['end_project1'], apidata['ket_project1'], apidata['project2'], apidata['project_address2'], apidata['project_position2'], apidata['start_project2'], apidata['end_project2'], apidata['ket_project2'], apidata['project3'], apidata['project_address3'], apidata['project_position3'], apidata['start_project3'], apidata['end_project3'], apidata['ket_project3'], apidata['project4'], apidata['project_address4'], apidata['project_position4'], apidata['start_project4'], apidata['end_project4'], apidata['ket_project4'], apidata['project5'], apidata['project_address5'], apidata['project_position5'], apidata['start_project5'], apidata['end_project5'], apidata['ket_project5'], apidata['project6'], apidata['project_address6'], apidata['project_position6'], apidata['start_project6'], apidata['end_project6'], apidata['ket_project6'])
                        response['status'] = '200'
                response['status'] = '200'
        return jsonify(response)

@core.route('/api/V1.0/insertjob', methods = ['GET', 'POST'])
def addjob():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
            if 'user_id' in apidata and 'npwp' in apidata and 'bpjstk' in apidata and 'bpjs' in apidata and 'aap1' in apidata and 'klasifikasi1' in apidata and 'ska1' in apidata and 'skastart1' in apidata and 'skaend1' in apidata and 'aap2' in apidata and 'klasifikasi2' in apidata and 'ska2' in apidata and 'skastart2' in apidata and 'skaend2' in apidata and 'aap3' in apidata and 'klasifikasi3' in apidata and 'ska3' in apidata and 'skastart3' in apidata and 'skaend3' in apidata and 'aap4' in apidata and 'klasifikasi4' in apidata and 'ska4' in apidata and 'skastart4' in apidata and 'skaend4' in apidata and 'aap5' in apidata and 'klasifikasi5' in apidata and 'ska5' in apidata and 'skastart5' in apidata and 'skaend5' in apidata and 'company1' in apidata and 'comaddress1' in apidata and 'work_position1' in apidata and 'starttime1' in apidata and 'endtime1' in apidata and 'ket1' in apidata and 'company2' in apidata and 'comaddress2' in apidata and 'work_position2' in apidata and 'starttime2' in apidata and 'endtime2' in apidata and 'ket2' in apidata and 'company3' in apidata and 'comaddress3' in apidata and 'work_position3' in apidata and 'starttime3' in apidata and 'endtime3' in apidata and 'ket3' in apidata and 'company4' in apidata and 'comaddress4' in apidata and 'work_position4' in apidata and 'starttime4' in apidata and 'endtime4' in apidata and 'ket4' in apidata and 'company5' in apidata and 'comaddress5' in apidata and 'work_position5' in apidata and 'starttime5' in apidata and 'endtime5' in apidata and 'ket5' in apidata and 'company6' in apidata and 'comaddress6' in apidata and 'work_position6' in apidata and 'starttime6' in apidata and 'endtime6' in apidata and 'ket6' in apidata and 'project1' in apidata and 'project_address1' in apidata and 'project_position1' in apidata and 'start_project1' in apidata and 'end_project1' in apidata and 'ket_project1' in apidata and 'project2' in apidata and 'project_address2' in apidata and 'project_position2' in apidata and 'start_project2' in apidata and 'end_project2' in apidata and 'ket_project2' in apidata and 'project3' in apidata and 'project_address3' in apidata and 'project_position3' in apidata and 'start_project3' in apidata and 'end_project3' in apidata and 'ket_project3' in apidata and 'project4' in apidata and 'project_address4' in apidata and 'project_position4' in apidata and 'start_project4' in apidata and 'end_project4' in apidata and 'ket_project4' in apidata and 'project5' in apidata and 'project_address5' in apidata and 'project_position5' in apidata and 'start_project5' in apidata and 'end_project5' in apidata and 'ket_project5' in apidata and 'project6' in apidata and 'project_address6' in apidata and 'project_position6' in apidata and 'start_project6' in apidata and 'end_project6' in apidata and 'ket_project6' in apidata:
                jobexperience = job_experience.query.filter_by(user_id = apidata['user_id']).first() 
                if jobexperience is None:
                        if access.verify_access('insert', 1):
                                job_experience()._insert(apidata['user_id'], apidata['npwp'], apidata['bpjstk'], apidata['bpjs'], apidata['aap1'], apidata['klasifikasi1'], apidata['ska1'], apidata['skastart1'], apidata['skaend1'], apidata['aap2'], apidata['klasifikasi2'], apidata['ska2'], apidata['skastart2'], apidata['skaend2'], apidata['aap3'], apidata['klasifikasi3'], apidata['ska3'], apidata['skastart3'], apidata['skaend3'], apidata['aap4'], apidata['klasifikasi4'], apidata['ska4'], apidata['skastart4'], apidata['skaend4'], apidata['aap5'], apidata['klasifikasi5'], apidata['ska5'], apidata['skastart5'], apidata['skaend5'], apidata['company1'], apidata['comaddress1'], apidata['work_position1'], apidata['starttime1'], apidata['endtime1'], apidata['ket1'], apidata['company2'], apidata['comaddress2'], apidata['work_position2'], apidata['starttime2'], apidata['endtime2'], apidata['ket2'], apidata['company3'], apidata['comaddress3'], apidata['work_position3'], apidata['starttime3'], apidata['endtime3'], apidata['ket3'], apidata['company4'], apidata['comaddress4'], apidata['work_position4'], apidata['starttime4'], apidata['endtime4'], apidata['ket4'], apidata['company5'], apidata['comaddress5'], apidata['work_position5'], apidata['starttime5'], apidata['endtime5'], apidata['ket5'], apidata['company6'], apidata['comaddress6'], apidata['work_position6'], apidata['starttime6'], apidata['endtime6'], apidata['ket6'], apidata['project1'], apidata['project_address1'], apidata['project_position1'], apidata['start_project1'], apidata['end_project1'], apidata['ket_project1'], apidata['project2'], apidata['project_address2'], apidata['project_position2'], apidata['start_project2'], apidata['end_project2'], apidata['ket_project2'], apidata['project3'], apidata['project_address3'], apidata['project_position3'], apidata['start_project3'], apidata['end_project3'], apidata['ket_project3'], apidata['project4'], apidata['project_address4'], apidata['project_position4'], apidata['start_project4'], apidata['end_project4'], apidata['ket_project4'], apidata['project5'], apidata['project_address5'], apidata['project_position5'], apidata['start_project5'], apidata['end_project5'], apidata['ket_project5'], apidata['project6'], apidata['project_address6'], apidata['project_position6'], apidata['start_project6'], apidata['end_project6'], apidata['ket_project6'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else :
                        if access.verify_access('update', 1):
                                job_experience()._update(jobexperience.id, apidata['npwp'], apidata['bpjstk'], apidata['bpjs'], apidata['aap1'], apidata['klasifikasi1'], apidata['ska1'], apidata['skastart1'], apidata['skaend1'], apidata['aap2'], apidata['klasifikasi2'], apidata['ska2'], apidata['skastart2'], apidata['skaend2'], apidata['aap3'], apidata['klasifikasi3'], apidata['ska3'], apidata['skastart3'], apidata['skaend3'], apidata['aap4'], apidata['klasifikasi4'], apidata['ska4'], apidata['skastart4'], apidata['skaend4'], apidata['aap5'], apidata['klasifikasi5'], apidata['ska5'], apidata['skastart5'], apidata['skaend5'], apidata['company1'], apidata['comaddress1'], apidata['work_position1'], apidata['starttime1'], apidata['endtime1'], apidata['ket1'], apidata['company2'], apidata['comaddress2'], apidata['work_position2'], apidata['starttime2'], apidata['endtime2'], apidata['ket2'], apidata['company3'], apidata['comaddress3'], apidata['work_position3'], apidata['starttime3'], apidata['endtime3'], apidata['ket3'], apidata['company4'], apidata['comaddress4'], apidata['work_position4'], apidata['starttime4'], apidata['endtime4'], apidata['ket4'], apidata['company5'], apidata['comaddress5'], apidata['work_position5'], apidata['starttime5'], apidata['endtime5'], apidata['ket5'], apidata['company6'], apidata['comaddress6'], apidata['work_position6'], apidata['starttime6'], apidata['endtime6'], apidata['ket6'], apidata['project1'], apidata['project_address1'], apidata['project_position1'], apidata['start_project1'], apidata['end_project1'], apidata['ket_project1'], apidata['project2'], apidata['project_address2'], apidata['project_position2'], apidata['start_project2'], apidata['end_project2'], apidata['ket_project2'], apidata['project3'], apidata['project_address3'], apidata['project_position3'], apidata['start_project3'], apidata['end_project3'], apidata['ket_project3'], apidata['project4'], apidata['project_address4'], apidata['project_position4'], apidata['start_project4'], apidata['end_project4'], apidata['ket_project4'], apidata['project5'], apidata['project_address5'], apidata['project_position5'], apidata['start_project5'], apidata['end_project5'], apidata['ket_project5'], apidata['project6'], apidata['project_address6'], apidata['project_position6'], apidata['start_project6'], apidata['end_project6'], apidata['ket_project6'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insert_user_corespon', methods = ['GET', 'POST'])
def addusercorespon():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                if 'cor-address' in apidata and 'cor-province' in apidata and 'cor-city' in apidata and 'cor-kecamatan' in apidata and 'cor-kelurahan' in apidata and 'cor-postalcode' in apidata and 'cor-rt' in apidata and 'cor-rw' in apidata and 'user_id' in apidata and 'statusaddress' in apidata:    
                        corespon = corespondend_address.query.filter_by(user_id = apidata['user_id']).first()
                        if corespon is None:
                                corespondend_address()._insert(apidata['cor-address'], apidata['cor-province'], apidata['cor-city'], apidata['cor-kecamatan'], apidata['cor-kelurahan'], apidata['cor-postalcode'], apidata['cor-rt'], apidata['cor-rw'], apidata['user_id'], apidata['statusaddress'])   
                                response['status'] = '200'
                        else:
                                corespondend_address()._update(corespon.id, apidata['cor-address'], apidata['cor-province'], apidata['cor-city'], apidata['cor-kecamatan'], apidata['cor-kelurahan'], apidata['cor-postalcode'], apidata['cor-rt'], apidata['cor-rw'], apidata['statusaddress'])    
                                response['status'] = '200'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertcorespon', methods = ['GET', 'POST'])
def addcorespon():
    if request.method == "POST":
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if 'cor-address' in apidata and 'cor-province' in apidata and 'cor-city' in apidata and 'cor-kecamatan' in apidata and 'cor-kelurahan' in apidata and 'cor-postalcode' in apidata and 'cor-rt' in apidata and 'cor-rw' in apidata and 'user_id' in apidata and 'statusaddress' in apidata:    
                        corespon = corespondend_address.query.filter_by(user_id = apidata['user_id']).first()
                        if corespon is None:
                                if access.verify_access('insert', 1):
                                        corespondend_address()._insert(apidata['cor-address'], apidata['cor-province'], apidata['cor-city'], apidata['cor-kecamatan'], apidata['cor-kelurahan'], apidata['cor-postalcode'], apidata['cor-rt'], apidata['cor-rw'], apidata['user_id'], apidata['statusaddress'])   
                                        response['status'] = '200'  
                                else:
                                        response['message'] = 'Akses Ditolak!'
                                        response['status'] = '400'  
                        else:                                   
                                if access.verify_access('update', 1):
                                        corespondend_address()._update(corespon.id, apidata['cor-address'], apidata['cor-province'], apidata['cor-city'], apidata['cor-kecamatan'], apidata['cor-kelurahan'], apidata['cor-postalcode'], apidata['cor-rt'], apidata['cor-rw'], apidata['statusaddress'])    
                                        response['status'] = '200'
                                else:
                                        response['message'] = 'Akses Ditolak!'
                                        response['status'] = '400'
                else:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/images/<path:filename>', methods = ['GET', 'POST'])
def gambar(filename):
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Image_Service.query.filter_by(id = apidata['file_id'], name = filename, status = True).first()
                if check is not None:
                        with open(MEDIA_FOLDER+"/"+filename, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response
                else:
                        with open(MEDIA_FOLDER+"/default2.jpg", "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response

@core.route('/user_images/<path:filename>', methods = ['GET', 'POST'])
def userimages(filename):
        response = {}
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                check = Image_Service.query.filter_by(id = apidata['file_id'], name = filename, status = True).first()
                if check is not None:
                        with open(MEDIA_FOLDER+"/"+filename, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response
                else:
                        with open(MEDIA_FOLDER+"/default2.jpg", "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response

@app.route('/user_uploads', methods = ['GET', 'POST'])
def user_uploads():
        apidata = request.form        
        user = User.query.filter_by(id = apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                check = Image_Service.query.filter_by(id = apidata['cv'], user_id = apidata['id'], status = True).first()
                if check is not None:
                        with open(MEDIA_FOLDER+"/"+check.name, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response


@app.route('/uploads', methods = ['GET', 'POST'])
def uploads():
        apidata = request.form        
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Image_Service.query.filter_by(id = apidata['cv'], user_id = apidata['id'], status = True).first()
                if check is not None:
                        with open(MEDIA_FOLDER+"/"+check.name, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response

@core.route('/vacancy_images/<path:filename>', methods = ['GET', 'POST'])
def foto_vacancy(filename):
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Vacancy_Image.query.filter_by(id = apidata['file_id'], name = filename, status = True).first()
                if check is not None:
                        with open(MEDIA_FOLDER+"/"+filename, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response
                else:
                        with open(MEDIA_FOLDER+"/default2.jpg", "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response

@app.route('/upload_pdf', methods = ['GET', 'POST'])
def uploads_pdf():
        apidata = request.form        
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Vacancy_Image.query.filter_by(id = apidata['filejob'], jobvacancy_id = apidata['id'], status = True).first()
                if check is not None:
                        with open(MEDIA_FOLDER+"/"+check.name, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read())
                                response = encoded_string
                        return response

@core.route('/api/V1.0/insertpermission', methods = ['GET', 'POST'])
def insertpermission():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user'], status = True).first()
        if access.verify_token(apidata['token']):                                              
                if access.verify_access('insert', 4):  
                        if 'userid' in apidata and 'startdate' in apidata and 'enddate' in apidata and 'shortdesc' in apidata and 'description' in apidata and 'id' in apidata :
                                startdate = datetime.strptime(apidata['startdate'],'%Y-%m-%d')
                                enddate = datetime.strptime(apidata['startdate'],'%Y-%m-%d')
                                if apidata['id'] is '':
                                        checkperm = hr_general_perm()._data(apidata['userid'], startdate, enddate)
                                        if 'id' not in checkperm:                        
                                                response['id'] = hr_general_perm()._insert(apidata['userid'], apidata['startdate'], apidata['enddate'], apidata['shortdesc'], apidata['description'],3,1)
                                        else:                                       
                                                response['message'] = 'Data Sudah Ada'
                                                response['status'] = '400'
                                else:
                                        hr_general_perm()._update(apidata['id'],apidata['userid'], apidata['startdate'], apidata['enddate'], apidata['shortdesc'], apidata['description'],3,1)
                        else:
                                response['message'] = 'Data Tidak Lengkap'
                                response['status'] = '400'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/listall', methods = ['GET', 'POST'])
def listall():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        if session['client'] is True:
                tempid = current_user.id
        else:                
                tempid = current_user.client_id
        access = Access.query.filter_by(id = apidata['cur_user'], status = True).first()
        if access.verify_token(apidata['token']):
                if 'keyword' not in apidata:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'
                elif apidata['keyword'] == 'province':            
                        response = province()._list()
                        response['status'] = '200'
                elif apidata['keyword'] == 'listcity': 
                        response = city()._listall()
                        response['status'] = '200'            
                elif apidata['keyword'] == 'listkecamatan': 
                        response = kecamatan()._listall()
                        response['status'] = '200'                
                elif apidata['keyword'] == 'listkelurahan': 
                        response = kelurahan()._listall()
                        response['status'] = '200'                
                elif apidata['keyword'] == 'listpostalcode': 
                        response = postal_code()._listall()
                        response['status'] = '200'
                elif apidata['keyword'] == 'city':    
                        response = city()._list(apidata['province_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'kecamatan':    
                        response = kecamatan()._list(apidata['city_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'kelurahan':    
                        response = kelurahan()._list(apidata['kecamatan_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'postalcode':    
                        response = postal_code()._list(apidata['kecamatan_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'applicantstatus':    
                        response = applicantstatus()._list()
                        response['status'] = '200'
                elif apidata['keyword'] == 'listmenu':                        
                        if access.verify_access('view', 11):  
                                response = menu()._listmenu(tempid)
                                response['status'] = '200'       
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                elif apidata['keyword'] == 'listrole':                        
                        if access.verify_access('view', 11):  
                                response = list_role()._list(tempid)
                                response['status'] = '200'       
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                elif apidata['keyword'] == 'client':                        
                        if access.verify_access('view', 5):  
                                response['client'] = clients()._list()
                                response['province'] = province()._list()   
                                response['status'] = '200'       
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                elif apidata['keyword'] == 'rolepermission': 
                        response['submenu'] = sub_menu()._listforpermission()
                        response['rolepermission'] = role_permission()._listbyrole(apidata['listroleid'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'division':
                        response['division'] = division()._list()
                        response['status'] = '200'
                elif apidata['keyword'] == 'branch':    
                        response['branch'] = branch()._list()
                        response['province'] = province()._list()
                        response['status'] = '200'
                else:
                        response['status'] = '400'
                        response['message'] = 'Kata kunci tidak ditemukan'            
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/listalluser', methods = ['GET', 'POST'])
def listalluser():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        user = User.query.filter_by(id = apidata['cur_user'], status = True).first()
        if user.verify_token(apidata['token']):
                if 'keyword' not in apidata:
                        response['message'] = 'Data Tidak Lengkap'
                        response['status'] = '400'
                elif apidata['keyword'] == 'province':            
                        response = province()._list()
                        response['status'] = '200'
                elif apidata['keyword'] == 'listcity': 
                        response = city()._listall()
                        response['status'] = '200'            
                elif apidata['keyword'] == 'listkecamatan': 
                        response = kecamatan()._listall()
                        response['status'] = '200'                
                elif apidata['keyword'] == 'listkelurahan': 
                        response = kelurahan()._listall()
                        response['status'] = '200'                
                elif apidata['keyword'] == 'listpostalcode': 
                        response = postal_code()._listall()
                        response['status'] = '200'
                elif apidata['keyword'] == 'city':    
                        response = city()._list(apidata['province_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'kecamatan':    
                        response = kecamatan()._list(apidata['city_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'kelurahan':    
                        response = kelurahan()._list(apidata['kecamatan_id'])
                        response['status'] = '200'
                elif apidata['keyword'] == 'postalcode':    
                        response = postal_code()._list(apidata['kecamatan_id'])
                        response['status'] = '200'
                else:
                        response['status'] = '400'
                        response['message'] = 'Kata kunci tidak ditemukan'            
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertlistrole', methods = ['GET', 'POST'])
def insertlistrole():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                if session['client'] is True:
                        tempid = current_user.id
                else:                
                        tempid = current_user.client_id
                listroleid = list_role.query.filter_by(id = apidata['id'], status = True).first() 
                if listroleid is None:
                        if access.verify_access('insert', 11):
                                list_role()._insert(apidata['name'],tempid)
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else :
                        if access.verify_access('update', 11):
                                list_role()._update(apidata['id'],apidata['name'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertrolepermission', methods = ['GET','POST'])
def insertrolepermission():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id = apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                try:
                        apidata['listroleid']
                        apidata['submenuid']
                        int(apidata['insert'])
                        int(apidata['update'])
                        int(apidata['remove'])
                        int(apidata['view'])    
                except:
                        response['message'] = 'Data yang dibutuhkan tidak Lengkap / format salah'
                        response['status'] = '400'
                else:
                        rolepermissionid = role_permission.query.filter_by(list_role_id = apidata['listroleid'], status = True, sub_menu_id = apidata['submenuid']).first() 
                        if rolepermissionid is None:
                                if access.verify_access('insert', 11):
                                        role_permission()._insert(apidata['listroleid'], apidata['submenuid'], int(apidata['insert']), int(apidata['update']), int(apidata['remove']), int(apidata['view']))
                                        response['status'] = '200'
                                else:
                                        response['message'] = 'Akses Ditolak!'
                                        response['status'] = '400'
                        else :
                                if access.verify_access('update', 11):
                                        role_permission()._update(rolepermissionid.id, apidata['listroleid'], apidata['submenuid'], int(apidata['insert']), int(apidata['update']), int(apidata['remove']), int(apidata['view']))
                                        response['status'] = '200'
                                else:
                                        response['message'] = 'Akses Ditolak!'
                                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/removelistrole', methods = ['GET', 'POST'])
def removelistrole():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user'],status=True).first()
        if access.verify_token(apidata['token']):
                check = list_role()._data(apidata['id'])
                if 'id' in check:
                        list_role()._remove(apidata['id'])
                        response['status'] = '200'
                else :
                        response['message'] = 'Role tidak ada'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/clientdetail', methods=['GET','POST'])     
def clientdetail():
    if request.method == 'POST':
        response = {}
        response['dataform'] = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = clients.query.filter_by(id=apidata['client_id']).first()
                if check is not None:                
                        if access.verify_access('view', 6):
                                response['client'] = clients()._data(apidata['client_id'])
                                response['dataform']['province'] = province()._list()
                                if 'id' in response['client']['province_id']:
                                        response['dataform']['city'] = city()._list(response['client']['province_id']['id'])
                                
                                if 'id' in response['client']['city_id']:
                                        response['dataform']['kecamatan'] = kecamatan()._list(response['client']['city_id']['id'])
                                
                                if 'id' in response['client']['kecamatan_id']:
                                        response['dataform']['kelurahan'] = kelurahan()._list(response['client']['kecamatan_id']['id'])
                                
                                if 'id' in response['client']['kelurahan_id']:
                                        response['dataform']['postal_code'] = postal_code()._list(response['client']['kelurahan_id']['id'])                           
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        response['message'] = 'Klien Tidak Terdaftar'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)
        
@core.route('/api/V1.0/insertclient', methods=['GET','POST'])
def addclient():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = clients.query.filter_by(id = apidata['client_id']).first()
                if check is None:
                        if access.verify_access('insert', 6):
                                clients()._insert(apidata['name'], apidata['phonenumber'], 'cpipassword!', '123456', apidata['email'], apidata['address'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'],apidata['rt'], apidata['rw'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        if access.verify_access('update', 6):
                                clients()._update(apidata['client_id'],apidata['name'], apidata['phonenumber'], apidata['email'], apidata['address'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'],apidata['rt'], apidata['rw'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                response['status'] = '200' 
        return jsonify(response)

@core.route('/api/V1.0/removeclient', methods=['GET','POST'])
def removeclient():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Access.query.filter_by(client_id = apidata['id'], status = True).first()
                if check is None:                        
                        if access.verify_access('remove', 6):
                                clients()._remove(apidata['id'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        response['message'] = 'Data Klien Tidak Bisa Dihapus. Masih ada data karyawan aktif di perusahaan ini.'
                        response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/insertdivision', methods=['GET','POST'])
def adddivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = division.query.filter_by(id=apidata['id']).first()
                if check is None:
                        if access.verify_access('insert', 7):
                                division()._insert(apidata['name'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else :
                        if access.verify_access('update', 7):
                                division()._update(apidata['id'],apidata['name'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/removedivision', methods=['GET','POST'])
def removedivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):                
                if access.verify_access('remove', 7):
                        division()._remove(apidata['id'])
                        response['status'] = '200'
                else:
                        response['message'] = 'Akses Ditolak!'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/branchdetail', methods=['GET','POST'])     
def branchdetail():
    if request.method == 'POST':
        response = {}
        response['dataform'] = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = branch.query.filter_by(id=apidata['branch_id']).first()
                if check is not None:                
                        if access.verify_access('view', 6):
                                response['branch'] = branch()._data(apidata['branch_id'])
                                response['dataform']['province'] = province()._list()
                                if 'id' in response['branch']['province_id']:
                                        response['dataform']['city'] = city()._list(response['branch']['province_id']['id'])
                                
                                if 'id' in response['branch']['city_id']:
                                        response['dataform']['kecamatan'] = kecamatan()._list(response['branch']['city_id']['id'])
                                
                                if 'id' in response['branch']['kecamatan_id']:
                                        response['dataform']['kelurahan'] = kelurahan()._list(response['branch']['kecamatan_id']['id'])
                                
                                if 'id' in response['branch']['kelurahan_id']:
                                        response['dataform']['postal_code'] = postal_code()._list(response['branch']['kelurahan_id']['id'])                           
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        response['message'] = 'User Tidak Terdaftar'
                        response['status'] = '400'
        else:
                response['message'] = 'User Tidak Terverifikasi'
                response['status'] = '400'
        return jsonify(response)
        
@core.route('/api/V1.0/insertbranch', methods=['GET','POST'])
def addbranch():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = branch.query.filter_by(id = apidata['branch_id']).first()
                if check is None:
                        if access.verify_access('insert', 6):
                                branch()._insert(apidata['name'], apidata['phonenumber'], apidata['email'], apidata['address'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'],apidata['rt'], apidata['rw'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        if access.verify_access('update', 6):
                                branch()._update(apidata['branch_id'], apidata['name'], apidata['phonenumber'], apidata['email'], apidata['address'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                response['status'] = '200' 
        return jsonify(response)

@core.route('/api/V1.0/removebranch', methods=['GET','POST'])
def removebranch():
    if request.method == 'POST':
        response = {}
        response['status'] = '400'
        apidata = request.form
        access = Access.query.filter_by(id=apidata['cur_user']).first()
        if access.verify_token(apidata['token']):
                check = Access.query.filter_by(branch_id = apidata['id'], status = True).first()
                if check is None:                        
                        if access.verify_access('remove', 6):
                                branch()._remove(apidata['id'])
                                response['status'] = '200'
                        else:
                                response['message'] = 'Akses Ditolak!'
                                response['status'] = '400'
                else:
                        response['message'] = 'User Tidak Terverifikasi'
                        response['status'] = '400'
        return jsonify(response)

@core.route('/api/V1.0/joblisting', methods = ['GET', 'POST'])
def joblisting():
    response = {}
    response['joblisting'] = Jobvacancy()._joblisting()
    response['jobtype'] = jobtype()._list()
    response['branch'] = branch()._list()
    response['experience'] = experience()._list()
    response['status'] = '200'
    return jsonify(response)

@core.route('/api/V1.0/jobdetail', methods = ['GET', 'POST'])
def jobdetail():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        response['jobvacancy'] = Jobvacancy()._jobvacancydetail(apidata['jobvacancy_id'])
        response['status'] = '200'
        return jsonify(response)