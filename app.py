from datetime import datetime

from flask import Flask, request, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
from terminalChat import countDownDel

import CRUDmessage
from CRUDmessage import addMessage

import CRUDroom
from CRUDroom import add

import time



app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fcvfynsismyhnc:2d819455cbdf3297b9e1bebf9c5b12c8f777eefa5a8aad60709db0789e9d5255@ec2-54-85-56-210.compute-1.amazonaws.com:5432/davqk24266br2q'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheese.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '*$0)rdca5#fNJLFfF]3E'
socketio = SocketIO(app)

db = SQLAlchemy(app)
max_messages = 800

class Rooms(db.Model):
    RID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    visibility = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.Column(db.Integer)
    closing = db.Column(db.Boolean)

    def __init__(self, name, date, visibility, messages, closing):
        self.name = name
        self.visibility = visibility
        self.date = date
        self.messages = messages
        self.closing = closing

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

def getLastMessage(RID):
    LastMessage = Logs.query.filter_by(RID=RID).order_by(Logs.MID.desc()).first()
    if LastMessage:
        return LastMessage.message
    return "No messages yet..."

@app.route('/', methods=['GET', 'POST'])
def index():
    public_rooms = Rooms.query.filter_by(visibility = "public").all()
    return render_template('listrooms.html',rooms = public_rooms, LastMessage = getLastMessage)

@app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    if request.method == "POST":
        if not request.form['name']:
            flash('Please Enter a Room Name!')
        elif Rooms.query.filter_by(name=request.form['name']).first():
            flash('Name already exists!')
        else:
            date = datetime.now()
            room = Rooms(request.form['name'], date, request.form['visibility'], 0, False)

            db.session.add(room)
            db.session.commit()
            flash('Successfully Added!')
            return redirect(url_for('index'))
    return render_template('createroom.html')

@app.route('/room/<RID>/<name>', methods=['GET', 'POST'])
def roomview(RID, name):
    # does not increment number of messages
    # this block of code is meant for long polling/short polling
    # if request.method == "POST":
    #     if not request.form['message']:
    #         flash('Please Enter a message!')
    #     else:
    #         message = Logs(RID, request.form['message'])
    #
    #         db.session.add(message)
    #         db.session.commit()
    #         flash('Message sent!')
    #         return redirect(url_for('roomview', RID = RID, name = name))

    room = Rooms.query.filter_by(RID=RID, name=name).first()
    messages = Logs.query.filter_by(RID=RID).all()
    if room:
        return render_template('room.html', RID = RID, name = name, room = room, messages = messages)
    else:
        return redirect(url_for('index'))

@app.route('/chatlog/<RID>')
def chatlogs(RID):
    room = Rooms.query.filter_by(RID=RID).first()
    messages = Logs.query.filter_by(RID=RID).all()


    return render_template('partial/chatlog.html', messages = messages, room = room, max_message = max_messages)

@app.route('/addMsg', methods = ['POST'])
def addMsg():
    if request.method == "POST":
        RID = request.form['RID']
        room = Rooms.query.filter_by(RID=RID).first()
        if room.messages < max_messages:
            message = request.form['message']
            CRUDroom.updateMessage(db, Rooms, RID)
            CRUDmessage.addMessage(db, Logs, RID, message)
        else:
            pass
        return redirect(url_for('chatlogs', RID = RID))
    else:
        return redirect(url_for('index'))

@app.route('/session', methods=['GET', 'POST'])
def session():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('received event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('message', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)