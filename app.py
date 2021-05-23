from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<name>")
def user(name):
    return f"hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="ADMIN"))

if __name__ == "__main__":
    app.run()

