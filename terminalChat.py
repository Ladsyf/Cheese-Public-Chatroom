import time
from threading import Thread, Timer

def countDownDel(db, room, Rooms, Logs):
    time = 60
    isClosing = room.closing

    if isClosing:
        print("This chatroom is on the process of deletion")
    else:
        room.closing = True
        db.session.commit()
        Timer(time, rotation, args=(db, room, Rooms,Logs,)).start()

def rotation(db, room, Rooms, Logs):
    RID = room.RID
    Rooms.query.filter_by(RID=RID).delete()
    Logs.query.filter_by(RID=RID).delete()
    db.session.commit()
    print("deleted!")
#delete all messages

