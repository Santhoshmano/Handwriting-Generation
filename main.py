from flask import Flask,request,render_template,redirect,session, url_for
from controller import MainController
from database_connector import dao
import smtplib
import twilio
from twilio.rest import Client

acc= "ACd55d51bf0ffb776dd46ff9cf6e0d5cd6"
token = 'b9f4fc3b69130ab082252801bb16b79c'
twilioClient = Client(acc,token)

app = Flask(__name__,static_url_path='')

smtpObj = smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.login('santhosh99mano@gmail.com','manosanthosh')

MainController.MainController(app, request, dao, render_template,redirect,url_for, session,smtpObj, twilioClient)

UPLOAD_FOLDER = 'datasets'
app.secret_key = '12344sefsrfsrg'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__=='__main__':
    app.run('localhost',debug=True)
