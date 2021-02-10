from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from flask_login import UserMixin, current_user
from app import db,login_manager
from . import mongo
import pymongo, requests
from .utils import *
from flask import jsonify, session
from calendar import monthrange
import pandas as pd
from datetime import timedelta

@login_manager.user_loader
def load_access(user_id):
    if 'client' in session:
        if session['client'] is True:
            return clients.query.get(user_id)
        else:
            return Access.query.get(user_id)
    else:
        return Access.query.get(user_id)

class Access(db.Model,UserMixin):
    __tablename__ = 'access'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    nik = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    pin_hash = db.Column(db.String(128))
    email = db.Column(db.String(100),index=True)    
    phone_number = db.Column(db.String(50),index=True)
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _name, _nik, _password, _pin, _phonenumber, _email, _clientid):
        insert = Access()
        insert.name = _name
        insert.nik = _nik
        insert.password_hash = generate_password_hash(_password)
        insert.pin_hash = generate_password_hash(_pin)       
        insert.phone_number = _phonenumber        
        insert.email = _email 
        insert.client_id = _clientid
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()
        return insert

    def _updatepassword(self, _id, _password):
        update = Access()
        update = Access.query.filter_by(id = _id).first()
        update.password_hash = generate_password_hash(_password)
        db.session.add(update)
        db.session.commit()

    def _update(self, _id, _name, _nik, _phonenumber, _email, _clientid):
        update = Access()
        update = Access.query.filter_by(id = _id).first()
        update.name = _name
        update.nik = _nik
        update.phone_number = _phonenumber        
        update.email = _email
        update.client_id = _clientid
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = Access()
        update = Access.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()
        return update

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def decode(self, password):
        response = False
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.password_hash))
        if decrypt == hmac_sha256(key, msg):
            response = True
        return response

    def check_pin(self, pin):
        return check_password_hash(self.pin_hash,pin)

    def generate_token(self):
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.id) + ':' + str(self.phone_number) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        return hmac_sha256(key, msg)

    def verify_token(self, token):
        response = False
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.id) + ':' + str(self.phone_number) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        if token == hmac_sha256(key, msg):
            response = True
        return response

    def verify_access(self, _permission, _submenu):
        response = False
        _role = role.query.filter_by(user_id = self.id, status = True).first()
        if _role is not None:
            _role_permission =  role_permission.query.filter_by(list_role_id = _role.list_role_id, sub_menu_id = _submenu, status = True).first()
            if _role_permission is not None:
                response = getattr(_role_permission,_permission)
        return response

    def _data(self, _id):
        response = {}
        _access = Access.query.filter_by(id = _id, status = True).first()
        if _access is not None:
            response['id'] = _access.id
            response['name'] = _access.name
            response['nik'] = _access.nik
            response['email'] = _access.email            
            response['phone_number'] = _access.phone_number
            response['client_id'] = clients()._data(_access.client_id)
        return response

    def _list(self):
        response = {}
        response['data'] = []
        _access = Access.query.filter_by(status = True).all()
        for i in _access:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'nik' : i.nik,
                'password_hash' : i.password_hash,
                'email' : i.email,
                'phone_number' : i.phone_number
            })
        return response

    def _accountdetail(self, _id):
        response = {}
        _access = Access.query.filter_by(status = True, id = _id).first()
        if _access is not None:
            response['id'] = _access.id
            response['client_id'] = clients()._data(_access.client_id)
            response['name'] = _access.name
            response['nik'] = _access.nik
            response['phone_number'] = _access.phone_number
            response['email'] = _access.email
        return response

    def _account(self, _clientid):
        response = {}
        response['data'] = []
        _access = Access.query.filter_by(status = True, client_id = _clientid).all()
        for i in _access:
            response['data'].append({
                'id' : i.id,
                'client_id' : clients()._data(i.client_id),                
                'name' : i.name,
                'nik' : i.nik,
                'phone_number' : i.phone_number,
                'email' : i.email,
            })
        return response

    def __repr__(self):
        return "Access-name " + self.name

class Jobvacancy(db.Model,UserMixin):
    __tablename__ = 'jobvacancy'

    id = db.Column(db.Integer,primary_key=True)
    jobposition = db.Column(db.String(100))
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'))
    salary = db.Column(db.String(100))
    applicationdate = db.Column(db.DateTime)
    requirement = db.Column(db.Text)
    experience = db.Column(db.Text)
    division_id = db.Column(db.Integer,db.ForeignKey('division.id'))
    jobtype_id = db.Column(db.Integer,db.ForeignKey('jobtype.id'))
    branch_id = db.Column(db.Integer,db.ForeignKey('branch.id'))
    experience_id = db.Column(db.Integer,db.ForeignKey('experience.id'))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _jobposition, _description, _clientid, _salary, _applicationdate, _requirement, _experience, _divisionid, _jobtypeid, _branchid, _experienceid):
        insert = Jobvacancy()
        insert.jobposition = _jobposition
        insert.description = _description
        insert.client_id = _clientid
        insert.salary = _salary
        insert.applicationdate = _applicationdate
        insert.requirement = _requirement
        insert.experience = _experience
        insert.division_id = _divisionid
        insert.jobtype_id = _jobtypeid
        insert.branch_id = _branchid
        insert.experience_id = _experienceid
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()
        return insert

    def _update(self, _id, _jobposition, _description, _clientid, _salary, _applicationdate, _requirement, _experience, _divisionid, _jobtypeid, _branchid, _experienceid):
        update = Jobvacancy()
        update = Jobvacancy.query.filter_by(id = _id).first()
        update.jobposition = _jobposition
        update.description = _description
        update.client_id = _clientid
        update.salary = _salary
        update.applicationdate = _applicationdate
        update.requirement = _requirement
        update.experience = _experience
        update.division_id = _divisionid
        update.jobtype_id = _jobtypeid
        update.branch_id = _branchid
        update.experience_id = _experienceid
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = Jobvacancy()
        update = Jobvacancy.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()
        return update

    def _data(self, _id):
        response = {}
        _jobvacancy = Jobvacancy.query.filter_by(id = _id, status = True).first()
        if _jobvacancy is not None:
            response['id'] = _jobvacancy.id
            response['jobposition'] = _jobvacancy.jobposition
            response['description'] = _jobvacancy.description
            response['client_id'] = clients()._data(_jobvacancy.client_id)
            response['salary'] = _jobvacancy.salary
            response['applicationdate'] = _jobvacancy.applicationdate
            response['requirement'] = _jobvacancy.requirement
            response['experience'] = _jobvacancy.experience
            response['division_id'] = division()._data(_jobvacancy.division_id)
            response['jobtype_id'] = jobtype()._data(_jobvacancy.jobtype_id)
            response['branch_id'] = branch()._data(_jobvacancy.branch_id)
            response['experience_id'] = experience()._data(_jobvacancy.experience_id)
        return response

    def _list(self):
        response = {}
        response['data'] = []
        _jobvacancy = Jobvacancy.query.filter_by(status = True).all()
        for i in _jobvacancy:
            response['data'].append({
                'id' : i.id,
                'jobposition' : i.jobposition,
                'description' : i.description,
                'client_id' : i.client_id,
                'salary' : i.salary,
                'applicationdate' : i.applicationdate,
                'requirement' : i.requirement,
                'experience' : i.experience,
                'division_id' : i.division_id,
                'jobtype_id' : i.jobtype_id,
                'branch_id' : i.branch_id,
                'experience_id' : i.experience_id
            })
        return response

    def _jobvacancy(self, _clientid):
        response = {}
        response['data'] = []
        _jobvacancy = Jobvacancy.query.filter_by(status = True, client_id = _clientid).all()
        for i in _jobvacancy:
            response['data'].append({
                'id' : i.id,
                'jobposition' : i.jobposition,
                'description' : i.description,
                'client_id' : clients()._data(i.client_id),
                'salary' : i.salary,
                'applicationdate' : i.applicationdate,
                'requirement' : i.requirement,
                'experience' : i.experience,
                'division_id' : division()._data(i.division_id),
                'jobtype_id' : jobtype()._data(i.jobtype_id),
                'branch_id' : branch()._data(i.branch_id),
                'experience_id' : experience()._data(i.experience_id)
            })
        return response

    def _jobvacancydetail(self, _id):
        response = {}
        _jobvacancy = Jobvacancy.query.filter_by(status = True, id = _id).first()
        if _jobvacancy is not None:
            response['id'] = _jobvacancy.id
            response['client_id'] = clients()._data(_jobvacancy.client_id)
            response['jobposition'] = _jobvacancy.jobposition
            response['description'] = _jobvacancy.description
            response['salary'] = _jobvacancy.salary
            response['applicationdate'] = ifnull(_jobvacancy.applicationdate)
            response['requirement'] = _jobvacancy.requirement
            response['experience'] = _jobvacancy.experience
            response['division_id'] = division()._data(_jobvacancy.division_id)
            response['jobtype_id'] = jobtype()._data(_jobvacancy.jobtype_id)
            response['branch_id'] = branch()._data(_jobvacancy.branch_id)
            response['experience_id'] = experience()._data(_jobvacancy.experience_id)
            response['datetime'] = _jobvacancy.add_time
        return response

    def _joblisting(self):
        response = {}
        response['data'] = []
        _jobvacancy = Jobvacancy.query.filter_by(status = True).all()
        for i in _jobvacancy:
            response['data'].append({
                'id' : i.id,
                'jobposition' : i.jobposition,
                'description' : i.description,
                'client_id' : clients()._data(i.client_id),
                'salary' : i.salary,
                'applicationdate' : i.applicationdate,
                'requirement' : i.requirement,
                'experience' : i.experience,
                'division_id' : division()._data(i.division_id),
                'jobtype_id' : jobtype()._data(i.jobtype_id),
                'branch_id' : branch()._data(i.branch_id),
                'experience_id' : experience()._data(i.experience_id)
            })
        return response

    def _jobdetail(self):
        response = {}
        _jobvacancy = Jobvacancy.query.filter_by(status = True).first()
        if _jobvacancy is not None:
            response['id'] = _jobvacancy.id
            response['client_id'] = clients()._data(_jobvacancy.client_id)
            response['jobposition'] = _jobvacancy.jobposition
            response['description'] = _jobvacancy.description
            response['salary'] = _jobvacancy.salary
            response['applicationdate'] = ifnull(_jobvacancy.applicationdate)
            response['requirement'] = _jobvacancy.requirement
            response['experience'] = _jobvacancy.experience
            response['division_id'] = division()._data(_jobvacancy.division_id)
            response['jobtype_id'] = jobtype()._data(_jobvacancy.jobtype_id)
            response['branch_id'] = branch()._data(_jobvacancy.branch_id)
            response['experience_id'] = experience()._data(_jobvacancy.experience_id)
        return response

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    nik = db.Column(db.String(30))
    phone_number = db.Column(db.String(50),index=True)
    password_hash = db.Column(db.String(128))
    pin_hash = db.Column(db.String(128))
    email = db.Column(db.String(100),index=True)
    birthdate = db.Column(db.DateTime)
    birthplace = db.Column(db.String(30))
    address = db.Column(db.Text)
    gender = db.Column(db.String(15))
    religion = db.Column(db.String(15))
    marital = db.Column(db.String(10))
    province_id = db.Column(db.Integer,db.ForeignKey('province.id'))
    city_id = db.Column(db.Integer,db.ForeignKey('city.id'))
    kecamatan_id = db.Column(db.Integer,db.ForeignKey('kecamatan.id'))
    kelurahan_id = db.Column(db.String(20),db.ForeignKey('kelurahan.id'))
    postal_code_id = db.Column(db.Integer,db.ForeignKey('postal_code.id'))
    rt = db.Column(db.String(4))
    rw = db.Column(db.String(4))
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'))
    applicantstatus_id = db.Column(db.Integer,db.ForeignKey('applicantstatus.id'))
    jobposition_id = db.Column(db.Integer,db.ForeignKey('jobvacancy.id'))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _name, _nik, _phonenumber, _password, _pin, _email, _birthdate, _birthplace, _address, _gender, _religion, _marital, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw, _clientid, _applicantstatusid, _jobpositionid):
        insert = User()
        insert.name = _name
        insert.nik = _nik
        insert.phone_number = _phonenumber
        insert.password_hash = generate_password_hash(_password)
        insert.pin_hash = generate_password_hash(_pin)
        insert.email = _email
        insert.birthdate = _birthdate
        insert.birthplace = _birthplace
        insert.address = _address
        insert.gender = _gender
        insert.religion = _religion
        insert.marital = _marital
        insert.province_id = _province
        insert.city_id = _city
        insert.kecamatan_id = _kecamatan
        insert.kelurahan_id = _kelurahan
        insert.postal_code_id = _postalcode
        insert.rt = _rt
        insert.rw = _rw
        insert.client_id = _clientid
        insert.applicantstatus_id = _applicantstatusid
        insert.jobposition_id = _jobpositionid
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()
        return insert

    def _register(self, _name, _phonenumber, _password, _email, _gender, _religion, _clientid):
        insert = User()
        insert.name = _name
        insert.phone_number = _phonenumber
        insert.password_hash = generate_password_hash(_password)
        insert.email = _email
        insert.gender = _gender
        insert.religion = _religion
        insert.client_id = _clientid
        db.session.add(insert)
        db.session.commit()
        return insert

    def _updatepassword(self, _id, _password):
        update = User()
        update = User.query.filter_by(id = _id).first()
        update.password_hash = generate_password_hash(_password)
        db.session.add(update)
        db.session.commit()

    def _update(self, _id, _name, _nik, _phonenumber, _email, _birthdate, _birthplace, _address, _gender, _religion, _marital, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw, _clientid, _applicantstatusid, _jobpositionid):
        update = User()
        update = User.query.filter_by(id = _id).first()
        update.name = _name
        update.nik = _nik
        update.phone_number = _phonenumber
        update.email = _email
        update.birthdate = _birthdate
        update.birthplace = _birthplace
        update.address = _address
        update.gender = _gender
        update.religion = _religion
        update.marital = _marital
        update.province_id = _province
        update.city_id = _city
        update.kecamatan_id = _kecamatan
        update.kelurahan_id = _kelurahan
        update.postal_code_id = _postalcode
        update.rt = _rt
        update.rw = _rw
        update.client_id = _clientid
        update.applicantstatus_id = _applicantstatusid
        update.jobposition_id = _jobpositionid
        db.session.add(update)
        db.session.commit()

    def _updateuser(self, _id, _name, _nik, _phonenumber, _email, _birthdate, _birthplace, _address, _gender, _religion, _marital, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw, _clientid):
        update = User()
        update = User.query.filter_by(id = _id).first()
        update.name = _name
        update.nik = _nik
        update.phone_number = _phonenumber
        update.email = _email
        update.birthdate = _birthdate
        update.birthplace = _birthplace
        update.address = _address
        update.gender = _gender
        update.religion = _religion
        update.marital = _marital
        update.province_id = _province
        update.city_id = _city
        update.kecamatan_id = _kecamatan
        update.kelurahan_id = _kelurahan
        update.postal_code_id = _postalcode
        update.rt = _rt
        update.rw = _rw
        update.client_id = _clientid
        db.session.add(update)
        db.session.commit()

    def _applyjob(self, _id, _applicantstatusid, _jobpositionid):
        update = User()
        update = User.query.filter_by(id = _id).first()
        update.applicantstatus_id = _applicantstatusid
        update.jobposition_id = _jobpositionid
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = User()
        update = User.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()
        return update

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def check_pin(self, pin):
        return check_password_hash(self.pin_hash,pin)

    def generate_token(self):
        key = str.encode(self.password_hash)
        msg = str.encode(str(self.id) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        return hmac_sha256(key, msg)

    def verify_token(self, token):
        response = False
        key = str.encode(self.password_hash)
        msg = str.encode(str(self.id) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        if token == hmac_sha256(key, msg):
            response = True
        return response

    def verify_access(self, _permission, _submenu):
        response = False
        _role = role.query.filter_by(user_id = self.id, status = True).first()
        if _role is not None:
            _role_permission =  role_permission.query.filter_by(list_role_id = _role.list_role_id, sub_menu_id = _submenu, status = True).first()
            if _role_permission is not None:
                response = getattr(_role_permission,_permission)
        return response

    def _data(self, _id):
        response = {}
        _user = User.query.filter_by(id = _id, status = True).first()
        if _user is not None:
            response['id'] = _user.id
            response['name'] = _user.name
            response['nik'] = _user.nik
            response['phone_number'] = _user.phone_number
            response['email'] = _user.email
            response['address'] = _user.address
            response['gender'] = _user.gender
            response['religion'] = _user.religion
            response['history_education'] = history_education()._data(_user.id)
            response['job_experience'] = job_experience()._data(_user.id)
            response['client_id'] = clients()._data(_user.client_id)
            response['applicantstatus_id'] = applicantstatus()._data(_user.applicantstatus_id)
            response['jobposition_id'] = Jobvacancy()._data(_user.jobposition_id)
        return response

    def _list(self):
        response = {}
        response['data'] = []
        _user = User.query.filter_by(status = True).all()
        for i in _user:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'nik' : i.nik,
                'gender' : i.gender,
                'religion' : i.religion,
                'address' : i.address,
                'province_id' : i.province_id,
                'city_id' : i.city_id,
                'kecamatan_id' : i.kecamatan_id,
                'kelurahan_id' : i.kelurahan_id,
                'postal_code_id' : i.postal_code_id,
                'rt' : i.rt,
                'rw' : i.rw,
                'birthdate' : i.birthdate,
                'birthplace' : i.birthplace,
                'phone_number' : i.phone_number,
                'email' : i.email,
                'marital' : i.marital,
                'client_id' : i.client_id,
                'applicantstatus_id' : i.applicantstatus_id,
                'jobposition_id' : i.jobposition_id
            })
        return response

    def _employee(self, _clientid):
        response = {}
        response['data'] = []
        _user = User.query.filter_by(status = True, client_id = _clientid).all()
        for i in _user:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'client_id' : clients()._data(i.client_id),
                'applicantstatus_id' : applicantstatus()._data(i.applicantstatus_id),
                'jobposition_id' : Jobvacancy()._data(i.jobposition_id),
                'province' : province()._data(i.province_id)
            })
        return response

    def _employeedetail(self, _id):
        response = {}
        _user = User.query.filter_by(status = True, id = _id).first()
        if _user is not None:
            response['id'] = _user.id
            response['client_id'] = clients()._data(_user.client_id)
            response['applicantstatus_id'] = applicantstatus()._data(_user.applicantstatus_id)
            response['jobposition'] = Jobvacancy()._data(_user.jobposition_id)
            response['name'] = _user.name
            response['nik'] = _user.nik
            response['phone_number'] = _user.phone_number
            response['email'] = _user.email
            response['religion'] = _user.religion
            response['gender'] = _user.gender
            response['address'] = _user.address
            response['province_id'] = province()._data(_user.province_id)
            response['city_id'] = city()._data(_user.city_id)
            response['kecamatan_id'] = kecamatan()._data(_user.kecamatan_id)
            response['kelurahan_id'] = kelurahan()._data(_user.kelurahan_id)
            response['postal_code_id'] = postal_code()._data(_user.postal_code_id)
            response['rt'] = _user.rt
            response['rw'] = _user.rw
            response['birthdate'] = ifnull(_user.birthdate)
            response['birthplace'] = _user.birthplace
            response['profile_picture'] = Image_Service()._dataimage(_user.id,2)
            response['fotoktp'] = Image_Service()._dataimage(_user.id,4)
            response['fotonpwp'] = Image_Service()._dataimage(_user.id,5)
            response['cv'] = Image_Service()._dataimage(_user.id,3)
            response['marital'] = _user.marital
            response['cor-address'] = corespondend_address()._data(_user.id)
            response['role'] = role()._databyuserid(_user.id)
            response['history_education'] = history_education()._data(_user.id)
            response['job_experience'] = job_experience()._data(_user.id)
        return response

    def _userclient(self, _userid,_clientid):
        response = {}
        _user = User.query.filter_by(id = _userid, client_id = _clientid, status = True).first()
        if _user is not None:
            response['id'] = _user.id
            response['name'] = _user.name
            response['phone_number'] = _user.phone_number
            response['email'] = _user.email
            response['birthdate'] = _user.birthdate
            response['birthplace'] = _user.birthplace
            response['address'] = _user.address
            response['gender'] = _user.gender
            response['province_id'] = province()._data(_user.province_id)
            response['city_id'] = city()._data(_user.city_id)
            response['kecamatan_id'] = _user.kecamatan_id
            response['kelurahan_id'] = _user.kelurahan_id
            response['postal_code_id'] = _user.postal_code_id
            response['rt'] = _user.rt
            response['rw'] = _user.rw
            response['client_id'] = clients()._data(_user.client_id)
            response['applicantstatus_id'] = applicantstatus()._data(_user.applicantstatus_id)
        return response

    def _jobseeker(self):
        return User.query.filter_by(status = True).count()

    def _shortlisted(self):
        return User.query.filter_by(applicantstatus_id = '1', status = True).count()

    def _sukses(self):
        return User.query.filter_by(applicantstatus_id = '2', status = True).count()

    def _gagal(self):
        return User.query.filter_by(applicantstatus_id = '3', status = True).count()

    def __repr__(self):
        return "Username " + self.name

