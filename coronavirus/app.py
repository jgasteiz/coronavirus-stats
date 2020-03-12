from flask import Flask, render_template

from . import website_data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", **website_data.get_website_data())
