import re, pdb, string, random, os, requests, base64, datetime, hmac, hashlib, time
from datetime import datetime, date, timedelta
from os.path import join, dirname, realpath
from flask import Flask, flash, jsonify, send_file
from PIL import Image

apps = Flask(__name__)

def resize_files(_user_id, _image, _typeimage):
    response = {}
    PATH_FOLDER = join(dirname(realpath(__file__)), '../images')
    apps.config['PATH_FOLDER'] = PATH_FOLDER
    filename, filename_ext = os.path.splitext(_image.filename)
    allowed_img = set(['png', 'jpg', 'jpeg'])
    if filename_ext.rsplit('.', 1)[1].lower() in allowed_img:
        _filename = str(_user_id)+'-'+str(time.time()).replace('.', '')+filename_ext
        getImage = Image.open(_image)
        image_size = getImage.size
        width = int(image_size[0])
        height = int(image_size[1])
        while(width>1000 or height>1000):
            width = int(width/2)
            height = int(height/2)
        imgresize = getImage.resize((width, height), Image.ANTIALIAS)
        imgresize.save(os.path.join(apps.config['PATH_FOLDER'], _filename))
        response['allowed'] = 'Upload File Sukses'
        response['status'] = '00'
        response['path'] = PATH_FOLDER
        response['name'] = _filename
        response['image_id'] = _typeimage
    else :
        response['allowed'] = 'File tidak diizinkan'
        response['status'] = '60'
    return response

def resize_cv(_user_id, _image, _typeimage):
    response = {}
    PATH_FOLDER = join(dirname(realpath(__file__)), '../images')
    apps.config['PATH_FOLDER'] = PATH_FOLDER
    filename, filename_ext = os.path.splitext(_image.filename)
    file = _image
    allowed_img = set(['pdf'])
    if filename_ext.rsplit('.', 1)[1].lower() in allowed_img:
        _filename = str(_user_id)+'-'+str(time.time()).replace('.', '')+filename_ext
        file.save(os.path.join(apps.config['PATH_FOLDER'], _filename))
        response['allowed'] = 'Upload File Sukses'
        response['status'] = '00'
        response['path'] = PATH_FOLDER
        response['name'] = _filename
        response['image_id'] = _typeimage
    else :
        response['allowed'] = 'File tidak diizinkan'
        response['status'] = '60'
    return response

def show_image(_name):
    return send_file(_name, mimetype='../images/profile')

def hmac_sha256(key, msg):
    hash_obj = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    return hash_obj.hexdigest()

