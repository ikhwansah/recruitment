from flask import render_template,request,Blueprint, jsonify, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from app.models import *
from .. import app
import json, os
from ..utils import resize_files, show_image

core = Blueprint('core',__name__)

@core.route('/listuser',methods=['GET','POST'])   
def listuser():
    if request.method == 'POST':
        respon = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            respon = User()._list()
            return jsonify(respon)
    return render_template('/error_pages/403.html')

@core.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method == "POST":
        respon = {}
        respon['response'] = ''
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        checkphonenumber = User.query.filter_by(phone_number = apidata['phonenumber']).first()
        checkemail = User.query.filter_by(email = apidata['email']).first()
        checkpegawaipin = pegawai.query.filter_by(pegawai_pin = apidata['pegawaipin'])
        if user.verify_token(apidata['token']):
            if checkemail is None:
                if checkphonenumber is None:
                    if checkpegawaipin is None:
                        User()._insert(apidata['name'], apidata['phonenumber'], 'cpipassword!', '123456', apidata['email'], apidata['birthdate'], apidata['birthplace'], apidata['address'], apidata['gender'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['client_id'])
                        user_id = User.query.filter_by(phone_number = apidata['phonenumber']).first()
                        pegawai()._insert(user_id, apidata['pegawaipin'], apidata['name'])
                        respon['response'] = 'Registrasi Berhasil!!'
                    else :
                        respon['response'] = 'ID Pegawai Pin sudah di pakai.'
                else:
                    respon['response'] = 'Phone Number sudah di pakai'
            else:
                respon['response'] = 'Email sudah di pakai'
        return jsonify(respon)
    return render_template('/error_pages/403.html')

@core.route('/updateemployee',methods=['GET','POST'])
def updateuser():
    if request.method == "POST":
        respon = {}
        apidata = request.form
        check = User.query.filter_by(id = apidata['id']).first()
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            if check is not None:
                    User()._update(apidata['id'], apidata['name'], apidata['email'], apidata['birthdate'], apidata['birthplace'], apidata['address'], apidata['gender'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['client_id'])
                    respon['response'] = 'Registrasi Berhasil!!'
            else:
                respon['response'] = 'User tidak terdaftar'
        return jsonify(respon)    
    return render_template('/error_pages/403.html')

@core.route('/removeuser',methods=['GET','POST']) #hapususer
def removeuser():
    if request.method == "POST":
        respon = {}
        respon['response'] = ''
        apidata = request.form
        check = User.query.filter_by(id = apidata['id']).first()
        user = User.query.filter_by(id=request.form['cur_user']).first()
        if user.verify_token(apidata['token']):
            if check is not None:
                User()._remove(apidata['id'])
                respon['response'] = 'Berhasil'
            else:
                respon['response'] = 'User tidak terdaftar'
        return jsonify(respon)
    return render_template('/error_pages/403.html')

@core.route('/updatepassword',methods=['GET','POST']) #updatepassword
def updatepassword():
    if request.method == "POST":
        respon = {}
        respon['response'] = ''
        apidata = request.form
        checkemail = User.query.filter_by(id = apidata['id']).first()
        user = User.query.filter_by(id=request.form['cur_user']).first()
        if user.verify_token(apidata['token']):
            if checkemail is not None:
                if checkemail.check_password(apidata['passwordlama']):
                    User()._updatepassword(apidata['id'],apidata['passwordbaru'])
                    respon['response'] = 'Registrasi Berhasil!!'
                else :
                    respon['response'] = 'Password Lama salah'
            else:
                respon['response'] = 'User tidak terdaftar'
        return jsonify(respon)    
    return render_template('/error_pages/403.html')

@core.route('/addidentity',methods=['GET','POST'])
def addIdentity():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        response['status'] = 'Identity sudah pernah di input!'
        cekIdentity = Identity().query.filter_by(nik = apidata['nik']).first()
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            if cekIdentity is None:
                Identity()._insert(apidata['userid'], apidata['nik'], apidata['filename'])
                response['status'] = "Berhasil!"
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updateidentity',methods=['GET','POST'])
def updateIdentity():
    if request.method == 'POST':
        response = {}
        apidata= request.form
        cekIdentity = Identity().query.filter_by(id = apidata['id']).first()
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            if cekIdentity is not None:
                Identity()._update(apidata['id'], apidata['nik'], apidata['filename'])
                response['status'] = "Berhasil!"
            else:
                response['status'] = 'Identity tidak ditemukan!'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/dataidentity',methods=['GET','POST'])
def dataIdentity():
    if request.method == 'POST':
        response = {}
        apidata= request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response['data']= Identity()._data(apidata['userid'])
            response['status'] = "Berhasil!"
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addkores',methods=['GET','POST'])
def addkores():
    if request.method == 'POST':
        response = {}
        apidata= request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response['status'] = 'Gagal!'
            corespondend_address()._insert(apidata['alamat'], apidata['province'], apidata['city'], apidata['kecamatan'],apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'], apidata['userid'], apidata['statusaddress'])
            response['status'] = "Berhasil!"
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatekores',methods=['GET','POST'])
def updatekores():
    if request.method == 'POST':
        response = {}
        apidata= request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            corespondend_address()._update(apidata['alamat'],apidata['province'], apidata['city'], apidata['kecamatan'],apidata['kelurahan'], apidata['postalcode'],apidata['rt'],apidata['rw'],apidata['id'], apidata['statusaddress'])
            response['status'] = "Berhasil!"
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datakores',methods=['GET','POST'])
def datakores():
    if request.method == 'POST':
        response = {}
        apidata= request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response['data']= corespondend_address()._data(apidata['userid'])
            response['status'] = "Berhasil!"
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addlevel',methods=['GET','POST'])
def addlevel():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            level()._insert(apidata['name'], apidata['aselon'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatelevel',methods=['GET','POST'])
def updatelevel():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            level()._update(apidata['id'], apidata['name'], apidata['aselon'])
            response['reponse'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removelevel',methods=['GET','POST'])
def removelevel():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            level()._remove(apidata['id'])
            response['reponse'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listlevel',methods=['GET','POST'])
def listlevel():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = level()._list()
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/adddivision',methods=['GET','POST'])
def adddivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            division()._insert(apidata['userid'], apidata['levelid'])
            response['response'] = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatedivision', methods = ['GET','POST'])
def updatedivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            division()._update(apidata['id'], apidata['userid'], apidata['levelid'])
            response['reponse'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removedivision', methods = ['GET','POST'])
def removedivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            division()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listdivision',methods=['GET','POST'])
def listdivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = division()._list()
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datadivision',methods=['GET','POST'])
def datadivision():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = division()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')
    
@core.route('/addaselon', methods = ['POST', 'GET'])
def addaselon():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            aselon()._insert(apidata['name'], apidata['minsalary'], apidata['maxsalary'], apidata['minovertime'], apidata['maxovertime'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updateaselon', methods = ['GET', 'POST'])
def updateaselon():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            aselon()._update(apidata['id'], apidata['name'], apidata['minsalary'], apidata['maxsalary'], apidata['minovertime'], apidata['maxovertime'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removeaselon', methods = ['GET', 'POST'])
def removeaselon():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            aselon()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listaselon', methods = ['POST', 'GET'])
def listaselon():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = aselon()._list()
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addhrfile', methods = ['GET', 'POST'])
def addhrfile():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            hr_file()._insert(apidata['hr_general_perm_id'], apidata['filename'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatehrfile', methods = ['GET', 'POST'])
def updatehrfile():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            hr_file()._update(apidata['id'], apidata['hr_general_perm_id'], apidata['filename'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removehrfile', methods = ['GET', 'POST'])
def removehrfile():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            hr_file()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listhrfile', methods = ['GET', 'POST'])
def listhrfile():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = hr_file()._list()
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datahrfile', methods = ['GET', 'POST'])
def datahrfile():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = hr_file()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addhrtype', methods = ['GET', 'POST'])
def addhrtype():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            hr_type()._insert(apidata['name'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatehrtype', methods = ['GET', 'POST'])
def updatehrtype():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            hr_type()._update(apidata['id'], apidata['name'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removehrtype', methods = ['GET', 'POST'])
def removehrtype():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            hr_type()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listhrtype', methods = ['GET', 'POST'])
def listhrtype():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = hr_type()._list()
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datahrtype', methods = ['GET', 'POST'])
def datahrtype():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = hr_type()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addposition', methods = ['GET', 'POST'])
def addposition():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            position()._insert(apidata['name'], apidata['user_id'], apidata['division_id'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updateposition', methods = ['GET', 'POST'])
def updateposition():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            position()._update(apidata['id'], apidata['name'], apidata['user_id'], apidata['division_id'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removeposition', methods = ['GET', 'POST'])
def removeposition():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            position()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/dataposition', methods = ['GET', 'POST'])
def dataposition():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = position()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addpostalcode', methods = ['GET', 'POST'])
def addpostalcode():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            check = postal_code.query.filter_by(name = apidata['name']).first()
            if check is None:
                postal_code()._insert(apidata['name'], apidata['kecamatan_id'])
                response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatepostalcode', methods = ['GET', 'POST'])
def updatepostalcode():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            postal_code()._update(apidata['id'], apidata['name'], apidata['kecamatan_id'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removepostalcode', methods = ['GET', 'POST'])
def removepostalcode():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            postal_code()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listpostalcode', methods = ['GET', 'POST'])
def listpostalcode():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = postal_code()._list()
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datapostalcode', methods = ['GET', 'POST'])
def datapostalcode():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = postal_code()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listclient',methods=['GET','POST'])     
def listclients():
    if request.method == 'POST':
        respon = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            respon = clients()._list()
            return jsonify(respon)
    return render_template('/error_pages/403.html')

@core.route('/addclients',methods=['GET','POST']) 
def addclients():
    if request.method == "POST":
        respon = {}
        respon['response'] = ''
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        checkphonenumber = clients.query.filter_by(phone_number = apidata['phonenumber']).first()
        checkemail = clients.query.filter_by(email = apidata['email']).first()
        if user.verify_token(apidata['token']):
            if checkemail is None:
                if checkphonenumber is None:
                    clients()._insert(apidata['name'], apidata['phonenumber'], 'cpipassword!', '123456', apidata['email'], apidata['address'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'])
                    respon['response'] = 'Registrasi Berhasil!!'
                else:
                    respon['response'] = 'Phone Number sudah di pakai!!'
            else:
                respon['response'] = 'Email sudah di pakai!!'
        return jsonify(respon)
    return render_template('/error_pages/403.html')

@core.route('/updateclients',methods=['GET','POST'])
def updateclients():
    if request.method == "POST":
        respon = {}
        apidata = request.form
        check = clients.query.filter_by(id = apidata['id']).first()
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            if check is not None:
                    clients()._update(apidata['id'], apidata['name'], apidata['email'], apidata['address'], apidata['province'], apidata['city'], apidata['kecamatan'], apidata['kelurahan'], apidata['postalcode'], apidata['rt'], apidata['rw'])
                    respon['response'] = 'Update Berhasil!!'
            else:
                respon['response'] = 'clients tidak terdaftar'
        return jsonify(respon)    
    return render_template('/error_pages/403.html')

@core.route('/removeclients',methods=['GET','POST'])
def removeclients():
    if request.method == "POST":
        respon = {}
        respon['response'] = ''
        apidata = request.form
        check = clients.query.filter_by(id = apidata['id']).first()
        user = User.query.filter_by(id=request.form['cur_user']).first()
        if user.verify_token(apidata['token']):
            if check is not None:
                clients()._remove(apidata['id'])
                respon['response'] = 'Berhasil'
            else:
                respon['response'] = 'clients tidak terdaftar'
        return jsonify(respon)
    return render_template('/error_pages/403.html')

@core.route('/addcontractclient', methods = ['GET', 'POST'])
def addcontractclient():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                contract_client()._insert(apidata['client_id'], apidata['position_id'], apidata['start_time'], apidata['end_time'])
                response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatecontractclient', methods = ['GET', 'POST'])
def updatecontractclient():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            contract_client()._update(apidata['id'], apidata['client_id'], apidata['position_id'], apidata['start_time'], apidata['end_time'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removecontractclient', methods = ['GET', 'POST'])
def removecontractclient():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            contract_client()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listcontractclient', methods = ['GET', 'POST'])
def listcontractclient():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = contract_client()._list()
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datacontractclient', methods = ['GET', 'POST'])
def datacontractclient():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = contract_client()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/addcontractuser', methods = ['GET', 'POST'])
def addcontractuser():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
                contract_user()._insert(apidata['user_id'], apidata['start_time'], apidata['end_time'])
                response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/updatecontractuser', methods = ['GET', 'POST'])
def updatecontractuser():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            contract_user()._update(apidata['id'], apidata['user_id'], apidata['start_time'], apidata['end_time'])
            response = 'Berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/removecontractuser', methods = ['GET', 'POST'])
def removecontractuser():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            contract_user()._remove(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listcontractuser', methods = ['GET', 'POST'])
def listcontractuser():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = contract_user()._list()
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/datacontractuser', methods = ['GET', 'POST'])
def datacontractuser():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = contract_user()._data(apidata['id'])
            response['response'] = 'berhasil'
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/dashboard',methods = ['GET' , 'POST'])
def dashboard():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response['hr_general_perm'] = hr_general_perm()._list(user.client_id)
            response['presence'] = attendance()._presencelog(user.client_id)
            response['employee'] = User()._countuser()
            response['countpresence'] = attendance()._countpresencelog()
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listemployee',methods = ['GET' , 'POST'])
def listemployee():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response = User()._employee(user.client_id)
        return jsonify(response)
    return render_template('/error_pages/403.html')

@core.route('/listposition',methods = ['GET' , 'POST'])
def listposition():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        user = User.query.filter_by(id=apidata['cur_user']).first()
        if user.verify_token(apidata['token']):
            response['aselon'] = aselon()._list()
            response['division'] = division()._list()
            response['level'] = level()._list()
            response['position'] = position()._list()
        return jsonify(response)
    return render_template('/error_pages/403.html')
    
@core.route('/store_image_identity', methods=['GET', 'POST'])
def _store_image_identity():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        apifile = request.files
        cur_user = User.query.filter_by(id=apidata['cur_user'], status=True).first()
        if cur_user.verify_token(apidata['token']):
            stored_file = resize_files(cur_user.id, apifile['imgfile'], int(apidata['typeimage']))
            if stored_file['status'] == '00':
                Image_Service()._insert(stored_file['name'], cur_user.id, stored_file['image_id'])
            response = stored_file
        else:
            response['status'] = '50'
            response['message'] = 'User tidak terverifikasi.'
        return jsonify(response)
    return render_template('/error_pages/403.html')

MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'images')

@core.route('/images/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
   return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)
