def addMessage(db, log, rid, message):
    q = log(rid, message)
    db.session.add(q)
    db.session.commit()
    q.MID
    
