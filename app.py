from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/cleysonph/workspaces/flask/hydra_atack/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    def __init__(self, username, password):
        self.username = username
        self.password = password


    def __repr__(self):
        return '<User {}>'.format(self.username)


    def check_password(self, password):
        return self.password == password


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')
    user = User.query.filter_by(username=request.form.get('username')).first()
    if user is not None and user.check_password(request.form.get('password')):
        login_user(user)

        return redirect(url_for('welcome'))
    return 'Bad Login'



@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', title='Welcome')
