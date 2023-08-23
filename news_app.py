from flask import Flask, redirect, url_for, render_template, request
from scripts import db
import config

application = app = Flask(__name__)
app.config['SECRET_KEY'] = config.client_secret

@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        db.add_news_note(title, body)

    return render_template(
        "news_form.html"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)