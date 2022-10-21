"""
TODO: Fill out readme.md
TODO: Fill out About tab.
TODO: Host website! On raspberry pi? Google Cloud?
TODO: Implement live, 7-day data storage. CSV? SQLite?
TODO: Implement live stream.
TODO: Increase header nav size.
TODO: Share header nav across all files. (Is this possible?)
"""

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")


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

