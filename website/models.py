from .import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,unique=True)
    firstname=db.Column(db.String(150))
    lastname=db.Column(db.String(150))
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    user_type=db.Column(db.String(150))

class Data(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    cusid=db.Column(db.String,unique=True)
    username=db.Column(db.String(150))
    firstname=db.Column(db.String(150))
    amount=db.Column(db.String(150))
    address=db.Column(db.String(200))
    houseno=db.Column(db.String(100))
    data1 = db.Column(db.LargeBinary, nullable=False)
    rendered_data1 = db.Column(db.Text, nullable=False)
    