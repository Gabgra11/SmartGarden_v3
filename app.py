"""
TODO: Pull data from db for graphs in stats
TODO: Pull live data from db for live data view
TODO: Verify token in /login https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
TODO: Fill out readme.md setup
TODO: Implement live, 7-day data storage. CSV? SQLite?
TODO: Implement live stream.
TODO: Decrease footer height.
TODO: Share header/footer nav across all files. jinja blocks extends
TODO: Pull stats data from db
TODO: Config parser
TODO: Hash load_user function, move to users.py
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
    return render_template("index.html")

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

    return render_template("stats.html", moistJSON=moistJSON, humidJSON=humidJSON, tempJSON=tempJSON,)

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

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
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

