from flask import Flask,g, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from decorator import login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'sup33rzz3cr3tzz'
db = SQLAlchemy(app)

from model import User

@app.before_request
def load_user():
    if session.get('user_id'):
        user = db.session.query(User).filter_by(id=session["user_id"]).first()
    else:
        user = None

    g.user = user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = db.session.query(User).filter_by(username=request.form['username']).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error = 'Wrong username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))    
    
@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    error = None
    if request.method == 'POST':
        user = db.session.query(User).filter_by(username=request.form['username']).first()
        if user:
            error = "User already exist"
        else:
            user = User(username=request.form['username'], name=request.form['name'], password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            return render_template('user_created.html', user=user)
    return render_template('create_user.html', error=error)