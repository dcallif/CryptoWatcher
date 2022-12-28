import flask_login
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import Schema
from service import CryptoWatcherService, UserService
from flask_login import LoginManager, login_required, current_user, login_user

login_manager = LoginManager()
app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watcher.db'

login_manager.init_app(app)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, " \
                                                       "X-Requested-With "
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tokens")
def tokens():
    return render_template("crypto.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/list-tokens", methods=["GET"])
def list_tokens():
    return jsonify(CryptoWatcherService().list())


@app.route("/token", methods=["POST"])
def create_token():
    print(request)
    return jsonify(CryptoWatcherService().create(request.get_json()))


@app.route("/token/<token_id>", methods=["PUT"])
def update_item(token_id):
    return jsonify(CryptoWatcherService().update(token_id, request.get_json()))


@app.route("/token/<token_id>", methods=["DELETE"])
def delete_item(token_id):
    return jsonify(CryptoWatcherService().delete(token_id))


@app.route('/profile')
def profile(name):
    return render_template('profile.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = UserService().get_by_email(email)
        # user_obj = {user['email']: {'password': user['password']}}
        if user is None:
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page
        user_obj = User()
        user_obj.id = user['email']
        print(f'Successfully generated user from db: {user_obj}')
        # print(user.keys())
        # print(user['name'])

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        # if not user or not check_password_hash(user.password, password):
        if not user or not check_password_hash(user['password'], password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right creds
        # login_user(user_obj, remember=remember, force=True)
        flask_login.login_user(user_obj)
        return render_template('profile.html', name=user['email'])


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
            flash('User already exists...please try with a different email')
            return redirect(url_for('signup'))
        else:
            UserService().create(email, name, generate_password_hash(password, method='sha256'))
            # Need to query to see if user exists
            user_created = UserService().get_by_id(request.form.get('email'))
            if user_created:
                flash('Successfully created user!')
                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    # print(''.join(user_id[1]))
    return UserService().get_by_id(''.join(user_id[1]))


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')

    user = User()
    user.id = email
    return user


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(UserService().list())


if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='127.0.0.1', port=8888)