class corespondend_address(db.Model,UserMixin):
    __tablename__ = 'corespondend_address'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    address = db.Column(db.Text)
    province_id = db.Column(db.Integer,db.ForeignKey('province.id'))
    city_id = db.Column(db.Integer,db.ForeignKey('city.id'))
    kecamatan_id = db.Column(db.Integer,db.ForeignKey('kecamatan.id'))
    kelurahan_id = db.Column(db.String(20),db.ForeignKey('kelurahan.id'))
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.id'))
    status_address_id = db.Column(db.Integer, db.ForeignKey('list_status_address.id'))
    rt = db.Column(db.String(4))
    rw = db.Column(db.String(4))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _address, _province, _city, _kecamatan, _kelurahan,  _postalcode, _rt, _rw, _userid, _statusaddress):
        insert = corespondend_address()
        insert.user_id = _userid
        insert.address = _address
        insert.province_id = _province
        insert.city_id = _city
        insert.kecamatan_id = _kecamatan
        insert.kelurahan_id = _kelurahan
        insert.postal_code_id = _postalcode
        insert.status_address_id = _statusaddress
        insert.rt = _rt
        insert.rw = _rw
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()


    def _update(self, _id, _address, _province, _city, _kecamatan, _kelurahan,  _postalcode, _rt, _rw, _statusaddress):
        update = corespondend_address()
        update = corespondend_address.query.filter_by(id=_id).first()
        update.address = _address
        update.province_id = _province
        update.city_id = _city
        update.kecamatan_id = _kecamatan
        update.kelurahan_id = _kelurahan
        update.postal_code_id = _postalcode
        update.status_address_id = _statusaddress
        update.rt = _rt
        update.rw = _rw
        db.session.add(update)
        db.session.commit()

    def _data(self,_userid):
        response = {}
        _korespon = corespondend_address.query.filter_by(user_id = _userid, status = True).first()
        if _korespon is not None:
            response['id'] =  _korespon.id
            response['user_id'] =  _korespon.user_id
            response['address'] =  _korespon.address
            response['province_id'] = province()._data(_korespon.province_id)
            response['city_id'] = city()._data(_korespon.city_id)
            response['kecamatan_id'] = kecamatan()._data(_korespon.kecamatan_id)
            response['kelurahan_id'] = kelurahan()._data(_korespon.kelurahan_id)
            response['postal_code_id'] = postal_code()._data(_korespon.postal_code_id)
            response['status_address_id'] = list_status_address()._data(_korespon.status_address_id)
            response['rt'] = _korespon.rt
            response['rw'] = _korespon.rw
        return response

class province(db.Model,UserMixin):
    __tablename__ = 'province'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name):
        insert = province()
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name):
        update = province()
        update = province.query.filter_by(id = _id).first()
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = province()
        update = province.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self):
        response = {}
        response['data'] = []
        _province = province.query.filter_by(status = True).order_by(province.name.asc()).all()
        for i in _province:
            response['data'].append({
                'id' : i.id ,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _province = province.query.filter_by(id = _id, status = True).first()
        if _province is not None:
            response['id'] = _province.id
            response['name'] = _province.name
        return response

class city(db.Model,UserMixin):
    __tablename__ = 'city'

    id = db.Column(db.Integer,primary_key=True)
    province_id = db.Column(db.Integer,db.ForeignKey('province.id'))
    name = db.Column(db.String(50))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name, _province):
        insert = city()
        insert.province_id = _province
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name, _province):
        update = city()
        update = city.query.filter_by(id = _id).first()
        update.province_id = _province
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = city()
        update = city.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self, _id):
        response = {}
        response['data'] = []
        _city = city.query.filter_by(province_id = _id).filter_by(status = True).order_by(city.name.asc()).all()
        for i in _city:
            response['data'].append({
                'id' : i.id,
                'province_id' : i.province_id,
                'name' : i.name
            })
        return response

    def _listall(self):
        response = {}
        response['data'] = []
        _city = city.query.filter_by(status = True).all()
        for i in _city:
            response['data'].append({
                'id' : i.id,
                'province_id' : i.province_id,
                'name' : i.name
            })
        return response

    def _data(self,_id):
        response = {}
        _city = city.query.filter_by(id = _id).filter_by(status = True).first()
        if _city is not None:
            response['id'] = _city.id
            response['province_id'] = _city.province_id
            response['name'] = _city.name
        return response

