"""
TODO: Fill out readme.md
TODO: Fill out About tab.
TODO: Host website on github.io
TODO: Implement live, 7-day data storage. CSV? SQLite?
TODO: Implement live stream.
TODO: Decrease footer height.
TODO: Share header nav across all files. (Is this possible?)
"""

import config
from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager
login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/vote")
def vote():
    config_data = { 'client_id': config.client_id, 
                    'client_secret': config.client_secret, 
                    'login_uri': config.login_uri}
    return render_template("vote.html", data=config_data)

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

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return

if __name__ == "__main__":
    app.run()

