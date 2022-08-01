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

    def __init__(self, RID, message):
        self.RID = RID
        self.message = message

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
            room = Rooms(request.form['name'], date, request.form['visibility'], 0)

            db.session.add(room)
            db.session.commit()
            flash('Successfully Added!')
            return redirect(url_for('index'))
    return render_template('createroom.html')

@app.route('/room/<RID>/<name>', methods=['GET', 'POST'])
def roomview(RID, name): # add number of messages
    if request.method == "POST":
        if not request.form['message']:
            flash('Please Enter a message!')
        else:
            message = Logs(RID, request.form['message'])

            db.session.add(message)
            db.session.commit()
            flash('Message sent!')
            return redirect(url_for('roomview', RID = RID, name = name))

    room = Rooms.query.filter_by(RID=RID, name = name).first()
    messages = Logs.query.filter_by(RID=RID).all()
    if room:
        return render_template('room.html', RID = RID, name = name, room = room, messages = messages)
    else:
        return redirect(url_for('index'))

@app.route('/chatlog/<RID>')
def chatlogs(RID):
    messages = Logs.query.filter_by(RID=RID).all()
    return render_template('partial/chatlog.html', messages = messages)




