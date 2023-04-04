from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String)
    long_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'URL(id={self.id}, long_url="{self.long_url}", short_url="{self.short_url}")'

@app.before_first_request
def before_first_request():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    short_url = hashlib.sha256(long_url.encode()).hexdigest()[:8]

    url = URL(long_url=long_url, short_url=short_url)
    db.session.add(url)
    db.session.commit()

    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url is None:
        return 'Invalid URL'
    return redirect(url.long_url)