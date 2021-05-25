from flask import Flask, json, jsonify, request, render_template
from flask.helpers import total_seconds
from flask_script import Manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Profile, Card
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from datetime import timedelta
from datetime import date
from datetime import datetime
from random import random, randrange

app = Flask(__name__)
app.url_map.strict_slashes = False #no errores si incluyo o no un / en una ruta ó endpoints
app.config['DEBUG'] = True  #Muestra errores del servidor
app.config['ENV'] = 'development' #Evitar cortar y levantar el servidor
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '7cb2c2339e5adea4d6e6e237c3a04bfd'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=3600)
db.init_app(app)  #Vincula app con bd
Migrate(app, db)  #Vincula comandos
CORS(app)
#cors=CORS(app, resources={r"/*":{"origins":"*"}})
#jwt = JWTManager(app)
manager = Manager(app) ##Adminsitra el app
manager.add_command("db", MigrateCommand) #Genera comando db 
today = date.today()




@app.route('/')
def main():
    return jsonify({'msg':'Exito'})




##############    USUARIOS REGISTRADOS GET   ##############

@app.route('/user', methods=['GET'])    #ME DEVUELVE TODOS LOS USUARIOS
@app.route('/user/<int:id>', methods=['GET','PUT','DELETE'])    #USUARIO EN ESPECIFICO
def users(id=None):
    if request.method == 'GET':
        
        if id is not None:
            user = User.query.get(id)

            if not user: 
                return jsonify({
                    "Error": "Usuario no encontrado"
                }),404

            return jsonify({
                "Correcto": "Usuario encontrado",
                "Usuario": user.serialize()
            }),200

        else:
            users=User.query.all()
            users = list(
                map(lambda user : user.serialize_user_with_cards_profile(),users)
            )

            
           
            return jsonify({
                "Total Usuarios":len(users), 
                "Usuarios":users
            }),200    


     
    
    
    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user: 
            return jsonify({"Error":"Usuario no existe"}),404
        user.delete()
        return jsonify({"Correcto":"Usuario Eliminado"}),200
    
    
##############   REGISTRO POST    ##############
@app.route('/user/signup', methods=['POST'])
def registro():
    name=request.json.get('name')
    last_name = request.json.get('last_name')
    #rut = request.json.get('rut')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')

    if not name:
        return jsonify({"Error":"Indicar Nombre"}), 400

    if not last_name:
        return jsonify({"Error":"Indicar Apellido"}), 400
    #if not rut:
        #return jsonify({"Error":"Indicar Rut"}), 400
    if not email:
        return jsonify({"Error":"Indicar Email"}), 400
    if not password:
        return jsonify({"Error":"Indicar Password"}), 400
    if not phone:
        return jsonify({"Error":"Indicar Telefono"}), 400

    #user = User.query.filter_by(rut=rut).first()
    #if user:
        #return jsonify({"Error":"Este Rut ya se encuentra registrado"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"Error":"Este Email ya se encuentra registrado"}), 400
    
    user = User.query.filter_by(phone=phone).first()
    if user:
        return jsonify({"Error":"Este Telefono ya se encuentra registrado"}), 400


    user = User()
    user.name=name
    user.last_name =last_name
    #user.rut=rut
    user.email=email
    user.password=generate_password_hash(password)
    user.phone=phone
    profile = Profile()
    user.profile = profile
    user.save()


    return jsonify({'Usuario creado': user.serialize()}),201





########### PROFILE #############

#Ruta con token funciona, pero hay que ver que sucede con el profile id especifico.    

@app.route('/user/profile/<int:id>', methods=['GET','PUT'])  
#@jwt_required()   #Activar para Token 
def profile(id=None):

    ##Actualiza los datos de profile##
    if request.method == 'PUT':
        if id is not None:
            user = User.query.filter_by(id=id).first()

            if not user: 
                return jsonify({
                    "Error": "Usuario no encontrado"
            }),404

            if user:
                country=request.json.get('country',"")
                address=request.json.get('address',"")
    
                #profile = Profile()

                user.profile.country=country
                user.profile.address=address
                #profile.user_id=user.id
            
                #profile.save()
                user.update()

                return jsonify({'Datos Profile creados': user.profile.serialize()}),201
    if request.method == 'GET':
        user = User.query.get(id)   #Desactivar sin token
        #current_user = get_jwt_identity() #Activar para token  #Muestra cual es el usuario actual
        return jsonify(user.serialize_profile()), 200 #Desactivar sin token
        #return jsonify({"success":"Private route", "user":current_user}),200  #Activar para token
        #return jsonify(user.serialize_prueba(),{"success":"Private route", "user":current_user}), 200 #Desactivar sin token
        
        
        




########### LOGIN ###############

@app.route('/user/signin', methods=['POST'])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({"Error":"El campo Email se encuentra vacio"}), 400
    if not password:
        return jsonify({"Error":"El campo Password se encuentra vacio"}), 400
  

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"Error":"Usuario o contraseña invalida"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"Error":"Usuario o contraseña invalida(Contraseña"}), 401 

    #access_token = create_access_token(identity=email)  
    #return jsonify({"access_token":access_token}),200
    
    return jsonify({"resultado": user.serialize()}), 200
        








##########     TRANSACCION

#@app.route('/user/card', methods=['GET','POST'])    #ME DEVUELVE TODOS LOS USUARIOS
@app.route('/user/card/<id>', methods=['GET','POST','DELETE'])    #USUARIO EN ESPECIFICO
def cards(id=None):

    if request.method=='GET':
        if id is not None:
            user = User.query.get(id)

            if not user: 
                return jsonify({
                    "Error": "Usuario no encontrado"
                }),404

            return jsonify({
                
                "resultado":user.user_with_card()  #Se asigna serializacion de user con card en getcadr()
            }),200


        else:
            cards=Card.query.all()
            cards = list(map(lambda card : card.serialize(),cards))
            return jsonify({"Cards":cards}),200
    

    if request.method=='POST':
        if id is not None:
            user = User.query.filter_by(id=id).first()

            if not user: 
                return jsonify({
                    "Error": "Usuario no encontrado"
            }),404

            if user:
                #card
                #addressee=Addressee()
                money_send= request.json.get("monto")
                #transaction_code= request.json.get("registroComprobante")
                date= today
                number_transfer=randrange(9999,9999999999)
                user_id=user.id
                money=request.json.get("money")
                

                #destinatario
                full_name= request.json.get("name")
                country= request.json.get("country")
                phone= request.json.get("numero")
                address= request.json.get("direccion")

                
                #addressee.full_name=full_name
                #addressee.country=country
                #addressee.bank_payment=bank_payment
                #addressee.account_number=account_number
                
                card= Card()
                card.full_name=full_name
                card.country=country
                card.phone=phone
                card.address=address
                card.money_send=money_send
                #card.transaction_code=transaction_code
                card.date=date
                card.money=money
                card.number_transfer=number_transfer
                card.user_id= user_id
                #card.addressee_id=addressee_id
                card.save()

                return jsonify(card.serialize_card_with_user()),201
        
    




if __name__ == '__main__':
    manager.run()

    
