"""
TODO: Fix formatting on vote page.
TODO: Verify token in /login https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
TODO: Fill out readme.md setup
TODO: Implement live stream.
TODO: Decrease footer height.
TODO: Config parser
TODO: Hash load_user function (?), move to users.py
"""

import config
import datetime as dt
import scripts.user as user
import scripts.barchart as bc
import scripts.db as db
import os
import sqlite3
from flask import Flask, redirect, url_for, render_template, request
import jwt
from flask_login import LoginManager, login_user, logout_user, current_user

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('client_secret')
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id=None):
    return user.User(user_id)

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    return render_template("index.html", data=db.get_page_data(conn))

@app.route("/stats")
def stats():
    conn = get_db_connection()

    df = db.get_data_week_df(conn, dt.datetime.now() - dt.timedelta(days=7))
    x = [dt.datetime.fromtimestamp(date).strftime("%a, %b %d") for date in df['timestamp']]
    moist_y = df['moisture'].values.tolist()
    humid_y = df['humidity'].values.tolist()
    temp_y = df['temperature'].values.tolist()

    moistJSON = bc.make_bar_chart(x, 'Day', moist_y, 'Moisture (%)', '7-Day Moisture History')
    humidJSON = bc.make_bar_chart(x, 'Day', humid_y, 'Humidity (%)', '7-Day Humidity History')
    tempJSON = bc.make_bar_chart(x, 'Day', temp_y, 'Temperature (°F)', '7-Day Temperature History')

    return render_template("stats.html", moistJSON=moistJSON, humidJSON=humidJSON, tempJSON=tempJSON, data=db.get_page_data(conn))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    conn = get_db_connection()
    current_vote = db.get_user_vote(conn, current_user.get_id())

    if request.method == 'POST':
        match request.form['post_type']:
            case 'vote':
                user_id = request.form['user_id']
                vote = request.form['voteRadioOptions'] # Yes = 1; No = -1
                db.add_user_vote(conn, user_id, vote)
                current_vote = int(vote)
    
    return render_template(
        "vote.html",
        client_id = config.client_id,
        login_uri = config.login_uri,
        user_id = current_user.get_id(),
        current_vote = current_vote, 
        data=db.get_page_data(conn)
    )

@app.route("/login", methods=["POST"])
def login():
    credential = jwt.decode(request.form['credential'], options={"verify_signature": False}, algorithms="RS256")
    login_user(user.User(credential["email"]))
    return redirect(url_for("vote"))

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("vote"))

@app.route("/about")
def about():
    conn = get_db_connection()
    return render_template("about.html", data=db.get_page_data(conn))

@app.route("/live")
def live():
    conn = get_db_connection()
    return render_template("live.html", data=db.get_page_data(conn))

@app.route("/tos")
def tos():
    return render_template("tos.html")

@app.route("/policy")
def policy():
    return render_template("policy.html")

if __name__ == "__main__":
    app.run()

