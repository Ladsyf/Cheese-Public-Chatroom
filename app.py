from flask import Flask, request, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

import CRUDroom
from CRUDroom import add

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheese.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '*$0)rdca5#fNJLFfF]3E'

db = SQLAlchemy(app)

class Rooms(db.Model):
    RID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Rooms %r>' % self.RID

class Logs(db.Model):
    MID = db.Column(db.Integer, primary_key=True)
    RID = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.Date, nullable=False)

    def __init__(self, RID, message, timestamp):
        self.RID = RID
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return '<Logs %r>' % self.MID

db.create_all()
db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        CRUDroom.add(db, Rooms, "HelloGuys")

    rooms = Rooms.query.all()
    return render_template('listrooms.html', rooms = rooms)

