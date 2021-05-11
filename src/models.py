from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey



db = SQLAlchemy()

##############    BANK DATA   ##############

class Bank(db.Model):
    __tablename__='bank'
    id = db.Column(db.Integer,primary_key=True)
    card_number = db.Column(db.Integer,nullable=False)
    expires_card = db.Column(db.String(120),nullable=False)
    cvv = db.Column(db.Integer,nullable=False, unique=True)
    bank_payment = db.Column(db.String(100),nullable=False)
    account_number = db.Column(db.Integer,nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "card_number":self.card_number,
            "expires_card": self.expires_card,
            "cvv":self.cvv,
            "bank_payment": self.bank_payment,
            "account_number": self.account_number
        }
    
    def save(self):
        db.session.add(self)  
        db.session.commit()   

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


##############    USER   ##############

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    last_name = db.Column(db.String(120),nullable=False)
    rut = db.Column(db.String(15),nullable=False, unique=True)
    email = db.Column(db.String(120),nullable=False, unique=True)
    password = db.Column(db.String(1000),nullable=False)
    phone = db.Column(db.Integer,nullable=False, unique=True)
    profile= db.relationship('Profile', cascade="all, delete", backref="user", uselist=False) #Campo es de 1 a1
    #profile= db.relationship('Bank_Data', cascade="all, delete", backref="user", uselist=False) #Campo es de 1 a1
    #profile= db.relationship('Orden', cascade="all, delete", backref="user", uselist=False) #Campo es de 1 a1

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "last_name": self.last_name,
            "rut":self.rut,
            "email": self.email,
            ## PASSWORD
            "phone":self.phone
        }
    
    def serialize_with_profile(self):
        return {
            "id": self.id,
            "name":self.name,
            "last_name": self.last_name,
            "rut":self.rut,
            "email": self.email,
            "phone":self.phone,
            "profile":self.profile.serialize()
            
        }

    
    
    def save(self):
        db.session.add(self)  
        db.session.commit()   

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


##############    PROFILE   ##############

class Profile(db.Model):
    __tablename__ ='profile'
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String(120), default="")
    country = db.Column(db.String(10), default="")
    #trans= db.Column(db.String(120),nullable=False) FK ?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "city": self.city,
            "country": self.country    
        }

    def save(self):
        db.session.add(self)  
        db.session.commit()   

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def serialize_with_user(self):
        return {
            "id": self.id,
            "city": self.city,
            "country": self.country,
            "user":{
                "name":self.user.name
            }
        }


##############    ORDEN   ##############
class Order(db.Model):
    __tablename__ ='order'
    id = db.Column(db.Integer,primary_key=True)
    money_send = db.Column(db.Integer,nullable=False)
    date = db.Column(db.String(120),nullable=False) #Cambiar a dato fecha
    transaction_code = db.Column(db.String(120),nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    destino_id = db.Column(db.Integer, db.ForeignKey('destino.id', ondelete='CASCADE'),nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'),nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "money_send": self.money_send,
            "date": self.date,
            "transaction_code": self.transaction_code
           # "user_id":self.user_id,
            #"destino":self.destino_id,
            #"status_id":self.status_id
        }



##############    Destino   ##############
class Destino(db.Model):
    __tablename__ ='destino'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(120),nullable=False)
    last_name = db.Column(db.String(120),nullable=False)
    bank_payment = db.Column(db.String(120),nullable=False)
    account_number = db.Column(db.Integer,nullable=False) 

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bank_payment": self.bank_payment,
            "account_number": self.account_number
        }
    

##############    STATUS   ##############
class Status(db.Model):
    __tablename__ ='status'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(120),nullable=False)  #Ver lista?

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description
        }






##############    ADMINISTRATOR   ##############
class Administrator(db.Model):
    __tablename__ ='administrator'
    id = db.Column(db.Integer,primary_key=True)
    notification = db.Column(db.String(120),nullable=False)  #Ver como realizarla

    def serialize(self):
        return {
            "id": self.id,
            "notification": self.notification
        }