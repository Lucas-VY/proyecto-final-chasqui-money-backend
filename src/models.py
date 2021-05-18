from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey



db = SQLAlchemy()

##############    USER   ##############

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    last_name = db.Column(db.String(120),nullable=False)
    #rut = db.Column(db.String(15),nullable=False, unique=True)
    email = db.Column(db.String(120),nullable=False, unique=True)
    password = db.Column(db.String(1000),nullable=False)
    phone = db.Column(db.Integer,nullable=False, unique=True)
    
    profile= db.relationship('Profile', cascade="all, delete", backref="user", uselist=False) #1 a 1
    card= db.relationship('Card', cascade="all, delete", backref="user") # 1 a muchos
    #Este me retorna un array con todos los objetos de tipo Card que esten asociados a ese usuario
    #Cuantas ordenes tiene el usuario
    
    def save(self):
        db.session.add(self)  
        db.session.commit()   

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):    #Devuelve todos los datos del user (Normal)
        return {
            "id": self.id,
            "name":self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone":self.phone
        }
    
    def user_with_profile(self):     #Devuelve todos los datos del user + todos los de profile
        return {
            "id": self.id,
            "name":self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone":self.phone,
            "profile":self.profile.serialize()  #Devuelve todo lo de profile
            
        }

    def serialize_profile(self):       #Devuelve todos los datos del user + 2 especificos de profile. Corresponde a los datos exactos que pide el fronted en Profile
        return {
            "name":self.name,
            "last_name": self.last_name,
            "country":self.profile.country,
            "phone":self.phone,
            "address":self.profile.address,
            "email": self.email
        }
    

    def serialize_user_with_cards(self):     #Devuelve todos los datos del user + todos los de profile
        return {
            "id": self.id,
            "name":self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone":self.phone,
            "cards":self.get_cards()
            
        }

    def serialize_user_with_cards_profile(self):     #Devuelve todos los datos del user + todos los de profile
        return {
            "id": self.id,
            "name":self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone":self.phone,
            "cards":self.get_cards(),
            "profile":self.profile.serialize(),
            #"addressee":self.addressee.get_cards()
            
            
        }   

    def user_with_card(self):     #Devuelve todos los datos del user + todos los de profile
        return (
            self.get_cards_historial()  #Devuelve todo lo de profile
            
        )
    
    def get_cards(self):
        return list(map(lambda card : card.serialize(), self.card))

    def get_cards_historial(self):
        return list(map(lambda card : card.serialize_historial(), self.card))
    


    def card_by_user(self):
        return len(self.card)


    
    
    




##############    CARD   ##############
class Card(db.Model):
    __tablename__ ='card'
    id = db.Column(db.Integer,primary_key=True)
    money_send = db.Column(db.Integer,nullable=False)
    date = db.Column(db.String(120)) #Cambiar a dato fecha
    transaction_code = db.Column(db.Integer,nullable=False) #Comprobante

    number_transfer= db.Column(db.Integer)
    

    full_name = db.Column(db.String(120),nullable=False)
    country = db.Column(db.String(120),nullable=False)
    bank_payment = db.Column(db.String(120),nullable=False)
    account_number = db.Column(db.String(120),nullable=False) 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    #addressee_id=db.Column(db.Integer, db.ForeignKey('addressee.id', ondelete='CASCADE'),nullable=False)

    #addressee= db.relationship('Addressee', cascade="all, delete", backref="card") # 1 a muchos 
    


    def save(self):
        db.session.add(self)  
        db.session.commit()   

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):    #Devuelve todos los datos de Card
        return {
            "id": self.id,
            "money_send": self.money_send,
            "date": self.date,
            "transaction_code": self.transaction_code,
            "user_id":self.user_id  ,  
            "full_name":self.full_name,
	        "country":self.country,
	        "bank_payment":self.bank_payment,
	        "account_number":self.account_number,
            "number_transfer":self.number_transfer      
        }  

    def serialize_historial(self):    #Devuelve todos los datos de Card
        return {
            #"id": self.id,
            "money_send": self.money_send,
            "date": self.date,  
            "full_name":self.full_name,
            "number_transfer":self.number_transfer      
        }  

    def serialize_card_with_user(self):    #Devuelve todos los datos de Card
        return {
            "id": self.id,
            "money_send": self.money_send,
            "date": self.date,
            "transaction_code": self.transaction_code,
            "user":{
                "id":self.user.id,
                "email":self.user.email
            }
            
        } 


    





##############    PROFILE   ##############

class Profile(db.Model):
    __tablename__ ='profile'
    id = db.Column(db.Integer,primary_key=True)
    country = db.Column(db.String(120), default="")
    address = db.Column(db.String(10), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)

    def serialize(self):       #Devuelve todos los datos de profile
        return {
            "id": self.id,
            "country": self.country,
            "address": self.address    
        }

    def save(self):
        db.session.add(self)  
        db.session.commit()   

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def serialize_with_user(self):      #Devuelve todos los datos de profile + el nombre de usuario
        return {
            "id": self.id,
            "country": self.country,
            "address": self.address,
            "user":{
                "name":self.user.name
            }
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

