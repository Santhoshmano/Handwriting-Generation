from .CreateUserController import CreateUserController
from .LoginController import LoginController
from .FrontEndController import FrontEndController
from itsdangerous import URLSafeTimedSerializer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from generate import gen
import random

def MainController(app, request, db, render_template, redirect, url_for, session,smtpObj, twilioClient):

    # front end routes
    FrontEndController(app, request, db, render_template, session)
    
    ###
    # back end routes
    ###

    @app.route('/createuser', methods=['POST'])
    def createUser():
        res = CreateUserController(request=request, db=db)
        if res=='ok':
            session['authenticated']=True
            session['user_name'] = request.form['user_name']
            session['email'] = request.form['email']
            session['confirmed'] = False
            confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

            token=confirm_serializer.dumps(session.get('email'), salt='email-confirmation-salt')
            confirm_url = 'http://localhost:5000/confirm_email?token=%s'%(token)
            html = render_template('confirmation_email_template.html',confirm_url=confirm_url)
            subject='confirm your computer jii account.'
            send_mail(session['email'],subject,html)
            return redirect('/')
        else:
            return redirect('/login_page?error=user_exist')
    
    @app.route('/resend_confirmation')
    def resend_confirmation():
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        token=confirm_serializer.dumps(session.get('email'), salt='email-confirmation-salt')
        confirm_url = 'http://localhost:5000/confirm_email?token=%s'%(token)
        html = render_template('confirmation_email_template.html',confirm_url=confirm_url)
        subject='confirm your computer jii account.'
        send_mail(session['email'],subject,html)
        return redirect('/')

    @app.route('/confirm_email')
    def confirm_mail():
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = request.args['token']
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        db.updateConfirmation(email)
        return redirect('/login_page?error=false')

    def send_mail(email,subject,html):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = 'santhosh99mano@gmail.com'
        msg['To'] = email
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        smtpObj.sendmail("santhosh99mano@gmail.com", email, msg.as_string()) 
        return

    @app.route('/verifyemailpassword',methods=['POST'])
    def verifyEmailPassword():
        email = request.form['email']
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        token=confirm_serializer.dumps(email, salt='email-confirmation-salt')
        confirm_url = 'http://localhost:5000/updatepassword_page?token=%s'%(token)
        html = render_template('confirmation_email_template.html',confirm_url=confirm_url)
        subject = 'change password for computer jii account.'
        send_mail(email,subject, html)
        
        return redirect('/')


    @app.route("/updatepassword",methods=['POST'])
    def updatePassword():
        email = request.form['email']
        password = request.form['password']
        if db.updatePassword(email,password)=='user not confirmed':
            return redirect('/dashboard_page')
        else:
            return redirect('/login_page?error=false')


    @app.route('/login', methods=['POST'])
    def login():
        res=LoginController(request=request, db=db)
        if res=='password confirmed':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            session['role'] = 'user'
            session['confirmed']=True
            return redirect('/')
        elif res=='password match':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            session['role'] = 'user'
            session['confirmed']=False
            return redirect('/')
        elif res=='password admin':
            session['authenticated']=True
            session['user_name'] = db.getUserNameByEmail(request.form['email'])
            session['email'] = request.form['email']
            session['role'] = 'admin'
            session['confirmed']=True
            return redirect('/')
        elif res=='user not exist':
            return redirect('/register_page?error=true')
        else:
            return redirect('/login_page?error=true')

    @app.route('/logout')
    def logout():
        session['authenticated']=False
        return redirect('/')    

    @app.route('/result', methods = ['POST'])
    def result():
        text = request.form["gen_text"]
        style = request.form.get('style', 404)
        bias = request.form.get('bias', 1.0)
        print("The text from user is: " + text)
        print("Generating..")
        gen(text, style, bias)
        print("Genrated and the File is saved")
        email = request.form['email']
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        token=confirm_serializer.dumps(email, salt='email-confirmation-salt')
        confirm_url = 'http://localhost:5000/result_page?token=%s'%(token)
        html = render_template('confirmation_result_template.html',confirm_url=confirm_url)
        subject = 'Your Handwriting is Selected for generation'
        send_mail(email,subject, html)
        otp=random.randint(1000,9000)
        msg = twilioClient.messages.create(
            body="Your OTP is - "+str(otp),
            from_='+12568500359',
            to='+917904385351'
        )
        return render_template('otp.html', otp = otp)