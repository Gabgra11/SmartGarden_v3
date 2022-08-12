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


if __name__ == "__main__":
    app.run()

