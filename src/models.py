from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey



db = SQLAlchemy()

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
        db.session.add(self)  #Insert
        db.session.commit()   #Guarda

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
    profession = db.Column(db.String(10), default="")
    website=db.Column(db.String(120), default="")
    github=db.Column(db.String(120), default="")
    twitter=db.Column(db.String(120), default="")
    instagram=db.Column(db.String(120), default="")
    facebook=db.Column(db.String(120), default="")
    #trans= db.Column(db.String(120),nullable=False) FK ?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "city": self.city,
            "profession": self.profession,
            "website":self.website,
            "github":self.github,
            "twitter":self.twitter,
            "instagram":self.instagram,
            "facebook":self.facebook
            
        }

    def save(self):
        db.session.add(self)  #Insert
        db.session.commit()   #Guarda

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

######## Tabla serialize ######### Puedo devolver los datos del perfil a consultar con el usuario

    def serialize_with_user(self):
        return {
            "id": self.id,
            "city": self.city,
            "profession": self.profession,
            "website":self.website,
            "github":self.github,
            "twitter":self.twitter,
            "instagram":self.instagram,
            "facebook":self.facebook,
            "user":{
                "name":self.user.name
            }
        }



##############    ORDEN   ##############
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
           # "user_id":self.user_id,
            #"addressee":self.addressee_id,
            #"status_id":self.status_id
        }


##############    ADDRESSEE   ##############
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