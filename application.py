"""
TODO: Add sensor/motor controls
TODO: Add internet outage backup watering schedule
"""

from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, login_user, logout_user, current_user
from scripts import chart, user, db
import config

login_manager = LoginManager()
application = app = Flask(__name__)
app.config['SECRET_KEY'] = config.client_secret
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id=None):
    return db.get_user_by_id(user_id)

@app.route("/")
def home():
    user_info = db.get_user_json_by_id(current_user.get_id())

    return render_template(
        "index.html",
        data=db.get_page_data(),    # Get vote count, daily statistics
        user=user_info  # JSON with current user info
    )

@app.route("/stats")
def stats():
    moistJSON, humidJSON, tempJSON = chart.get_week_stats_json()
    user_info = db.get_user_json_by_id(current_user.get_id())

    return render_template(
        "stats.html",
        moistJSON=moistJSON,
        humidJSON=humidJSON,
        tempJSON=tempJSON,
        data=db.get_page_data(),
        user = user_info
    )

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    current_vote = db.get_user_vote(current_user.get_id())
    user_info = db.get_user_json_by_id(current_user.get_id())

    if request.method == 'POST':
        user_id = request.form['user_id']
        vote = request.form['voteRadioOptions'] # Yes = 1; No = -1
        db.add_user_vote(user_id, vote)
        current_vote = int(vote)

    return render_template(
        "vote.html",
        client_id = config.client_id,
        login_uri = config.login_uri,
        user = user_info,
        current_vote = current_vote, 
        data=db.get_page_data()
    )

@app.route("/login", methods=["POST"])
def login():
    user_info = user.verify_token(request.form['credential'])
    login_user(user.User(user_info))
    return redirect(url_for("vote"))

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/about")
def about():
    user_info = db.get_user_json_by_id(current_user.get_id())

    return render_template(
        "about.html",
        data=db.get_page_data(),
        user = user_info
    )

@app.route("/live")
def live():
    user_info = db.get_user_json_by_id(current_user.get_id())

    return render_template(
        "live.html",
        data=db.get_page_data(),
        user = user_info,
        image_id=db.get_recent_image_id()
    )

@app.route("/tos")
def tos():
    return render_template("tos.html")

@app.route("/policy")
def policy():
    return render_template("policy.html")

if __name__ == "__main__":
    app.run()