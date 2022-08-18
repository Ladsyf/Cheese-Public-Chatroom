from threading import Thread, Timer

def countDownDel(db, room, Rooms, Logs):
    time = 5
    isClosing = room.closing

    if isClosing:
        print("This chatroom is on the process of deletion")
    else:
        print("OK, deleting now...")
        room.closing = True
        db.session.commit()
        Timer(time, delete, args=(db, room, Rooms,Logs,)).start()

def delete(db, room, Rooms, Logs):
    RID = room.RID
    Rooms.query.filter_by(RID=RID).delete()
    Logs.query.filter_by(RID=RID).delete()
    db.session.commit()
    print("deleted!")