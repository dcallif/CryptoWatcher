from flask import Flask, render_template, request, jsonify, Blueprint

from models import Schema
from service import CryptoWatcherService

app = Flask(__name__, template_folder='../templates', static_folder='../static')


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
def profile():
    return render_template('profile.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='127.0.0.1', port=8888)

