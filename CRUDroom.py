def add(db, rooms, name):
    q = rooms(name)
    db.session.add(q)
    db.session.commit()
    q.RID

def updateMessage(db, rooms, RID):
    roomMSG = rooms.query.filter_by(RID = RID).first()
    MessageCount = roomMSG.messages
    roomMSG.messages = MessageCount + 1
    db.session.commit()