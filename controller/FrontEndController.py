from itsdangerous import URLSafeTimedSerializer

def FrontEndController(app, request, db, render_template, session):
    
    @app.route('/')
    def Hello():
        if not session.get('authenticated'):
            return render_template('index.html',user_name=None)
        return render_template('index.html',user_name=session['user_name'])
    
    @app.route('/login_page')
    def Login_page():
        if request.args['error']=='password':
            return render_template('login.html',error='password')
        elif request.args['error']=='user_exist':
            return render_template('login.html',error='user_exist')
        return render_template('login.html')

    @app.route('/register_page')
    def Register_page():
        if request.args['error']=='true':
            return render_template('register.html',error='error')
        return render_template('register.html')
     
        
    @app.route('/handwriting_page')
    def handwriting_page():
        return render_template('handwriting.html')
    
    @app.route('/verify_otp', methods = ['POST'])
    def otp_page():
        if request.form['user_otp'] == request.form['actual_otp']:
            data='results/result.png'
            return render_template('result.html', data=data)
        return 'unauthorized'

    @app.route('/result_page')
    def result_page():
        data='results/result.png'
        return render_template('result.html', data=data)
    
    @app.route('/addtrainablemodel_page')
    def addTrainableModel_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        elif not session.get('role')=='admin':
            return render_template('index.html')
        return render_template('addtrainablemodel.html')
    
    @app.route('/addnontrainablemodel_page')
    def addNonTrainableModel_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        elif not session.get('role')=='admin':
            return render_template('404.html')
        return render_template('addnontrainablemodel.html')

    @app.route('/admin_dashboard')
    def adminDashboard_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        elif not session.get('role')=='admin':
            return render_template('404.html')
        return render_template('admin_dashboard.html')

    @app.route('/dashboard_page')
    def dashboard_page():
        if not session.get('authenticated'):
            return render_template('login.html')
        if not session.get('confirmed'):
            return render_template('unconfirmed_dashboard.html')
        user = db.getUserByEmail(session['email'])
        models = db.getModelUserCountDetails(session['email'])
        request_models  = db.getModelUserRequestDetails(session['email'])
        api = db.getModelUserApiDetails(session['email'])
        model_desc = db.getAllTrainableModelDescription()
        datasets = db.getDatasetsByEmail(session['email'])
        return render_template('dashboard.html',user=user,datasets=datasets,model_desc=model_desc,api=api,hostname='localhost:5000',models=models,request=request_models)
    
    @app.route('/updatepassword_page')
    def updatePassword_page():
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = request.args['token']
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        return render_template('update_password.html',email=email)

    @app.route('/verifyemailpassword_page')
    def verifyEmailPassword_page():
        return render_template('verifyemailpassword.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')
    
    @app.errorhandler(405)
    def page_not_found(e):
        return render_template('404.html')
    
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('404.html')