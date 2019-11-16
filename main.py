from flask import Flask, render_template, request, url_for, redirect
from forms import SignupForm, LoginForm, EditProfileForm, EditProfilesForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#Configuracion
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+os.environ.get('BD_USER')+':'+os.environ.get('BD_PASSWORD')+'@localhost:5432/'+os.environ.get('BD_NAME')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/signup", methods=["GET","POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User(email=form.email.data.lower(),
                    username=form.username.data)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or not next.startswith('/'):
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('auth/signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('home')
            return redirect(next)
    return render_template('auth/login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    users = User.query.all()
    return render_template('usuarios.html', users=users)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)

@app.route('/userDelete/<username>')
@login_required
def deleteUser(username):
    if current_user.username==username:
        logout_user()
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        return redirect(url_for('.user', username=current_user.username))
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('edit_profile.html', form=form, user=user)

@app.route('/edit-profiles/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profiles(id):
    user = User.query.get(id)
    form = EditProfilesForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    return render_template('edit_profile.html', form=form, user=user)