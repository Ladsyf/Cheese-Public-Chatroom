from datetime import datetime

from flask import Flask, request, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from terminalChat import countDownDel, delete

import CRUDmessage
from CRUDmessage import addMessage

import CRUDroom
from CRUDroom import add

import time

print()

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fcvfynsismyhnc:2d819455cbdf3297b9e1bebf9c5b12c8f777eefa5a8aad60709db0789e9d5255@ec2-54-85-56-210.compute-1.amazonaws.com:5432/davqk24266br2q'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheese.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '*$0)rdca5#fNJLFfF]3E'
socketio = SocketIO(app)

db = SQLAlchemy(app)
max_messages = 500
max_participants = 3
max_rooms = 6

class Rooms(db.Model):
    RID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    visibility = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.Column(db.Integer)
    closing = db.Column(db.Boolean)
    chatters = db.Column(db.Integer)

    def __init__(self, name, date, visibility, messages, closing, chatters):
        self.name = name
        self.visibility = visibility
        self.date = date
        self.messages = messages
        self.closing = closing
        self.chatters = chatters

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
    query = request.args.get('query')
    search = "%{}%".format(query)
    public_rooms = Rooms.query.filter_by(visibility='public').filter(Rooms.name.like(search)).all()
    if query:
        return render_template('partial/roomsQuery.html', rooms=public_rooms, LastMessage=getLastMessage)
    elif query == "":
        return render_template('partial/roomsQuery.html',rooms = public_rooms, LastMessage = getLastMessage)

    public_rooms = Rooms.query.filter_by(visibility='public').all()
    return render_template('listrooms.html', rooms=public_rooms, LastMessage=getLastMessage)

@app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    roomQuery = Rooms.query.count()
    if request.method == "POST":
        if roomQuery >= max_rooms:
            flash("Sorry, the creation of rooms are currently closed due to maximum numbers of rooms")
        elif not request.form['name']:
            flash('Please Enter a Room Name!')
        elif Rooms.query.filter_by(name=request.form['name']).first():
            flash('Name already exists!')
        else:
            date = datetime.now()
            room = Rooms(request.form['name'], date, request.form['visibility'], 0, False, 0)

            db.session.add(room)
            db.session.commit()
            return redirect(url_for('roomview', RID = room.RID, name = room.name))
    return render_template('createroom.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
        chatters = room.chatters
        if chatters < max_participants:
            return render_template('room.html', RID = RID, name = name, room = room, messages = messages, chatters = chatters)
        else:
            flash("The room is currently full, please try again later")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/chatlog/<RID>')
def chatlogs(RID):
    room = Rooms.query.filter_by(RID=RID).first()
    messages = Logs.query.filter_by(RID=RID).all()

    if room.messages >= max_messages:
        countDownDel(db, room, Rooms, Logs)

    return render_template('partial/chatlog.html', messages = messages, room = room, max_message = max_messages, closing = room.closing)

@app.route('/addMsg', methods = ['POST'])
def addMsg():
    if request.method == "POST":
        RID = request.form['RID']
        room = Rooms.query.filter_by(RID=RID).first()
        if room.messages < max_messages:
            message = request.form['message']
            CRUDroom.updateMessage(db, Rooms, RID)
            CRUDmessage.addMessage(db, Logs, RID, message)
        return redirect(url_for('chatlogs', RID = RID))
    else:
        return redirect(url_for('index'))

@app.route('/copyLink')
def copyLink():
    flash("Invitation Copied!")
    return render_template('partial/copyNoticeFlash.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('received event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('send msg', json, callback=messageReceived)

@socketio.on('join')
def on_join(data, methods=['GET', 'POST']):
    channel = data['channel']
    join_room(channel)
    leave_room(request.sid)
    updateChattersCount(channel, True)
    print("someone joined on Room "+ str(channel))
    send( "someone joined", to = channel)

@socketio.on('leave')
def on_leave(channel, methods=['GET', 'POST']):
    leave_room(channel)
    updateChattersCount(channel, False)
    print('someone disconnected: ' + str(request.sid) + " channel: " + str(channel))
    send( "someone left", to = channel)

@socketio.on('disconnect')
def on_disconnecting():
    channel = rooms()[0]
    socketio.emit('someone leftroom')
    on_leave(channel)

def deleteRoom(RID):
    room = Rooms.query.filter_by(RID=RID).first()
    delete(db, room, Rooms, Logs)

def updateChattersCount(RID, isAdd, methods=['GET', 'POST']):
    room = Rooms.query.filter_by(RID = RID).first()

    if isAdd:
        room.chatters = room.chatters + 1
    else:
        room.chatters = room.chatters - 1
        if room.chatters <= 0 and room.visibility == "private":
            deleteRoom(RID)

    db.session.commit()
    chatters = room.chatters
    socketio.emit('update participants', chatters, room = RID)

def onServerReset_ResetParticipants():
    #this ensures that the participants are back to 0 when the server starts
    room = Rooms.query.all()
    for r in room:
        r.chatters = 0
        db.session.commit()


onServerReset_ResetParticipants()

if __name__ == '__main__':
    socketio.run(app, debug=True)