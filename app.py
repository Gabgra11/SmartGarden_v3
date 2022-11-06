"""
TODO: Fill out readme.md setup
TODO: Implement Google Authentication log-in
TODO: Host website on github.io
TODO: Implement live, 7-day data storage. CSV? SQLite?
TODO: Implement live stream.
TODO: Decrease footer height.
TODO: Share header/footer nav across all files. jinja blocks extends
TODO: Flesh out validate_login function
TODO: Implement log out
TODO: Pull stats data from db
TODO: Config parser
TODO: Hash load_user function, move to users.py
"""

import config
import user
import os
from flask import Flask, redirect, url_for, render_template, request
import jwt
from flask_login import LoginManager, login_user, current_user

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('client_secret')
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id=None):
    return user.User(user_id)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/vote")
def vote():
    return render_template(
        "vote.html",
        client_id = config.client_id,
        login_uri = config.login_uri,
        user_id = current_user.get_id()
    )

@app.route("/login", methods=["POST"])
def login():
    credential = jwt.decode(request.form['credential'], options={"verify_signature": False}, algorithms="RS256")
    login_user(user.User(credential["email"]))
    return redirect(url_for("vote"))

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

if __name__ == "__main__":
    app.run()

