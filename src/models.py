from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey



db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(120),nullable=False)
    first_name = db.Column(db.String(120),nullable=False)
    last_name = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.Integer,nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_name":self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            ## No se Serializa"password":self.password,
            "phone":self.phone
            
        }
    
    def save(self):
        db.session.add(self)  #Insert
        db.session.commit()   #Guarda



class Profile(db.Model):
    __tablename__ ='profiles'
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize(self):
        return {
            "id": self.id,
            "city": self.city,
            "phone": self.phone,
            "gender": self.gender,
            "user_id": self.user_id
        }

class Order(db.Model):
    __tablename__ ='order'
    id = db.Column(db.Integer,primary_key=True)
    original_value = db.Column(db.Integer,nullable=False)
    dollar_value = db.Column(db.Integer,nullable=False)
    date = db.Column(db.String(120),nullable=False) #Cambiar a dato fecha
    payment_method = db.Column(db.String(120),nullable=False) #Ver lista?
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    addressee_id= db.Column(db.Integer, db.ForeignKey('addressee.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

    def serialize(self):
        return {
            "id": self.id,
            "original_value": self.original_value,
            "dollar_value": self.dollar_value,
            "date": self.date,
            "payment_method": self.payment_method,
            "user_id":self.user_id,
            "addressee":self.addressee_id,
            "status_id":self.status_id
        }

class Addressee(db.Model):
    __tablename__ ='addressee'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(120),nullable=False)
    last_name = db.Column(db.String(120),nullable=False)
    city = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(10),nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "city": self.city,
            "phone": self.phone,
            "gender":self.gender
        }
    
class Status(db.Model):
    __tablename__ ='status'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(120),nullable=False)  #Ver lista?

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description
        }

class Administrator(db.Model):
    __tablename__ ='administrator'
    id = db.Column(db.Integer,primary_key=True)
    notification = db.Column(db.String(120),nullable=False)  #Ver como realizarla

    def serialize(self):
        return {
            "id": self.id,
            "notification": self.notification
        }