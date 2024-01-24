from flask import Flask , render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from powerbiclient import models, Report

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf=CSRFProtect()

db = MySQL(app)

login_manager_app= LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user=User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db,user)    
        #print(logged_user.id)
        #print(logged_user.username)
        #print(logged_user.password)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid Password...")  
                return render_template('auth/login.html')
            
        else:
            flash("User no found...")  
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/protected')
@login_required 
def protected():
    return "<h1>Esta es una vista para usuarios autentificados </h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada </h1>",404


@app.route('/dashboard')
def dashboard():
    group_id = '942201c6-5600-4bd7-a841-5fbc9a767a4a'
    report_id = '4259572e-0078-4768-9ca2-53ac89ddc48c'
    base_url = 'https://api.powerbi.com'
    access_token = 'TU_TOKEN_DE_ACCESO'

    report = Report(group_id, report_id, base_url, access_token)
    embed_url = report.get_embed_url()
     
    return render_template('dashboard.html',embed_url=embed_url)




if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)

    app.run()