class kecamatan(db.Model,UserMixin):
    __tablename__ = 'kecamatan'

    id = db.Column(db.Integer,primary_key=True)
    city_id = db.Column(db.Integer,db.ForeignKey('city.id'))
    name = db.Column(db.String(50))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name, _city):
        insert = kecamatan()
        insert.city_id = _city
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name, _idcity):
        update = kecamatan()
        update = kecamatan.query.filter_by(id = _id).first()
        update.city_id = _idcity
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = kecamatan()
        update = kecamatan.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self,_id):
        response = {}
        response['data'] = []
        _kecamatan = kecamatan.query.filter_by(city_id = _id).filter_by(status = True).order_by(kecamatan.name.asc()).all()
        for i in _kecamatan:
            response['data'].append({
                'id' : i.id,
                'city_id' : i.city_id,
                'name' : i.name
            })
        return response

    def _listall(self):
        response = {}
        response['data'] = []
        _kecamatan = kecamatan.query.filter_by(status = True).all()
        for i in _kecamatan:
            response['data'].append({
                'id' : i.id,
                'city_id' : i.city_id,
                'name' : i.name
            })
        return response
    def _data(self, _id):
        response = {}
        _kecamatan = kecamatan.query.filter_by(id = _id).filter_by(status = True).first()
        if _kecamatan is not None:
            response['id'] = _kecamatan.id
            response['city_id'] = _kecamatan.city_id
            response['name'] = _kecamatan.name
        return response

class kelurahan(db.Model,UserMixin):
    __tablename__ = 'kelurahan'

    id = db.Column(db.String(20),primary_key=True)
    kecamatan_id = db.Column(db.Integer,db.ForeignKey('kecamatan.id'))
    name = db.Column(db.String(50))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name, _kecamatan):
        insert = kelurahan()
        insert.kecamatan_id = _kecamatan
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name, _kecamatan):
        update = kelurahan()
        update = kelurahan.query.filter_by(id = _id).first()
        update.name = _name
        update.kecamatan_id = _kecamatan
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = kelurahan()
        update = kelurahan.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self,_id):
        response = {}
        response['data'] = []
        _kelurahan = kelurahan.query.filter_by(kecamatan_id = _id).filter_by(status = True).order_by(kelurahan.name.asc()).all()
        for i in _kelurahan:
            response['data'].append({
                'id' : i.id,
                'kecamatan_id' : i.kecamatan_id,
                'name' : i.name
            })
        return response

    def _listall(self):
        response = {}
        response['data'] = []
        _kelurahan = kelurahan.query.filter_by(status = True).all()
        for i in _kelurahan:
            response['data'].append({
                'id' : i.id,
                'kecamatan_id' : i.kecamatan_id,
                'name' : i.name
            })
        return response

    def _data(self,_id):
        response = {}
        _kelurahan = kelurahan.query.filter_by(id = _id).filter_by(status = True).first()
        if _kelurahan is not None:
            response['id'] = _kelurahan.id
            response['kecamatan_id'] = _kelurahan.kecamatan_id
            response['name'] = _kelurahan.name
        return response

class postal_code(db.Model,UserMixin):
    __tablename__ = 'postal_code'

    id = db.Column(db.String(5),primary_key=True)
    kelurahan_id = db.Column(db.String(20),db.ForeignKey('kelurahan.id'))
    name = db.Column(db.String(6))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name, _kelurahan):
        insert = postal_code()
        insert.kelurahan_id = _kelurahan
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name, _kelurahan):
        update = postal_code()
        update = postal_code.query.filter_by(id = _id).filter_by(status = True).first()
        upadte.kelurahan_id = _kelurahan
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = postal_code()
        update = postal_code.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self,_kelurahan):
        response = {}
        response['data'] = []
        _postalcode = postal_code.query.filter_by(status = True, kelurahan_id = _kelurahan).all()
        for i in _postalcode:
            response['data'].append({
                'id' : i.id,
                'kelurahan_id' : i.kelurahan_id,
                'name' : i.name
            })
        return response

    def _listall(self):
        response = {}
        response['data'] = []
        _postalcode = postal_code.query.filter_by(status = True).all()
        for i in _postalcode:
            response['data'].append({
                'id' : i.id,
                'kelurahan_id' : i.kelurahan_id,
                'name' : i.name
            })
        return response

    def _data(self,_id):
        response = {}
        _postalcode = postal_code.query.filter_by(id = _id).filter_by(status = True).first()
        if _postalcode is not None:
            response['id'] = _postalcode.id
            response['kelurahan_id'] = _postalcode.kelurahan_id
            response['name'] = _postalcode.name
        return response

class clients(db.Model, UserMixin):
    __tablename__ = 'clients'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(50),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    pin_hash = db.Column(db.String(128))
    email = db.Column(db.String(100),unique=True,index=True)
    address = db.Column(db.Text)
    province_id = db.Column(db.Integer,db.ForeignKey('province.id'))
    city_id = db.Column(db.Integer,db.ForeignKey('city.id'))
    kecamatan_id = db.Column(db.Integer,db.ForeignKey('kecamatan.id'))
    kelurahan_id = db.Column(db.String(20),db.ForeignKey('kelurahan.id'))
    postal_code_id = db.Column(db.Integer,db.ForeignKey('postal_code.id'))
    rt = db.Column(db.String(4))
    rw = db.Column(db.String(4))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _name, _phonenumber, _password, _pin, _email, _address, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw):
        insert = clients()
        insert.name = _name
        insert.phone_number = _phonenumber
        insert.password_hash = generate_password_hash(_password)
        insert.pin_hash = generate_password_hash(_pin)
        insert.email = _email
        insert.address = _address
        insert.province_id = _province
        insert.city_id = _city
        insert.kecamatan_id = _kecamatan
        insert.kelurahan_id = _kelurahan
        insert.postal_code_id = _postalcode
        insert.rt = _rt
        insert.rw = _rw
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _updatepassword(self, _id, _password):
        update = clients()
        update = clients.query.filter_by(id = _id).first()
        update.password_hash = generate_password_hash(_password)
        db.session.add(update)
        db.session.commit()

    def _update(self, _id, _name, _phonenumber, _email, _address, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw):
        update = clients()
        update = clients.query.filter_by(id = _id).first()
        update.name = _name
        update.phone_number = _phonenumber
        update.email = _email
        update.address = _address
        update.province_id = _province
        update.city_id = _city
        update.kecamatan_id = _kecamatan
        update.kelurahan_id = _kelurahan
        update.postal_code_id = _postalcode
        update.rt = _rt
        update.rw = _rw
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = clients()
        update = clients.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def check_pin(self,pin):
        return check_password_hash(self.pin_hash,pin)

    def generate_token(self):
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.id) + ':' + str(self.phone_number) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        return hmac_sha256(key, msg)

    def verify_token(self, token):
        response = False
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.id) + ':'+ str(self.phone_number) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        if token == hmac_sha256(key, msg):
            response = True
        return response

    def _data(self,_id):
        response = {}
        i = clients.query.filter_by(id = _id, status = True).first()
        if i is not None:
            response['id'] = i.id
            response['name'] = i.name
            response['phone_number'] = i.phone_number
            response['email'] = i.email
            response['address'] = i.address
            response['province_id'] = province()._data(i.province_id)
            response['city_id'] = city()._data(i.city_id)
            response['kecamatan_id'] = kecamatan()._data(i.kecamatan_id)
            response['kelurahan_id'] = kelurahan()._data(i.kelurahan_id)
            response['postal_code_id'] = postal_code()._data(i.postal_code_id)
            response['rt'] = i.rt
            response['rw'] = i.rw
        return response

    def _list(self):
        response = {}
        response['data'] = []
        _user = clients.query.filter_by(status = True).all()
        for i in _user:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'phone_number' : i.phone_number,
                'email' : i.email,
                'address' : i.address
            })
        return response

class contract_client(db.Model, UserMixin):
    __tablename__ = 'contract_client'

    id = db.Column(db.Integer,primary_key=True)
    client_id = db.Column(db.Integer,db.ForeignKey('clients.id'))
    position_id = db.Column(db.Integer,db.ForeignKey('position.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _clientid, _jobtipeid, _startime, _endtime):
        insert = contract_client()
        insert.client_id = _clientid
        insert.position_id = _jobtipeid
        insert.start_time = _startime
        insert.end_time = _endtime
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _update(self, _id, _clientid, _jobtipeid, _startime, _endtime):
        update = contract_client()
        update = contract_client.query.filter_by(id = _id).first()
        update.client_id = _clientid
        update.position_id
        update.start_time
        update.end_time
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = contract_client()
        update = contract_client.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self):
        response = {}
        response['data'] = []
        _hr_short_desc = contract_client.query.filter_by(status = True).all()
        for i in _hr_short_desc:
            response['data'].append({
                'id' : i.id,
                'client_id' : i.client_id,
                'position_id' : i.position_id,
                'start_time' : i.start_time,
                'end_time' : i.end_time
            })
        return response

    def _data(self, _id):
        response = {}
        _hr_short_desc =  contract_client.query.filter_by(id = _id).filter_by(status = True).first()
        if _hr_short_desc is not None:
            response['id'] = _hr_short_desc.id
            response['client_id'] = _hr_short_desc.client_id
            response['position_id'] = _hr_short_desc.position_id
            response['start_time'] = _hr_short_desc.start_time
            response['end_time'] = _hr_short_desc.end_time
        return response

class Vacancy_Image(db.Model):
    __tablename__ = 'vacancy_image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    jobvacancy_id = db.Column(db.Integer, db.ForeignKey('jobvacancy.id'))
    image_title_id = db.Column(db.Integer, db.ForeignKey('vacancy_image_title.id'))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    updated_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _insert(self, _name, _jobvacancy_id, _img_title_id):
        _img_service_jobvacancy = Vacancy_Image()
        _img_service_jobvacancy.name = _name
        _img_service_jobvacancy.jobvacancy_id = _jobvacancy_id
        _img_service_jobvacancy.image_title_id = _img_title_id
        db.session.add(_img_service_jobvacancy)
        db.session.commit()

    def _update(self, _id, _name, _img_title_id):
        _img_service_jobvacancy = Vacancy_Image()
        _img_service_jobvacancy = Vacancy_Image.query.filter_by(id = _id).first()
        _img_service_jobvacancy.name = _name
        _img_service_jobvacancy.image_title_id = _img_title_id
        db.session.add(_img_service_jobvacancy)
        db.session.commit()

    def _remove(self, _id):
        _img_service_jobvacancy = Vacancy_Image()
        _img_service_jobvacancy = Vacancy_Image.query.filter_by(id = _id).first()
        _img_service_jobvacancy.status = False
        db.session.add(_img_service_jobvacancy)
        db.session.commit()

    def _data(self, _id):
        response = {}
        _img_service_jobvacancy = Vacancy_Image.query.filter_by(id = _id, status = True).first()
        if _img_service_jobvacancy is not None:
            response['id'] = _img_service_jobvacancy.id
            response['name'] = _img_service_jobvacancy.name
            response['jobvacancy_id'] = _img_service_jobvacancy.jobvacancy_id
            response['image_title_id'] = _img_service_jobvacancy.image_title_id
        return response

    def _dataimage(self, _jobvacancyid, _title):
        response = {}
        _img_service_jobvacancy = Vacancy_Image.query.filter_by(jobvacancy_id = _jobvacancyid, image_title_id = _title, status = True).first()
        if _img_service_jobvacancy is not None:
            response['id'] = _img_service_jobvacancy.id
            response['name'] = _img_service_jobvacancy.name
            response['jobvacancy_id'] = _img_service_jobvacancy.jobvacancy_id
            response['image_title_id'] = _img_service_jobvacancy.image_title_id
        return response

    def _list(self, _jobvacancyid):
        response = {}
        response['data'] = []
        _img_service_jobvacancy = Vacancy_Image.query.filter_by(jobvacancy_id = _jobvacancyid, status = True).all()
        for i in _img_service_jobvacancy:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'jobvacancy_id' : i.jobvacancy_id,
                'image_title_id' : i.image_title_id
            })
        return response

class vacancy_image_title(db.Model):
    __tablename__ = 'vacancy_image_title'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    vacancy_image = db.relationship('Vacancy_Image', backref='vacancy_image_title', lazy='dynamic')

    @staticmethod
    def _insert():
        _imgTitle = ["fotojob", "filejob"]
        for i in _imgTitle:
            _imgT = vacancy_image_title()
            _imgT.name = i
            db.session.add(_imgT)
            db.session.commit()       

