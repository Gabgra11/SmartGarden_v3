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


@app.route("/donate")
def donate():
    return render_template("donate.html")
"""
@app.route("/<name>")
def user(name):
    return f"hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="ADMIN"))

@ap.route('/', methods=['GET', 'POST'])
def parse_request():
    data = request.form
    return f"Data: {data}"
"""


if __name__ == "__main__":
    app.run()

