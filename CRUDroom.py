def add(db, rooms, name):
    q = rooms(name)
    db.session.add(q)
    db.session.commit()
    q.RID

