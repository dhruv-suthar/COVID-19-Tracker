from datetime import datetime
import requests
import os
from flask import Flask , render_template ,flash , redirect , url_for ,  request , abort ,jsonify , make_response , Response , session , Markup
from werkzeug.utils import secure_filename
from state_wise_data_scrapper import *
import pyrebase
from functools import wraps
from passlib.hash import sha256_crypt

app=Flask(__name__)

app.config.from_pyfile('config.py')

config = {

	"apiKey" : "AIzaSyBwGCVNG2FNxp3_F65w3xwLZXrdhzwFNbc",
    "authDomain" : "covid19-news-9d60d.firebaseapp.com",
    "databaseURL" : "https://covid19-news-9d60d.firebaseio.com",
    "projectId" : "covid19-news-9d60d",
    "storageBucket" : "covid19-news-9d60d.appspot.com",
    "messagingSenderId" : "555308724577",
    "appId" : "1:555308724577:web:aae407d096729b06265520",
    "measurementId" : "G-PRKXTP5PYZ"
}

firebase = pyrebase.initialize_app(config)

db= firebase.database()


from views import *

if __name__=='__main__':
	app.secret_key='any key'
	app.run(debug = True, threaded=True)

	
	