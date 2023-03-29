from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String)
    long_url = db.Column(db.String)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    with app.app_context():
        urls = Url.query.all()
    return render_template("base.html", urls=urls)