"""
TODO: Fill out readme.md setup
TODO: Fill out About tab.
TODO: Implement Google Authentication log-in
TODO: Host website on github.io
TODO: Implement live, 7-day data storage. CSV? SQLite?
TODO: Implement live stream.
TODO: Decrease footer height.
TODO: Share header/footer nav across all files. (Is this possible?)
TODO: Flesh out validate_login function
"""

import config
import user
import sqlite3
import os
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_login import LoginManager, login_user, current_user

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('client_secret')
login_manager.init_app(app)

# Initialize connection to SQLite3 db:
con = sqlite3.connect("vote2grow.db")
cur = con.cursor()

@login_manager.user_loader
def load_user(user_id=None):
    # res = cur.execute("SELECT user_id FROM Users WHERE user_id == " + user_id)
    curr_user_id = user_id
    return user.User(user_id)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/login")
def login():
    config_data = { 'client_id': config.client_id, 
                    'login_uri': config.login_uri}
    return render_template("login.html", data=config_data)

@app.route("/vote")
def vote(): # Default to anonymous user
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template("vote.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/live")
def live():
    return render_template("live.html")

@app.route("/tos")
def tos():
    return render_template("tos.html")

@app.route("/policy")
def policy():
    return render_template("policy.html")

@app.route('/loginhandler', methods=['POST'])
def loginhandler():
    # Parse the data passed in from Google Sign In:
    request_data = request.get_data(as_text=True).split("&")
    request_data = clean_request_data(request_data)

    if (not validate_login(request_data)):
        print("Error Validating Login")
        # Do something, redirect to fail page?
        return redirect(url_for('login'))
    else:
        curr_user = load_user(request_data[0])
        login_user(curr_user, remember=True)
        return redirect(url_for('vote'))

def validate_login(request_data):
    if (len(request_data) == 2):
        return True

# Trim each data element such that everything before and including "=" is removed
def clean_request_data(request_data):
    for i in range(len(request_data)):
        request_data[i] = request_data[i][request_data[i].find("=")+1:]
    return request_data


if __name__ == "__main__":
    app.run()

