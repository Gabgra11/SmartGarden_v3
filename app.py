"""
TODO: Add sensor/motor controls
TODO: Fill out readme.md setup
TODO: Implement live stream
"""

import config
import os
import sqlite3
from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, login_user, logout_user, current_user
from scripts import barchart, user, db

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('client_secret')
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id=None):
    conn = get_db_connection()

    return db.get_user_by_id(conn, user_id)

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row

    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    user_info = db.get_user_json_by_id(conn, current_user.get_id())

    return render_template(
        "index.html",
        data=db.get_page_data(conn),    # Get vote count, daily statistics
        user=user_info  # JSON with current user info
    )

@app.route("/stats")
def stats():
    conn = get_db_connection()
    moistJSON, humidJSON, tempJSON = barchart.get_week_stats_json(conn)
    user_info = db.get_user_json_by_id(conn, current_user.get_id())

    return render_template(
        "stats.html",
        moistJSON=moistJSON,
        humidJSON=humidJSON,
        tempJSON=tempJSON,
        data=db.get_page_data(conn),
        user = user_info
    )

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    conn = get_db_connection()
    current_vote = db.get_user_vote(conn, current_user.get_id())
    user_info = db.get_user_json_by_id(conn, current_user.get_id())

    if request.method == 'POST':
        user_id = request.form['user_id']
        vote = request.form['voteRadioOptions'] # Yes = 1; No = -1
        db.add_user_vote(conn, user_id, vote)
        current_vote = int(vote)
    
    return render_template(
        "vote.html",
        client_id = config.client_id,
        login_uri = config.login_uri,
        user = user_info,
        current_vote = current_vote, 
        data=db.get_page_data(conn)
    )

@app.route("/login", methods=["POST"])
def login():
    conn = get_db_connection()
    user_info = user.verify_token(request.form['credential'])
    login_user(user.User(user_info, conn))
    return redirect(url_for("vote"))

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/about")
def about():
    conn = get_db_connection()
    user_info = db.get_user_json_by_id(conn, current_user.get_id())

    return render_template(
        "about.html",
        data=db.get_page_data(conn),
        user = user_info
    )

@app.route("/live")
def live():
    conn = get_db_connection()
    user_info = db.get_user_json_by_id(conn, current_user.get_id())

    return render_template(
        "live.html",
        data=db.get_page_data(conn),
        user = user_info
    )

@app.route("/tos")
def tos():
    return render_template("tos.html")

@app.route("/policy")
def policy():
    return render_template("policy.html")

if __name__ == "__main__":
    app.run()