class Image_Service(db.Model):
    __tablename__ = 'image_service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_title_id = db.Column(db.Integer, db.ForeignKey('image_title.id'))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    updated_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _insert(self, _name, _user_id, _img_title_id):
        _img_service_ = Image_Service()
        _img_service_.name = _name
        _img_service_.user_id = _user_id
        _img_service_.image_title_id = _img_title_id
        db.session.add(_img_service_)
        db.session.commit()

    def _update(self, _id, _name, _img_title_id):
        _img_service_ = Image_Service()
        _img_service_ = Image_Service.query.filter_by(id = _id).first()
        _img_service_.name = _name
        _img_service_.image_title_id = _img_title_id
        db.session.add(_img_service_)
        db.session.commit()

    def _remove(self, _id):
        _img_service_ = Image_Service()
        _img_service_ = Image_Service.query.filter_by(id = _id).first()
        _img_service_.status = False
        db.session.add(_img_service_)
        db.session.commit()

    def _data(self, _id):
        response = {}
        _img_service_=  Image_Service.query.filter_by(id = _id, status = True).first()
        if _img_service_ is not None:
            response['id'] = _img_service_.id
            response['name'] = _img_service_.name
            response['user_id'] = _img_service_.user_id
            response['image_title_id'] = _img_service_.image_title_id
        return response

    def _dataimage(self, _userid, _title):
        response = {}
        _img_service_=  Image_Service.query.filter_by(user_id = _userid,image_title_id = _title , status = True).first()
        if _img_service_ is not None:
            response['id'] = _img_service_.id
            response['name'] = _img_service_.name
            response['user_id'] = _img_service_.user_id
            response['image_title_id'] = _img_service_.image_title_id
        return response

    def _list(self, _userid):
        response = {}
        response['data'] = []
        _img_service_=  Image_Service.query.filter_by(user_id = _userid, status = True).all()
        for i in _img_service_:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'user_id' : i.user_id,
                'image_title_id' : i.image_title_id
            })
        return response

class Image_Title(db.Model):
    __tablename__ = 'image_title'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True) 

    image_service = db.relationship('Image_Service', backref='Image_Title', lazy='dynamic')

    @staticmethod
    def _insert():
        _imgTitle = ["Profil Picture", "cv", "ID card", "npwp"]
        for i in _imgTitle:
            _imgT = Image_Title()
            _imgT.name = i
            db.session.add(_imgT)
            db.session.commit()

