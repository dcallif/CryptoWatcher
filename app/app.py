import datetime

import flask
import flask_login
import base64
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from models import Schema
from service import CryptoWatcherService, UserService
from flask_login import LoginManager, login_required, current_user

login_manager = LoginManager()
login_manager.login_view = 'login'
app = Flask(__name__, template_folder='../templates', static_folder='../static')
# app = Flask(__name__, template_folder='/home/qy8fou0m88j5/CryptoWatcher/templates',
# static_folder='/home/qy8fou0m88j5/CryptoWatcher/static')

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watcher.db'
app.config['REMEMBER_COOKIE_NAME'] = app.config.get('remember_cookie_name')
app.REMEMBER_COOKIE_DURATION = datetime.timedelta(minutes=60)
app.PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=60)

login_manager.init_app(app)
Schema()


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, " \
                                                       "X-Requested-With "
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    flask.session.modified = True
    g.user = current_user


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = UserService().get_by_email(email)
        if user is None:
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))  # if user doesn't exist
        session["user_dbId"] = user['id']
        user_obj = User()
        user_obj.id = user['email']
        user_obj.name = user['name']
        user_obj.dbId = user['id']

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user['password'], password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right creds
        flask_login.login_user(user_obj)
        return render_template('profile.html', name=current_user.name, email=user['email'])


@app.route('/logout')
@login_required
def logout():
    session["user_dbId"] = ""
    flask_login.logout_user()
    res = flask.make_response("Deleting cookie")
    res.set_cookie('', max_age=0)
    current_user.logged_in = False

    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        # code to validate and add user to database goes here
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if email == '':
            flash('Please enter a valid email and try again.')
            return redirect(url_for('signup'))
        if name == '':
            flash('Please enter a name and try again.')
            return render_template('signup.html', email=email)
            # return redirect(url_for('signup'))
        if password == '':
            flash('Please enter a password and try again.')
            return render_template('signup.html', email=email, name=name)
            # return redirect(url_for('signup'))

        # Need to query to see if user exists
        user = UserService().get_by_email(email)
        if user:
            flash('User already exists...please try with a different email.')
            return redirect(url_for('signup'))
        else:
            UserService().create(email, name, generate_password_hash(password, method='sha256'))
            # Need to query to see if user exists
            user_created = UserService().get_by_id(request.form.get('email'))
            if user_created:
                flash('Successfully created user!')
                return redirect(url_for('login'))


@app.route('/users', methods=['GET'])
def get_users():
    if len(current_user.__dict__) == 0:
        flash('Missing or Invalid Auth header.')
        return render_template('login.html')
    if current_user.id == 'dcallif22@gmail.com':
        return jsonify(UserService().list())
    else:
        return render_template('home.html')


@app.route("/tokens")
@flask_login.login_required
def tokens():
    # print(f"Tokens user id: {current_user.id}, dbId: {current_user.dbId}")
    if current_user is not None:
        return render_template("crypto.html", user_email=current_user.id)
    flash('Please login before accessing crypto page.')
    return render_template("login.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/list-tokens", methods=["GET"])
def list_tokens():
    if len(current_user.__dict__) == 0:
        flash('Try logging in or adding an Auth header if calling API.')
        # return render_template('login.html')
        return jsonify("Invalid auth.")
    print(f"List-tokens user id: {current_user.id}, dbId: {current_user.dbId}")
    if session.get("user_dbId") is not None:
        return jsonify(CryptoWatcherService().list(current_user.dbId))
    else:
        return jsonify("Invalid auth.")


@app.route("/token", methods=["POST"])
def create_token():
    return jsonify(CryptoWatcherService().create(request.get_json()))


@app.route("/token/<token_id>", methods=["PUT"])
def update_item(token_id):
    # print(token_id)
    # print(request.get_json())
    flash("Not implemented yet")
    return render_template("crypto.html")
    # return jsonify(CryptoWatcherService().update(token_id, request.get_json()))


@app.route("/token/<token_id>", methods=["DELETE"])
def delete_item(token_id):
    return jsonify(CryptoWatcherService().delete(token_id, request.get_json()))


@app.route('/profile')
@flask_login.login_required
def profile():
    if current_user is not None:
        user = UserService().get_by_email(current_user.id)
        return render_template('profile.html', name=user['name'], email=user['email'])
    flash('Please login before accessing profile page.')
    return render_template('login.html')


class User(flask_login.UserMixin):
    username = None
    dbId = None

    def get_id(self):
        return self.id

    def __init__(self):
        self.id = None
        self.username = None
        self.dbId = None
    pass


@login_manager.user_loader
def load_user(user_id):
    u = UserService().get_by_email(user_id)
    session["user_dbId"] = u['id']

    user = User()
    user.id = user_id
    user.dbId = u['id']
    user.username = u['email']
    user.name = u['name']
    return user


@login_manager.request_loader
def request_loader(request):
    auth_str = request.headers.get('Authorization')
    token = auth_str.split(' ')[1] if auth_str else ''

    if not token:
        return None

    user_name = base64.b64decode(token).decode('UTF-8').split(':')[0]
    pass_w = base64.b64decode(token).decode('UTF-8').split(':')[1]
    u = UserService().get_by_email(user_name)

    if u is None:
        return None
    if not check_password_hash(u['password'], pass_w):
        flash("Invalid authorization.", "danger")
        return None
    if u:
        session["user_dbId"] = u['id']
        user_obj = User()
        user_obj.id = int(u['id'])
        user_obj.dbId = u['id']
        user_obj.username = u['email']
        user_obj.name = u['name']
        return user_obj
    return None


if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='127.0.0.1', port=8888)
