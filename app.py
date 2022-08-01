from datetime import datetime

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
    name = db.Column(db.String(100), unique=True, nullable=False)
    visibility = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.Column(db.Integer)

    def __init__(self, name, date, visibility, messages):
        self.name = name
        self.visibility = visibility
        self.date = date
        self.messages = messages

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
    public_room = Rooms.query.filter_by(visibility = "public").all()
    return render_template('listrooms.html', rooms = public_room)

@app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    if request.method == "POST":
        if not request.form['name']:
            flash('Please Enter a Room Name!')
        elif Rooms.query.filter_by(name=request.form['name']).first():
            flash('Name already exists!')
        else:
            date = datetime.now()
            add = Rooms(request.form['name'], date, request.form['visibility'], 0)

            db.session.add(add)
            db.session.commit()
            flash('Successfully Added!')
            return redirect(url_for('index'))
    return render_template('createroom.html')

@app.route('/room/<RID>/<name>', methods=['GET'])
def roomview(RID, name):
    room = Rooms.query.filter_by(RID=RID, name = name).first()
    messages = Logs.query.filter_by(RID=RID).all()
    if room:
        return render_template('room.html', RID = RID, name = name, room = room, messages = messages)
    else:
        return redirect(url_for('index'))