class list_status_address(db.Model,UserMixin):
    __tablename__ = 'list_status_address'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name):
        insert = list_status_address()
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name):
        update = list_status_address()
        update = list_status_address.query.filter_by(id = _id).first()
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _list(self):
        response = {}
        response['data'] = []
        _statusaddress = list_status_address.query.filter_by(status = True).all()
        for i in _statusaddress:
            response['data'].append({
                'id' : i.id ,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _statusaddress = list_status_address.query.filter_by(id = _id, status = True).first()
        if _statusaddress is not None:
            response['id'] = _statusaddress.id
            response['name'] = _statusaddress.name
        return response

class role(db.Model,UserMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    list_role_id = db.Column(db.Integer, db.ForeignKey('list_role.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _insert(self, _listroleid, _userid):
        _role = role()
        _role.list_role_id = _listroleid
        _role.user_id = _userid
        db.session.add(_role)
        db.session.commit()

    def _update(self, _id, _listroleid, _userid):
        _role = role()
        _role = role.query.filter_by(id = _id).first()
        _role.list_role_id = _listroleid
        _role.user_id = _userid
        db.session.add(_role)
        db.session.commit()

    def _remove(self, _id):
        _role = role()
        _role = role.query.filter_by(id = _id).first()
        _role.status = False
        db.session.add(_role)
        db.session.commit()

    def _data(self, _id):
        response = {}
        _role = role.query.filter_by(id = _id, status = True).first()
        if _role is not None:
            response['id'] = _role.id
            response['list_role'] = list_role().data(_role.list_role_id)
            response['user_id'] = User()._data(_role.user_id)
        return response

    def _databyuserid(self, _userid):
        response = {}
        _role = role.query.filter_by(user_id = _userid, status = True).first()
        if _role is not None:
            response['id'] = _role.id
            response['list_role'] = list_role()._data(_role.list_role_id)
        return response

    def _datauseraccess(self, _userid, _clientid):
        response = {}
        response['data'] = []
        _role =  role.query.filter_by(user_id = _userid, status = True).all()
        for i in _role:
            response['data'].append({
                'menu' : menu()._listmenu(_clientid),
                'permission' : role_permission()._listbyrole(i.list_role_id)
            })
        return response

    def _listpermission(self, _userid):
        response = []
        _role =  role.query.filter_by(user_id = _userid, status = True).all()
        for i in _role:
            response.append(role_permission()._listview(i.list_role_id))
        return response

class menu(db.Model,UserMixin):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    icon = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _data(self, _id):
        response = {}
        _menu =  menu.query.filter_by(id = _id, status = True).first()
        if _menu is not None:
            response['id'] = _menu.id
            response['name'] = _menu.name
        return response

    def _listmenu(self, _clientid):
        response = []
        _menu =  menu.query.filter_by(client_id = _clientid, status = True).all()
        for i in _menu:
            response.append({
                'name' : i.name,
                'icon' : i.icon,
                'sub_menu' : sub_menu()._list(i.id)
            })
        return response

class sub_menu(db.Model,UserMixin):
    __tablename__ = 'sub_menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    icon = db.Column(db.Text)
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _data(self, _id):
        response = {}
        _sub_menu =  sub_menu.query.filter_by(id = _id, status = True).first()
        if _sub_menu is not None:
            response['id'] = _sub_menu.id
            response['name'] = _sub_menu.name
        return response

    def _list(self, _menuid):
        response = []
        _sub_menu =  sub_menu.query.filter_by(menu_id = _menuid, status = True).all()
        for i in _sub_menu:
            response.append({
                'id' : i.id,
                'name' : i.name,
                'icon' : i.icon
            })
        return response

    def _listforpermission(self):
        response = []
        _sub_menu =  sub_menu.query.filter_by(status = True).all()
        for i in _sub_menu:
            response.append({
                'id' : i.id,
                'name' : i.name
            })
        return response

class role_permission(db.Model,UserMixin):
    __tablename__ = 'role_permission'
    id = db.Column(db.Integer, primary_key=True)
    list_role_id = db.Column(db.Integer, db.ForeignKey('list_role.id'))
    sub_menu_id = db.Column(db.Integer, db.ForeignKey('sub_menu.id'))
    insert = db.Column(db.Boolean)
    update = db.Column(db.Boolean)
    remove = db.Column(db.Boolean)
    view = db.Column(db.Boolean)
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _insert(self, _listroleid, _submenuid, _insert, _update, _remove, _view):
        _rolepermission = role_permission()
        _rolepermission.list_role_id = _listroleid
        _rolepermission.sub_menu_id = _submenuid
        _rolepermission.insert = _insert
        _rolepermission.update = _update
        _rolepermission.remove = _remove
        _rolepermission.view = _view
        db.session.add(_rolepermission)
        db.session.commit()

    def _update(self, _id, _listroleid, _submenuid, _insert, _update, _remove, _view):
        _rolepermission = role_permission()
        _rolepermission = role_permission.query.filter_by(id = _id).first()
        _rolepermission.list_role_id = _listroleid
        _rolepermission.sub_menu_id = _submenuid
        _rolepermission.insert = _insert
        _rolepermission.update = _update
        _rolepermission.remove = _remove
        _rolepermission.view = _view
        db.session.add(_rolepermission)
        db.session.commit()

    def _remove(self, _id):
        _rolepermission = role_permission()
        _rolepermission = role_permission.query.filter_by(id = _id).first()
        _rolepermission.status = False
        db.session.add(_rolepermission)
        db.session.commit()

    def _data(self, _id):
        response = {}
        _role_permission =  role_permission.query.filter_by(id = _id, status = True).first()
        if _role_permission is not None:
            response['id'] = _role_permission.id
            response['insert'] = _role_permission.insert
            response['update'] = _role_permission.update
            response['remove'] = _role_permission.remove
            response['view'] = _role_permission.view
        return response

    def _listbyrole(self, _roleid):
        response = []
        _role_permission =  role_permission.query.filter_by(list_role_id = _roleid, status = True).all()
        for i in _role_permission:
            response.append({
                'id' : i.id,
                'sub_menu'  : i.sub_menu_id,
                'insert'    : i.insert,
                'update'    : i.update,
                'remove'    : i.remove,
                'view'  : i.view
            })
        return response

    def _listview(self, _roleid):
        response = []
        _role_permission =  role_permission.query.filter_by(list_role_id = _roleid, status = True, view = True).all()
        for i in _role_permission:
            response.append(sub_menu()._data(i.sub_menu_id)['name'])
        return response

class list_role(db.Model,UserMixin):
    __tablename__ = 'list_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    added_time = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean, default=True)

    def _insert(self, _name, _clientid):
        _list_role = list_role()
        _list_role.name = _name
        _list_role.client_id = _clientid
        db.session.add(_list_role)
        db.session.commit()

    def _update(self, _id, _name):
        _list_role = list_role()
        _list_role = list_role.query.filter_by(id = _id).first()
        _list_role.name = _name
        db.session.add(_list_role)
        db.session.commit()

    def _remove(self, _id):
        _list_role = list_role()
        _list_role = list_role.query.filter_by(id = _id).first()
        _list_role.status = False
        db.session.add(_list_role)
        db.session.commit()

    def _data(self, _id):
        response = {}
        _list_role =  list_role.query.filter_by(id = _id, status = True).first()
        if _list_role is not None:
            response['id'] = _list_role.id
            response['name'] = _list_role.name
        return response

    def _list(self,_clientid):
        response = {}
        response['data'] = []
        _list_role =  list_role.query.filter_by(client_id = _clientid, status = True).all()
        for i in _list_role:
            response['data'].append({
                'id' : i.id,
                'name' : i.name
            })
        return response

def reinit():
    db.drop_all()
    db.create_all()

def ifnull(var):
  if var is None:
    return var
  return var.strftime("%Y-%m-%d")

def userbaruexcel():
        df = pd.read_excel(r'D:\New folder (2)\pamtol.xlsx', sheet_name='Sheet1')
        for i in df.index:
                dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + df['tanggal lahir'][i] - 2)
                provincektp = province.query.filter(province.name.like('%'+df['provinsi ktp'][i]+'%')).first()
                if provincektp is not None:
                        provincektp = provincektp.id
                cityktp = city.query.filter(city.name.like('%'+df['kabupaten ktp'][i]+'%')).first()
                if cityktp is not None:
                        cityktp = cityktp.id
                kecamatanktp = kecamatan.query.filter(kecamatan.name.like('%'+df['kecamatan ktp'][i]+'%')).first()
                if kecamatanktp is not None:
                        kecamatanktp = kecamatanktp.id
                kelurahanktp = kelurahan.query.filter(kelurahan.name.like('%'+df['kelurahan ktp'][i]+'%')).first()
                if kelurahanktp is not None:
                        kelurahanktp = kelurahanktp.id

                new_user = User()._insert(df['Nama Lengkap'][i], df['No HandPhone'][i], 'cpipassword!', '123456', df['email'][i], dt, df['tempat lahir'][i], df['alamat ktp'][i], df['Gender'][i], provincektp, cityktp, kecamatanktp,kelurahanktp, None, df['rt ktp'][i], df['rw ktp'][i],1,)

                ptkpid = ptkp.query.filter(ptkp.name.like('%'+df['Status TK'][i]+'%')).first()
                if ptkpid is not None:
                        ptkpid = ptkpid.id
                identity()._insert(new_user.id,df['nik karyawan'][i],ptkpid)
                bank_account()._insert(new_user.id,2,df['nomor rekening'][i])
                position()._insert(new_user.id,2,2,2)
                salary()._insert(new_user.id,3940973)
        return ''

def updateuser():
        df = pd.read_excel(r'D:\New folder (2)\Data SDM CPI.xlsx', sheet_name='Sheet1')
        for i in df.index:
            update = User.query.filter_by(name = df['Nama Lengkap'][i]).first()
            identity()._insert(update.id, df['nik karyawan'][i], None)
        return ''

class level_education(db.Model,UserMixin):
    __tablename__ = 'education_level'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self,_name):
        insert = level_education()
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)

    def _update(self, _id, _name):
        update = level_education()
        update = level_education.query.filter_by(id = _id).first()
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _list(self):
        response = {}
        response['data'] = []
        _level_education = level_education.query.filter_by(status = True).all()
        for i in _level_education:
            response['data'].append({
                'id' : i.id ,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _level_education = level_education.query.filter_by(id = _id, status = True).first()
        if _level_education is not None:
            response['id'] = _level_education.id
            response['name'] = _level_education.name
        return response

class history_education(db.Model,UserMixin):
    __tablename__ = 'history_education'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    level_education = db.Column(db.Integer, db.ForeignKey('education_level.id'))
    nama_sd = db.Column(db.String(100))
    kota_sd = db.Column(db.String(50))
    jurusan_sd = db.Column(db.String(50))
    masuk_sd = db.Column(db.Integer)
    lulus_sd = db.Column(db.Integer)
    status_sd = db.Column(db.String(10))
    nama_smp = db.Column(db.String(100))
    kota_smp = db.Column(db.String(50))
    jurusan_smp = db.Column(db.String(50))
    masuk_smp = db.Column(db.Integer)
    lulus_smp = db.Column(db.Integer)
    status_smp = db.Column(db.String(10))
    nama_sma = db.Column(db.String(100))
    kota_sma = db.Column(db.String(50))
    jurusan_sma = db.Column(db.String(50))
    masuk_sma = db.Column(db.Integer)
    lulus_sma = db.Column(db.Integer)
    status_sma = db.Column(db.String(10))
    nama_s1 = db.Column(db.String(100))
    kota_s1 = db.Column(db.String(50))
    jurusan_s1 = db.Column(db.String(50))
    masuk_s1 = db.Column(db.Integer)
    lulus_s1 = db.Column(db.Integer)
    status_s1 = db.Column(db.String(10))
    nama_s2 = db.Column(db.String(100))
    kota_s2 = db.Column(db.String(50))
    jurusan_s2 = db.Column(db.String(50))
    masuk_s2 = db.Column(db.Integer)
    lulus_s2 = db.Column(db.Integer)
    status_s2 = db.Column(db.String(10))
    nama_s3 = db.Column(db.String(100))
    kota_s3 = db.Column(db.String(50))
    jurusan_s3 = db.Column(db.String(50))
    masuk_s3 = db.Column(db.Integer)
    lulus_s3 = db.Column(db.Integer)
    status_s3 = db.Column(db.String(10))
    bidang1 = db.Column(db.String(100))
    penyelenggara1 = db.Column(db.String(100))
    kota_kursus1 = db.Column(db.String(50))
    lama_kursus1 = db.Column(db.String(50))
    tahun_masuk1 = db.Column(db.Integer)
    biaya1 = db.Column(db.String(100))
    bidang2 = db.Column(db.String(100))
    penyelenggara2 = db.Column(db.String(100))
    kota_kursus2 = db.Column(db.String(50))
    lama_kursus2 = db.Column(db.String(50))
    tahun_masuk2 = db.Column(db.Integer)
    biaya2 = db.Column(db.String(100))
    bidang3 = db.Column(db.String(100))
    penyelenggara3 = db.Column(db.String(100))
    kota_kursus3 = db.Column(db.String(50))
    lama_kursus3 = db.Column(db.String(50))
    tahun_masuk3 = db.Column(db.Integer)
    biaya3 = db.Column(db.String(100))
    bidang4 = db.Column(db.String(100))
    penyelenggara4 = db.Column(db.String(100))
    kota_kursus4 = db.Column(db.String(50))
    lama_kursus4 = db.Column(db.String(50))
    tahun_masuk4 = db.Column(db.Integer)
    biaya4 = db.Column(db.String(100))
    bidang5 = db.Column(db.String(100))
    penyelenggara5 = db.Column(db.String(100))
    kota_kursus5 = db.Column(db.String(50))
    lama_kursus5 = db.Column(db.String(50))
    tahun_masuk5 = db.Column(db.Integer)
    biaya5 = db.Column(db.String(100))
    bidang6 = db.Column(db.String(100))
    penyelenggara6 = db.Column(db.String(100))
    kota_kursus6 = db.Column(db.String(50))
    lama_kursus6 = db.Column(db.String(50))
    tahun_masuk6 = db.Column(db.Integer)
    biaya6 = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _userid, _leveleducation, _namasd, _kotasd, _jurusansd, _masuksd, _lulussd, _statussd, _namasmp, _kotasmp, _jurusansmp, _masuksmp, _lulussmp, _statussmp, _namasma, _kotasma, _jurusansma, _masuksma, _lulussma, _statussma, _namas1, _kotas1, _jurusans1, _masuks1, _luluss1, _statuss1, _namas2, _kotas2, _jurusans2, _masuks2, _luluss2, _statuss2, _namas3, _kotas3, _jurusans3, _masuks3, _luluss3, _statuss3, _bidang1, _penyelenggara1, _kotakursus1, _lamakursus1, _tahunmasuk1, _biaya1, _bidang2, _penyelenggara2, _kotakursus2, _lamakursus2, _tahunmasuk2, _biaya2, _bidang3, _penyelenggara3, _kotakursus3, _lamakursus3, _tahunmasuk3, _biaya3, _bidang4, _penyelenggara4, _kotakursus4, _lamakursus4, _tahunmasuk4, _biaya4, _bidang5, _penyelenggara5, _kotakursus5, _lamakursus5, _tahunmasuk5, _biaya5, _bidang6, _penyelenggara6, _kotakursus6, _lamakursus6, _tahunmasuk6, _biaya6):
        insert = history_education()
        insert.user_id = _userid
        insert.level_education = _leveleducation
        insert.nama_sd = _namasd
        insert.kota_sd = _kotasd
        insert.jurusan_sd = _jurusansd
        insert.masuk_sd = _masuksd
        insert.lulus_sd = _lulussd
        insert.status_sd = _statussd
        insert.nama_smp = _namasmp
        insert.kota_smp = _kotasmp
        insert.jurusan_smp = _jurusansmp
        insert.masuk_smp = _masuksmp
        insert.lulus_smp = _lulussmp
        insert.status_smp = _statussmp
        insert.nama_sma = _namasma
        insert.kota_sma = _kotasma
        insert.jurusan_sma = _jurusansma
        insert.masuk_sma = _masuksma
        insert.lulus_sma = _lulussma
        insert.status_sma = _statussma
        insert.nama_s1 = _namas1
        insert.kota_s1 = _kotas1
        insert.jurusan_s1 = _jurusans1
        insert.masuk_s1 = _masuks1
        insert.lulus_s1 = _luluss1
        insert.status_s1 = _statuss1
        insert.nama_s2 = _namas2
        insert.kota_s2 = _kotas2
        insert.jurusan_s2 = _jurusans2
        insert.masuk_s2 = _masuks2
        insert.lulus_s2 = _luluss2
        insert.status_s2 = _statuss2
        insert.nama_s3 = _namas3
        insert.kota_s3 = _kotas3
        insert.jurusan_s3 = _jurusans3
        insert.masuk_s3 = _masuks3
        insert.lulus_s3 = _luluss3
        insert.status_s3 = _statuss3
        insert.bidang1 = _bidang1
        insert.penyelenggara1 = _penyelenggara1
        insert.kota_kursus1 = _kotakursus1
        insert.lama_kursus1 = _lamakursus1
        insert.tahun_masuk1 = _tahunmasuk1
        insert.biaya1 = _biaya1
        insert.bidang2 = _bidang2
        insert.penyelenggara2 = _penyelenggara2
        insert.kota_kursus2 = _kotakursus2
        insert.lama_kursus2 = _lamakursus2
        insert.tahun_masuk2 = _tahunmasuk2
        insert.biaya2 = _biaya2
        insert.bidang3 = _bidang3
        insert.penyelenggara3 = _penyelenggara3
        insert.kota_kursus3 = _kotakursus3
        insert.lama_kursus3 = _lamakursus3
        insert.tahun_masuk3 = _tahunmasuk3
        insert.biaya3 = _biaya3
        insert.bidang4 = _bidang4
        insert.penyelenggara4 = _penyelenggara4
        insert.kota_kursus4 = _kotakursus4
        insert.lama_kursus4 = _lamakursus4
        insert.tahun_masuk4 = _tahunmasuk4
        insert.biaya4 = _biaya4
        insert.bidang5 = _bidang5
        insert.penyelenggara5 = _penyelenggara5
        insert.kota_kursus5 = _kotakursus5
        insert.lama_kursus5 = _lamakursus5
        insert.tahun_masuk5 = _tahunmasuk5
        insert.biaya5 = _biaya5
        insert.bidang6 = _bidang6
        insert.penyelenggara6 = _penyelenggara6
        insert.kota_kursus6 = _kotakursus6
        insert.lama_kursus6 = _lamakursus6
        insert.tahun_masuk6 = _tahunmasuk6
        insert.biaya6 = _biaya6
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _update(self, _id, _leveleducation, _namasd, _kotasd, _jurusansd, _masuksd, _lulussd, _statussd, _namasmp, _kotasmp, _jurusansmp, _masuksmp, _lulussmp, _statussmp, _namasma, _kotasma, _jurusansma, _masuksma, _lulussma, _statussma, _namas1, _kotas1, _jurusans1, _masuks1, _luluss1, _statuss1, _namas2, _kotas2, _jurusans2, _masuks2, _luluss2, _statuss2, _namas3, _kotas3, _jurusans3, _masuks3, _luluss3, _statuss3, _bidang1, _penyelenggara1, _kotakursus1, _lamakursus1, _tahunmasuk1, _biaya1, _bidang2, _penyelenggara2, _kotakursus2, _lamakursus2, _tahunmasuk2, _biaya2, _bidang3, _penyelenggara3, _kotakursus3, _lamakursus3, _tahunmasuk3, _biaya3, _bidang4, _penyelenggara4, _kotakursus4, _lamakursus4, _tahunmasuk4, _biaya4, _bidang5, _penyelenggara5, _kotakursus5, _lamakursus5, _tahunmasuk5, _biaya5, _bidang6, _penyelenggara6, _kotakursus6, _lamakursus6, _tahunmasuk6, _biaya6):
        update = history_education()
        update = history_education.query.filter_by(id=_id).first()
        update.level_education = _leveleducation
        update.nama_sd = _namasd
        update.kota_sd = _kotasd
        update.jurusan_sd = _jurusansd
        update.masuk_sd = _masuksd
        update.lulus_sd = _lulussd
        update.status_sd = _statussd
        update.nama_smp = _namasmp
        update.kota_smp = _kotasmp
        update.jurusan_smp = _jurusansmp
        update.masuk_smp = _masuksmp
        update.lulus_smp = _lulussmp
        update.status_smp = _statussmp
        update.nama_sma = _namasma
        update.kota_sma = _kotasma
        update.jurusan_sma = _jurusansma
        update.masuk_sma = _masuksma
        update.lulus_sma = _lulussma
        update.status_sma = _statussma
        update.nama_s1 = _namas1
        update.kota_s1 = _kotas1
        update.jurusan_s1 = _jurusans1
        update.masuk_s1 = _masuks1
        update.lulus_s1 = _luluss1
        update.status_s1 = _statuss1
        update.nama_s2 = _namas2
        update.kota_s2 = _kotas2
        update.jurusan_s2 = _jurusans2
        update.masuk_s2 = _masuks2
        update.lulus_s2 = _luluss2
        update.status_s2 = _statuss2
        update.nama_s3 = _namas3
        update.kota_s3 = _kotas3
        update.jurusan_s3 = _jurusans3
        update.masuk_s3 = _masuks3
        update.lulus_s3 = _luluss3
        update.status_s3 = _statuss3
        update.bidang1 = _bidang1
        update.penyelenggara1 = _penyelenggara1
        update.kota_kursus1 = _kotakursus1
        update.lama_kursus1 = _lamakursus1
        update.tahun_masuk1 = _tahunmasuk1
        update.biaya1 = _biaya1
        update.bidang2 = _bidang2
        update.penyelenggara2 = _penyelenggara2
        update.kota_kursus2 = _kotakursus2
        update.lama_kursus2 = _lamakursus2
        update.tahun_masuk2 = _tahunmasuk2
        update.biaya2 = _biaya2
        update.bidang3 = _bidang3
        update.penyelenggara3 = _penyelenggara3
        update.kota_kursus3 = _kotakursus3
        update.lama_kursus3 = _lamakursus3
        update.tahun_masuk3 = _tahunmasuk3
        update.biaya3 = _biaya3
        update.bidang4 = _bidang4
        update.penyelenggara4 = _penyelenggara4
        update.kota_kursus4 = _kotakursus4
        update.lama_kursus4 = _lamakursus4
        update.tahun_masuk4 = _tahunmasuk4
        update.biaya4 = _biaya4
        update.bidang5 = _bidang5
        update.penyelenggara5 = _penyelenggara5
        update.kota_kursus5 = _kotakursus5
        update.lama_kursus5 = _lamakursus5
        update.tahun_masuk5 = _tahunmasuk5
        update.biaya5 = _biaya5
        update.bidang6 = _bidang6
        update.penyelenggara6 = _penyelenggara6
        update.kota_kursus6 = _kotakursus6
        update.lama_kursus6 = _lamakursus6
        update.tahun_masuk6 = _tahunmasuk6
        update.biaya6 = _biaya6
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = history_education()
        update = history_education.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()


    def _list(self):
        response = {}
        response['data'] = []
        _history_education = history_education.query.filter_by(status = True).all()
        for i in _history_education:
            response['data'].append({
                'id' : i.id,
                    'user_id' : i.user_id,
                    'level_education' : i.level_education,
                    'nama_sd' : i.nama_sd,
                    'kota_sd' : i.kota_sd,
                    'jurusan_sd' : i.jurusan_sd,
                    'masuk_sd' : i.masuk_sd,
                    'lulus_sd' : i.lulus_sd,
                    'status_sd' : i.status_sd,
                    'nama_smp' : i.nama_smp,
                    'kota_smp' : i.kota_smp,
                    'jurusan_smp' : i.jurusan_smp,
                    'masuk_smp' : i.masuk_smp,
                    'lulus_smp' : i.lulus_smp,
                    'status_smp' : i.status_smp,
                    'nama_sma' : i.nama_sma,
                    'kota_sma' : i.kota_sma,
                    'jurusan_sma' : i.jurusan_sma,
                    'masuk_sma' : i.masuk_sma,
                    'lulus_sma' : i.lulus_sma,
                    'status_sma' : i.status_sma,
                    'nama_s1' : i.nama_s1,
                    'kota_s1' : i.kota_s1,
                    'jurusan_s1' : i.jurusan_s1,
                    'masuk_s1' : i.masuk_s1,
                    'lulus_s1' : i.lulus_s1,
                    'status_s1' : i.status_s1,
                    'nama_s2' : i.nama_s2,
                    'kota_s2' : i.kota_s2,
                    'jurusan_s2' : i.jurusan_s2,
                    'masuk_s2' : i.masuk_s2,
                    'lulus_s2' : i.lulus_s2,
                    'status_s2' : i.status_s2,
                    'nama_s3' : i.nama_s3,
                    'kota_s3' : i.kota_s3,
                    'jurusan_s3' : i.jurusan_s3,
                    'masuk_s3' : i.masuk_s3,
                    'lulus_s3' : i.lulus_s3,
                    'status_s3' : i.status_s3,
                    'bidang1' : i.bidang1,
                    'penyelenggara1' : i.penyelenggara1,
                    'kota_kursus1' : i.kota_kursus1,
                    'lama_kursus1' : i.lama_kursus1,
                    'tahun_masuk1' : i.tahun_masuk1,
                    'biaya1' : i.biaya1,
                    'bidang2' : i.bidang2,
                    'penyelenggara2' : i.penyelenggara2,
                    'kota_kursus2' : i.kota_kursus2,
                    'lama_kursus2' : i.lama_kursus2,
                    'tahun_masuk2' : i.tahun_masuk2,
                    'biaya2' : i.biaya2,
                    'bidang3' : i.bidang3,
                    'penyelenggara3' : i.penyelenggara3,
                    'kota_kursus3' : i.kota_kursus3,
                    'lama_kursus3' : i.lama_kursus3,
                    'tahun_masuk3' : i.tahun_masuk3,
                    'biaya3' : i.biaya3,
                    'bidang4' : i.bidang4,
                    'penyelenggara4' : i.penyelenggara4,
                    'kota_kursus4' : i.kota_kursus4,
                    'lama_kursus4' : i.lama_kursus4,
                    'tahun_masuk4' : i.tahun_masuk4,
                    'biaya4' : i.biaya4,
                    'bidang5' : i.bidang5,
                    'penyelenggara5' : i.penyelenggara5,
                    'kota_kursus5' : i.kota_kursus5,
                    'lama_kursus5' : i.lama_kursus5,
                    'tahun_masuk5' : i.tahun_masuk5,
                    'biaya5' : i.biaya5,
                    'bidang6' : i.bidang6,
                    'penyelenggara6' : i.penyelenggara6,
                    'kota_kursus6' : i.kota_kursus6,
                    'lama_kursus6' : i.lama_kursus6,
                    'tahun_masuk6' : i.tahun_masuk6,
                    'biaya6' : i.biaya6
            })
        return response


    def _data(self, _userid):
        response = {}
        _history_education = history_education.query.filter_by(user_id = _userid, status = True).first()
        if _history_education is not None:
                    response['id'] = _history_education.id
                    response['user_id'] = _history_education.user_id
                    response['level_education'] = _history_education.level_education
                    response['nama_sd'] = _history_education.nama_sd
                    response['kota_sd'] = _history_education.kota_sd
                    response['jurusan_sd'] = _history_education.jurusan_sd
                    response['masuk_sd'] = _history_education.masuk_sd
                    response['lulus_sd'] = _history_education.lulus_sd
                    response['status_sd']= _history_education.status_sd
                    response['nama_smp']= _history_education.nama_smp
                    response['kota_smp']= _history_education.kota_smp
                    response['jurusan_smp']= _history_education.jurusan_smp
                    response['masuk_smp']= _history_education.masuk_smp
                    response['lulus_smp']= _history_education.lulus_smp
                    response['status_smp']= _history_education.status_smp
                    response['nama_sma']= _history_education.nama_sma
                    response['kota_sma']= _history_education.kota_sma
                    response['jurusan_sma']= _history_education.jurusan_sma
                    response['masuk_sma']= _history_education.masuk_sma
                    response['lulus_sma']= _history_education.lulus_sma
                    response['status_sma']= _history_education.status_sma
                    response['nama_s1']= _history_education.nama_s1
                    response['kota_s1']= _history_education.kota_s1
                    response['jurusan_s1']= _history_education.jurusan_s1
                    response['masuk_s1']= _history_education.masuk_s1
                    response['lulus_s1']= _history_education.lulus_s1
                    response['status_s1']= _history_education.status_s1
                    response['nama_s2']= _history_education.nama_s2
                    response['kota_s2']= _history_education.kota_s2
                    response['jurusan_s2']= _history_education.jurusan_s2
                    response['masuk_s2']= _history_education.masuk_s2
                    response['lulus_s2']= _history_education.lulus_s2
                    response['status_s2']= _history_education.status_s2
                    response['nama_s3']= _history_education.nama_s3
                    response['kota_s3']= _history_education.kota_s3
                    response['jurusan_s3']= _history_education.jurusan_s3
                    response['masuk_s3']= _history_education.masuk_s3
                    response['lulus_s3']= _history_education.lulus_s3
                    response['status_s3']= _history_education.status_s3
                    response['bidang1']= _history_education.bidang1
                    response['penyelenggara1']= _history_education.penyelenggara1
                    response['kota_kursus1']= _history_education.kota_kursus1
                    response['lama_kursus1']= _history_education.lama_kursus1
                    response['tahun_masuk1']= _history_education.tahun_masuk1
                    response['biaya1']= _history_education.biaya1
                    response['bidang2']= _history_education.bidang2
                    response['penyelenggara2']= _history_education.penyelenggara2
                    response['kota_kursus2']= _history_education.kota_kursus2
                    response['lama_kursus2']= _history_education.lama_kursus2
                    response['tahun_masuk2']= _history_education.tahun_masuk2
                    response['biaya2']= _history_education.biaya2
                    response['bidang3']= _history_education.bidang3
                    response['penyelenggara3']= _history_education.penyelenggara3
                    response['kota_kursus3']= _history_education.kota_kursus3
                    response['lama_kursus3']= _history_education.lama_kursus3
                    response['tahun_masuk3']= _history_education.tahun_masuk3
                    response['biaya3']= _history_education.biaya3
                    response['bidang4']= _history_education.bidang4
                    response['penyelenggara4']= _history_education.penyelenggara4
                    response['kota_kursus4']= _history_education.kota_kursus4
                    response['lama_kursus4']= _history_education.lama_kursus4
                    response['tahun_masuk4']= _history_education.tahun_masuk4
                    response['biaya4']= _history_education.biaya4
                    response['bidang5']= _history_education.bidang5
                    response['penyelenggara5']= _history_education.penyelenggara5
                    response['kota_kursus5']= _history_education.kota_kursus5
                    response['lama_kursus5']= _history_education.lama_kursus5
                    response['tahun_masuk5']= _history_education.tahun_masuk5
                    response['biaya5']= _history_education.biaya5
                    response['bidang6']= _history_education.bidang6
                    response['penyelenggara6']= _history_education.penyelenggara6
                    response['kota_kursus6']= _history_education.kota_kursus6
                    response['lama_kursus6']= _history_education.lama_kursus6
                    response['tahun_masuk6']= _history_education.tahun_masuk6
                    response['biaya6']= _history_education.biaya6
        return response

class applicantstatus(db.Model,UserMixin):
    __tablename__ = 'applicantstatus'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _name):
        insert = applicantstatus()
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _update(self, _id, _name):
        update = applicantstatus()
        update = applicantstatus.query.filter_by(id = _id).first()
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = applicantstatus()
        update = applicantstatus.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self):
        response = {}
        response['data'] = []
        _applicantstatus = applicantstatus.query.filter_by(status = True).all()
        for i in _applicantstatus:
            response['data'].append({
                'id' : i.id,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _applicantstatus = applicantstatus.query.filter_by(id = _id, status = True).first()
        if _applicantstatus is not None:
            response['id'] = _applicantstatus.id
            response['name'] = _applicantstatus.name
        return response

class job_experience(db.Model,UserMixin):
    __tablename__ = 'job_experience'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    npwp = db.Column(db.String(30))
    bpjstk = db.Column(db.String(30))
    bpjs = db.Column(db.String(30))
    aap1 = db.Column(db.String(100))
    klasifikasi1 = db.Column(db.String(100))
    ska1 = db.Column(db.String(30))
    skastart1 = db.Column(db.DateTime)
    skaend1 = db.Column(db.DateTime)
    aap2 = db.Column(db.String(100))
    klasifikasi2 = db.Column(db.String(100))
    ska2 = db.Column(db.String(30))
    skastart2 = db.Column(db.DateTime)
    skaend2 = db.Column(db.DateTime)
    aap3 = db.Column(db.String(100))
    klasifikasi3 = db.Column(db.String(100))
    ska3 = db.Column(db.String(30))
    skastart3 = db.Column(db.DateTime)
    skaend3 = db.Column(db.DateTime)
    aap4 = db.Column(db.String(100))
    klasifikasi4 = db.Column(db.String(100))
    ska4 = db.Column(db.String(30))
    skastart4 = db.Column(db.DateTime)
    skaend4 = db.Column(db.DateTime)
    aap5 = db.Column(db.String(100))
    klasifikasi5 = db.Column(db.String(100))
    ska5 = db.Column(db.String(30))
    skastart5 = db.Column(db.DateTime)
    skaend5 = db.Column(db.DateTime)
    company1 = db.Column(db.String(100))
    comaddress1 = db.Column(db.Text)
    work_position1 = db.Column(db.String(50))
    starttime1 = db.Column(db.String(10))
    endtime1 = db.Column(db.String(10))
    ket1 = db.Column(db.String(100))
    company2 = db.Column(db.String(100))
    comaddress2 = db.Column(db.Text)
    work_position2 = db.Column(db.String(50))
    starttime2 = db.Column(db.String(10))
    endtime2 = db.Column(db.String(10))
    ket2 = db.Column(db.String(100))
    company3 = db.Column(db.String(100))
    comaddress3 = db.Column(db.Text)
    work_position3 = db.Column(db.String(50))
    starttime3 = db.Column(db.String(10))
    endtime3 = db.Column(db.String(10))
    ket3 = db.Column(db.String(100))
    company4 = db.Column(db.String(100))
    comaddress4 = db.Column(db.Text)
    work_position4 = db.Column(db.String(50))
    starttime4 = db.Column(db.String(10))
    endtime4 = db.Column(db.String(10))
    ket4 = db.Column(db.String(100))
    company5 = db.Column(db.String(100))
    comaddress5 = db.Column(db.Text)
    work_position5 = db.Column(db.String(50))
    starttime5 = db.Column(db.String(10))
    endtime5 = db.Column(db.String(10))
    ket5 = db.Column(db.String(100))
    company6 = db.Column(db.String(100))
    comaddress6 = db.Column(db.Text)
    work_position6 = db.Column(db.String(50))
    starttime6 = db.Column(db.String(10))
    endtime6 = db.Column(db.String(10))
    ket6 = db.Column(db.String(100))
    project1 = db.Column(db.String(100))
    project_address1 = db.Column(db.Text)
    project_position1 = db.Column(db.String(50))
    start_project1 = db.Column(db.String(10))
    end_project1 = db.Column(db.String(10))
    ket_project1 = db.Column(db.String(100))
    project2 = db.Column(db.String(100))
    project_address2 = db.Column(db.Text)
    project_position2 = db.Column(db.String(50))
    start_project2 = db.Column(db.String(10))
    end_project2 = db.Column(db.String(10))
    ket_project2 = db.Column(db.String(100))
    project3 = db.Column(db.String(100))
    project_address3 = db.Column(db.Text)
    project_position3 = db.Column(db.String(50))
    start_project3 = db.Column(db.String(10))
    end_project3 = db.Column(db.String(10))
    ket_project3 = db.Column(db.String(100))
    project4 = db.Column(db.String(100))
    project_address4 = db.Column(db.Text)
    project_position4 = db.Column(db.String(50))
    start_project4 = db.Column(db.String(10))
    end_project4 = db.Column(db.String(10))
    ket_project4 = db.Column(db.String(100))
    project5 = db.Column(db.String(100))
    project_address5 = db.Column(db.Text)
    project_position5 = db.Column(db.String(50))
    start_project5 = db.Column(db.String(10))
    end_project5 = db.Column(db.String(10))
    ket_project5 = db.Column(db.String(100))
    project6 = db.Column(db.String(100))
    project_address6 = db.Column(db.Text)
    project_position6 = db.Column(db.String(50))
    start_project6 = db.Column(db.String(10))
    end_project6 = db.Column(db.String(10))
    ket_project6 = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _userid, _npwp, _bpjstk, _bpjs, _aap1, _klasifikasi1, _ska1, _skastart1, _skaend1, _aap2, _klasifikasi2, _ska2, _skastart2, _skaend2, _aap3, _klasifikasi3, _ska3, _skastart3, _skaend3, _aap4, _klasifikasi4, _ska4, _skastart4, _skaend4, _aap5, _klasifikasi5, _ska5, _skastart5, _skaend5, _company1, _comaddress1, _workposition1, _starttime1, _endtime1, _ket1, _company2, _comaddress2, _workposition2, _starttime2, _endtime2, _ket2, _company3, _comaddress3, _workposition3, _starttime3, _endtime3, _ket3, _company4, _comaddress4, _workposition4, _starttime4, _endtime4, _ket4, _company5, _comaddress5, _workposition5, _starttime5, _endtime5, _ket5, _company6, _comaddress6, _workposition6, _starttime6, _endtime6, _ket6, _project1, _projectaddress1, _projectposition1, _startproject1, _endproject1, _ketproject1, _project2, _projectaddress2, _projectposition2, _startproject2, _endproject2, _ketproject2, _project3, _projectaddress3, _projectposition3, _startproject3, _endproject3, _ketproject3, _project4, _projectaddress4, _projectposition4, _startproject4, _endproject4, _ketproject4, _project5, _projectaddress5, _projectposition5, _startproject5, _endproject5, _ketproject5, _project6, _projectaddress6, _projectposition6, _startproject6, _endproject6, _ketproject6):
        insert = job_experience()
        insert.user_id = _userid
        insert.npwp = _npwp
        insert.bpjstk = _bpjstk
        insert.bpjs = _bpjs
        insert.aap1 = _aap1
        insert.klasifikasi1 = _klasifikasi1
        insert.ska1 = _ska1
        insert.skastart1 = _skastart1
        insert.skaend1 = _skaend1
        insert.aap2 = _aap2
        insert.klasifikasi2 = _klasifikasi2
        insert.ska2 = _ska2
        insert.skastart2 = _skastart2
        insert.skaend2 = _skaend2
        insert.aap3 = _aap3
        insert.klasifikasi3 = _klasifikasi3
        insert.ska3 = _ska3
        insert.skastart3 = _skastart3
        insert.skaend3 = _skaend3
        insert.aap4 = _aap4
        insert.klasifikasi4 = _klasifikasi4
        insert.ska4 = _ska4
        insert.skastart4 = _skastart4
        insert.skaend4 = _skaend4
        insert.aap5 = _aap5
        insert.klasifikasi5 = _klasifikasi5
        insert.ska5 = _ska5
        insert.skastart5 = _skastart5
        insert.skaend5 = _skaend5
        insert.company1 = _company1
        insert.comaddress1 = _comaddress1
        insert.work_position1 = _workposition1
        insert.starttime1 = _starttime1
        insert.endtime1 = _endtime1
        insert.ket1 = _ket1
        insert.company2 = _company2
        insert.comaddress2 = _comaddress2
        insert.work_position2 = _workposition2
        insert.starttime2 = _starttime2
        insert.endtime2 = _endtime2
        insert.ket2 = _ket2
        insert.company3 = _company3
        insert.comaddress3 = _comaddress3
        insert.work_position3 = _workposition3
        insert.starttime3 = _starttime3
        insert.endtime3 = _endtime3
        insert.ket3 = _ket3
        insert.company4 = _company4
        insert.comaddress4 = _comaddress4
        insert.work_position4 = _workposition4
        insert.starttime4 = _starttime4
        insert.endtime4 = _endtime4
        insert.ket4 = _ket4
        insert.company5 = _company5
        insert.comaddress5 = _comaddress5
        insert.work_position5 = _workposition5
        insert.starttime5 = _starttime5
        insert.endtime5 = _endtime5
        insert.ket5 = _ket5
        insert.company6 = _company6
        insert.comaddress6 = _comaddress6
        insert.work_position6 = _workposition6
        insert.starttime6 = _starttime6
        insert.endtime6 = _endtime6
        insert.ket6 = _ket6
        insert.project1 = _project1
        insert.project_address1 = _projectaddress1
        insert.project_position1 = _projectposition1
        insert.start_project1 = _startproject1
        insert.end_project1 = _endproject1
        insert.ket_project1 = _ketproject1
        insert.project2 = _project2
        insert.project_address2 = _projectaddress2
        insert.project_position2 = _projectposition2
        insert.start_project2 = _startproject2
        insert.end_project2 = _endproject2
        insert.ket_project2 = _ketproject2
        insert.project3 = _project3
        insert.project_address3 = _projectaddress3
        insert.project_position3 = _projectposition3
        insert.start_project3 = _startproject3
        insert.end_project3 = _endproject3
        insert.ket_project3 = _ketproject3
        insert.project4 = _project4
        insert.project_address4 = _projectaddress4
        insert.project_position4 = _projectposition4
        insert.start_project4 = _startproject4
        insert.end_project4 = _endproject4
        insert.ket_project4 = _ketproject4
        insert.project5 = _project5
        insert.project_address5 = _projectaddress5
        insert.project_position5 = _projectposition5
        insert.start_project5 = _startproject5
        insert.end_project5 = _endproject5
        insert.ket_project5 = _ketproject5
        insert.project6 = _project6
        insert.project_address6 = _projectaddress6
        insert.project_position6 = _projectposition6
        insert.start_project6 = _startproject6
        insert.end_project6 = _endproject6
        insert.ket_project6 = _ketproject6
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _update(self, _id, _npwp, _bpjstk, _bpjs, _aap1, _klasifikasi1, _ska1, _skastart1, _skaend1, _aap2, _klasifikasi2, _ska2, _skastart2, _skaend2, _aap3, _klasifikasi3, _ska3, _skastart3, _skaend3, _aap4, _klasifikasi4, _ska4, _skastart4, _skaend4, _aap5, _klasifikasi5, _ska5, _skastart5, _skaend5, _company1, _comaddress1, _workposition1, _starttime1, _endtime1, _ket1, _company2, _comaddress2, _workposition2, _starttime2, _endtime2, _ket2, _company3, _comaddress3, _workposition3, _starttime3, _endtime3, _ket3, _company4, _comaddress4, _workposition4, _starttime4, _endtime4, _ket4, _company5, _comaddress5, _workposition5, _starttime5, _endtime5, _ket5, _company6, _comaddress6, _workposition6, _starttime6, _endtime6, _ket6, _project1, _projectaddress1, _projectposition1, _startproject1, _endproject1, _ketproject1, _project2, _projectaddress2, _projectposition2, _startproject2, _endproject2, _ketproject2, _project3, _projectaddress3, _projectposition3, _startproject3, _endproject3, _ketproject3, _project4, _projectaddress4, _projectposition4, _startproject4, _endproject4, _ketproject4, _project5, _projectaddress5, _projectposition5, _startproject5, _endproject5, _ketproject5, _project6, _projectaddress6, _projectposition6, _startproject6, _endproject6, _ketproject6):
        update = job_experience()
        update = job_experience.query.filter_by(id=_id).first()
        update.npwp = _npwp
        update.bpjstk = _bpjstk
        update.bpjs = _bpjs
        update.aap1 = _aap1
        update.klasifikasi1 = _klasifikasi1
        update.ska1 = _ska1
        update.skastart1 = _skastart1
        update.skaend1 = _skaend1
        update.aap2 = _aap2
        update.klasifikasi2 = _klasifikasi2
        update.ska2 = _ska2
        update.skastart2 = _skastart2
        update.skaend2 = _skaend2
        update.aap3 = _aap3
        update.klasifikasi3 = _klasifikasi3
        update.ska3 = _ska3
        update.skastart3 = _skastart3
        update.skaend3 = _skaend3
        update.aap4 = _aap4
        update.klasifikasi4 = _klasifikasi4
        update.ska4 = _ska4
        update.skastart4 = _skastart4
        update.skaend4 = _skaend4
        update.aap5 = _aap5
        update.klasifikasi5 = _klasifikasi5
        update.ska5 = _ska5
        update.skastart5 = _skastart5
        update.skaend5 = _skaend5
        update.company1 = _company1
        update.comaddress1 = _comaddress1
        update.work_position1 = _workposition1
        update.starttime1 = _starttime1
        update.endtime1 = _endtime1
        update.ket1 = _ket1
        update.company2 = _company2
        update.comaddress2 = _comaddress2
        update.work_position2 = _workposition2
        update.starttime2 = _starttime2
        update.endtime2 = _endtime2
        update.ket2 = _ket2
        update.company3 = _company3
        update.comaddress3 = _comaddress3
        update.work_position3 = _workposition3
        update.starttime3 = _starttime3
        update.endtime3 = _endtime3
        update.ket3 = _ket3
        update.company4 = _company4
        update.comaddress4 = _comaddress4
        update.work_position4 = _workposition4
        update.starttime4 = _starttime4
        update.endtime4 = _endtime4
        update.ket4 = _ket4
        update.company5 = _company5
        update.comaddress5 = _comaddress5
        update.work_position5 = _workposition5
        update.starttime5 = _starttime5
        update.endtime5 = _endtime5
        update.ket5 = _ket5
        update.company6 = _company6
        update.comaddress6 = _comaddress6
        update.work_position6 = _workposition6
        update.starttime6 = _starttime6
        update.endtime6 = _endtime6
        update.ket6 = _ket6
        update.project1 = _project1
        update.project_address1 = _projectaddress1
        update.project_position1 = _projectposition1
        update.start_project1 = _startproject1
        update.end_project1 = _endproject1
        update.ket_project1 = _ketproject1
        update.project2 = _project2
        update.project_address2 = _projectaddress2
        update.project_position2 = _projectposition2
        update.start_project2 = _startproject2
        update.end_project2 = _endproject2
        update.ket_project2 = _ketproject2
        update.project3 = _project3
        update.project_address3 = _projectaddress3
        update.project_position3 = _projectposition3
        update.start_project3 = _startproject3
        update.end_project3 = _endproject3
        update.ket_project3 = _ketproject3
        update.project4 = _project4
        update.project_address4 = _projectaddress4
        update.project_position4 = _projectposition4
        update.start_project4 = _startproject4
        update.end_project4 = _endproject4
        update.ket_project4 = _ketproject4
        update.project5 = _project5
        update.project_address5 = _projectaddress5
        update.project_position5 = _projectposition5
        update.start_project5 = _startproject5
        update.end_project5 = _endproject5
        update.ket_project5 = _ketproject5
        update.project6 = _project6
        update.project_address6 = _projectaddress6
        update.project_position6 = _projectposition6
        update.start_project6 = _startproject6
        update.end_project6 = _endproject6
        update.ket_project6 = _ketproject6
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = job_experience()
        update = job_experience.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()


    def _list(self):
        response = {}
        response['data'] = []
        _job_experience = job_experience.query.filter_by(status = True).all()
        for i in _job_experience:
            response['data'].append({
                    'id' : i.id,
                    'user_id' : i.user_id,
                    'npwp' : i.npwp,
                    'bpjstk' : i.bpjstk,
                    'bpjs' : i.bpjs,
                    'aap1' : i.aap1,
                    'klasifikasi1' : i.klasifikasi1,
                    'ska1' : i.ska1,
                    'skastart1' : i.skastart1,
                    'skaend1' : i.skaend1,
                    'aap2' : i.aap2,
                    'klasifikasi2' : i.klasifikasi2,
                    'ska2' : i.ska2,
                    'skastart2' : i.skastart2,
                    'skaend2' : i.skaend2,
                    'aap3' : i.aap3,
                    'klasifikasi3' : i.klasifikasi3,
                    'ska3' : i.ska3,
                    'skastart3' : i.skastart3,
                    'skaend3' : i.skaend3,
                    'aap4' : i.aap4,
                    'klasifikasi4' : i.klasifikasi4,
                    'ska4' : i.ska4,
                    'skastart4' : i.skastart4,
                    'skaend4' : i.skaend4,
                    'aap5' : i.aap5,
                    'klasifikasi5' : i.klasifikasi5,
                    'ska5' : i.ska5,
                    'skastart5' : i.skastart5,
                    'skaend5' : i.skaend5,
                    'company1' : i.company1,
                    'comaddress1' : i.comaddress1,
                    'work_position1' : i.work_position1,
                    'starttime1' : i.starttime1,
                    'endtime1' : i.endtime1,
                    'ket1' : i.ket1,
                    'company2' : i.company2,
                    'comaddress2' : i.comaddress2,
                    'work_position2' : i.work_position2,
                    'starttime2' : i.starttime2,
                    'endtime2' : i.endtime2,
                    'ket2' : i.ket2,
                    'company3' : i.company3,
                    'comaddress3' : i.comaddress3,
                    'work_position3' : i.work_position3,
                    'starttime3' : i.starttime3,
                    'endtime3' : i.endtime3,
                    'ket3' : i.ket3,
                    'company4' : i.company4,
                    'comaddress4' : i.comaddress4,
                    'work_position4' : i.work_position4,
                    'starttime4' : i.starttime4,
                    'endtime4' : i.endtime4,
                    'ket4' : i.ket4,
                    'company5' : i.company5,
                    'comaddress5' : i.comaddress5,
                    'work_position5' : i.work_position5,
                    'starttime5' : i.starttime5,
                    'endtime5' : i.endtime5,
                    'ket5' : i.ket5,
                    'company6' : i.company6,
                    'comaddress6' : i.comaddress6,
                    'work_position6' : i.work_position6,
                    'starttime6' : i.starttime6,
                    'endtime6' : i.endtime6,
                    'ket6' : i.ket6,
                    'project1' : i.project1,
                    'project_address1' : i.project_address1,
                    'project_position1' : i.project_position1,
                    'start_project1' : i.start_project1,
                    'end_project1' : i.end_project1,
                    'ket_project1' : i.ket_project1,
                    'project2' : i.project2,
                    'project_address2' : i.project_address2,
                    'project_position2' : i.project_position2,
                    'start_project2' : i.start_project2,
                    'end_project2' : i.end_project2,
                    'ket_project2' : i.ket_project2,
                    'project3' : i.project3,
                    'project_address3' : i.project_address3,
                    'project_position3' : i.project_position3,
                    'start_project3' : i.start_project3,
                    'end_project3' : i.end_project3,
                    'ket_project3' : i.ket_project3,
                    'project4' : i.project4,
                    'project_address4' : i.project_address4,
                    'project_position4' : i.project_position4,
                    'start_project4' : i.start_project4,
                    'end_project4' : i.end_project4,
                    'ket_project4' : i.ket_project4,
                    'project5' : i.project5,
                    'project_address5' : i.project_address5,
                    'project_position5' : i.project_position5,
                    'start_project5' : i.start_project5,
                    'end_project5' : i.end_project5,
                    'ket_project5' : i.ket_project5,
                    'project6' : i.project6,
                    'project_address6' : i.project_address6,
                    'project_position6' : i.project_position6,
                    'start_project6' : i.start_project6,
                    'end_project6' : i.end_project6,
                    'ket_project6' : i.ket_project6
            })
        return response


    def _data(self, _userid):
        response = {}
        _job_experience = job_experience.query.filter_by(user_id = _userid, status = True).first()
        if _job_experience is not None:
                   response['id'] = _job_experience.id
                   response['user_id'] = _job_experience.user_id
                   response['npwp'] = _job_experience.npwp
                   response['bpjstk'] = _job_experience.bpjstk
                   response['bpjs'] = _job_experience.bpjs
                   response['aap1'] = _job_experience.aap1
                   response['klasifikasi1'] = _job_experience.klasifikasi1
                   response['ska1'] = _job_experience.ska1
                   response['skastart1'] = ifnull(_job_experience.skastart1)
                   response['skaend1'] = ifnull(_job_experience.skaend1)
                   response['aap2'] = _job_experience.aap2
                   response['klasifikasi2'] = _job_experience.klasifikasi2
                   response['ska2'] = _job_experience.ska2
                   response['skastart2'] = ifnull(_job_experience.skastart2)
                   response['skaend2'] = ifnull(_job_experience.skaend2)
                   response['aap3'] = _job_experience.aap3
                   response['klasifikasi3'] = _job_experience.klasifikasi3
                   response['ska3'] = _job_experience.ska3
                   response['skastart3'] = ifnull(_job_experience.skastart3)
                   response['skaend3'] = ifnull(_job_experience.skaend3)
                   response['aap4'] = _job_experience.aap4
                   response['klasifikasi4'] = _job_experience.klasifikasi4
                   response['ska4'] = _job_experience.ska4
                   response['skastart4'] = ifnull(_job_experience.skastart4)
                   response['skaend4'] = ifnull(_job_experience.skaend4)
                   response['aap5'] = _job_experience.aap5
                   response['klasifikasi5'] = _job_experience.klasifikasi5
                   response['ska5'] = _job_experience.ska5
                   response['skastart5'] = ifnull(_job_experience.skastart5)
                   response['skaend5'] = ifnull(_job_experience.skaend5)
                   response['company1'] = _job_experience.company1
                   response['comaddress1'] = _job_experience.comaddress1
                   response['work_position1'] = _job_experience.work_position1
                   response['starttime1'] = _job_experience.starttime1
                   response['endtime1'] = _job_experience.endtime1
                   response['ket1'] = _job_experience.ket1
                   response['company2'] = _job_experience.company2
                   response['comaddress2'] = _job_experience.comaddress2
                   response['work_position2'] = _job_experience.work_position2
                   response['starttime2'] = _job_experience.starttime2
                   response['endtime2'] = _job_experience.endtime2
                   response['ket2'] = _job_experience.ket2
                   response['company3'] = _job_experience.company3
                   response['comaddress3'] = _job_experience.comaddress3
                   response['work_position3'] = _job_experience.work_position3
                   response['starttime3'] = _job_experience.starttime3
                   response['endtime3'] = _job_experience.endtime3
                   response['ket3'] = _job_experience.ket3
                   response['company4'] = _job_experience.company4
                   response['comaddress4'] = _job_experience.comaddress4
                   response['work_position4'] = _job_experience.work_position4
                   response['starttime4'] = _job_experience.starttime4
                   response['endtime4'] = _job_experience.endtime4
                   response['ket4'] = _job_experience.ket4
                   response['company5'] = _job_experience.company5
                   response['comaddress5'] = _job_experience.comaddress5
                   response['work_position5'] = _job_experience.work_position5
                   response['starttime5'] = _job_experience.starttime5
                   response['endtime5'] = _job_experience.endtime5
                   response['ket5'] = _job_experience.ket5
                   response['company6'] = _job_experience.company6
                   response['comaddress6'] = _job_experience.comaddress6
                   response['work_position6'] = _job_experience.work_position6
                   response['starttime6'] = _job_experience.starttime6
                   response['endtime6'] = _job_experience.endtime6
                   response['ket6'] = _job_experience.ket6
                   response['project1'] = _job_experience.project1
                   response['project_address1'] = _job_experience.project_address1
                   response['project_position1'] = _job_experience.project_position1
                   response['start_project1'] = _job_experience.start_project1
                   response['end_project1'] = _job_experience.end_project1
                   response['ket_project1'] = _job_experience.ket_project1
                   response['project2'] = _job_experience.project2
                   response['project_address2'] = _job_experience.project_address2
                   response['project_position2'] = _job_experience.project_position2
                   response['start_project2'] = _job_experience.start_project2
                   response['end_project2'] = _job_experience.end_project2
                   response['ket_project2'] = _job_experience.ket_project2
                   response['project3'] = _job_experience.project3
                   response['project_address3'] = _job_experience.project_address3
                   response['project_position3'] = _job_experience.project_position3
                   response['start_project3'] = _job_experience.start_project3
                   response['end_project3'] = _job_experience.end_project3
                   response['ket_project3'] = _job_experience.ket_project3
                   response['project4'] = _job_experience.project4
                   response['project_address4'] = _job_experience.project_address4
                   response['project_position4'] = _job_experience.project_position4
                   response['start_project4'] = _job_experience.start_project4
                   response['end_project4'] = _job_experience.end_project4
                   response['ket_project4'] = _job_experience.ket_project4
                   response['project5'] = _job_experience.project5
                   response['project_address5'] = _job_experience.project_address5
                   response['project_position5'] = _job_experience.project_position5
                   response['start_project5'] = _job_experience.start_project5
                   response['end_project5'] = _job_experience.end_project5
                   response['ket_project5'] = _job_experience.ket_project5
                   response['project6'] = _job_experience.project6
                   response['project_address6'] = _job_experience.project_address6
                   response['project_position6'] = _job_experience.project_position6
                   response['start_project6'] = _job_experience.start_project6
                   response['end_project6'] = _job_experience.end_project6
                   response['ket_project6'] = _job_experience.ket_project6
        return response

class division(db.Model,UserMixin):
    __tablename__ = 'division'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _insert(self, _name):
        insert = division()
        insert.name = _name
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _update(self, _id, _name):
        update = division()
        update = division.query.filter_by(id = _id).first()
        update.name = _name
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = division()
        update = division.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _list(self):
        response = {}
        response['data'] = []
        _division = division.query.filter_by(status = True).all()
        for i in _division:
            response['data'].append({
                'id' : i.id,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _division = division.query.filter_by(id = _id, status = True).first()
        if _division is not None:
            response['id'] = _division.id
            response['name'] = _division.name
        return response

class jobtype(db.Model,UserMixin):
    __tablename__ = 'jobtype'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _list(self):
        response = {}
        response['data'] = []
        _jobtype = jobtype.query.filter_by(status = True).all()
        for i in _jobtype:
            response['data'].append({
                'id' : i.id,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _jobtype = jobtype.query.filter_by(id = _id, status = True).first()
        if _jobtype is not None:
            response['id'] = _jobtype.id
            response['name'] = _jobtype.name
        return response

class branch(db.Model, UserMixin):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    province_id = db.Column(db.Integer,db.ForeignKey('province.id'))
    city_id = db.Column(db.Integer,db.ForeignKey('city.id'))
    kecamatan_id = db.Column(db.Integer,db.ForeignKey('kecamatan.id'))
    kelurahan_id = db.Column(db.String(20),db.ForeignKey('kelurahan.id'))
    postal_code_id = db.Column(db.Integer,db.ForeignKey('postal_code.id'))
    rt = db.Column(db.String(4))
    rw = db.Column(db.String(4))
    add_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)

    def _insert(self, _name, _phonenumber, _email, _address, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw):
        insert = branch()
        insert.name = _name
        insert.phone_number = _phonenumber
        insert.email = _email
        insert.address = _address
        insert.province_id = _province
        insert.city_id = _city
        insert.kecamatan_id = _kecamatan
        insert.kelurahan_id = _kelurahan
        insert.postal_code_id = _postalcode
        insert.rt = _rt
        insert.rw = _rw
        insert.add_time = datetime.now()
        db.session.add(insert)
        db.session.commit()

    def _update(self, _id, _name, _phonenumber, _email, _address, _province, _city, _kecamatan, _kelurahan, _postalcode, _rt, _rw):
        update = branch()
        update = branch.query.filter_by(id = _id).first()
        update.name = _name
        update.phone_number = _phonenumber
        update.email = _email
        update.address = _address
        update.province_id = _province
        update.city_id = _city
        update.kecamatan_id = _kecamatan
        update.kelurahan_id = _kelurahan
        update.postal_code_id = _postalcode
        update.rt = _rt
        update.rw = _rw
        db.session.add(update)
        db.session.commit()

    def _remove(self, _id):
        update = branch()
        update = branch.query.filter_by(id = _id).first()
        update.status = False
        db.session.add(update)
        db.session.commit()

    def _data(self,_id):
        response = {}
        i = branch.query.filter_by(id = _id, status = True).first()
        if i is not None:
            response['id'] = i.id
            response['name'] = i.name
            response['phone_number'] = i.phone_number
            response['email'] = i.email
            response['address'] = i.address
            response['province_id'] = province()._data(i.province_id)
            response['city_id'] = city()._data(i.city_id)
            response['kecamatan_id'] = kecamatan()._data(i.kecamatan_id)
            response['kelurahan_id'] = kelurahan()._data(i.kelurahan_id)
            response['postal_code_id'] = postal_code()._data(i.postal_code_id)
            response['rt'] = i.rt
            response['rw'] = i.rw
        return response

    def _list(self):
        response = {}
        response['data'] = []
        _branch = branch.query.filter_by(status = True).all()
        for i in _branch:
            response['data'].append({
                'id' : i.id,
                'name' : i.name,
                'phone_number' : i.phone_number,
                'email' : i.email,
                'address' : i.address
            })
        return response

class experience(db.Model,UserMixin):
    __tablename__ = 'experience'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.Boolean,default=True)

    def _list(self):
        response = {}
        response['data'] = []
        _experience = experience.query.filter_by(status = True).all()
        for i in _experience:
            response['data'].append({
                'id' : i.id,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        _experience = experience.query.filter_by(id = _id, status = True).first()
        if _experience is not None:
            response['id'] = _experience.id
            response['name'] = _experience.name
        return response