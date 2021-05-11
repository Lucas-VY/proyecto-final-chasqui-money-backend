from flask import Flask, json, jsonify, request, render_template
from flask_script import Manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Profile
#JWT
app = Flask(__name__)
app.url_map.strict_slashes = False #no errores si incluyo o no un / en una ruta ó endpoints
app.config['DEBUG'] = True  #Muestra errores del servidor
app.config['ENV'] = 'development' #Evitar cortar y levantar el servidor
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  #Vincula app con bd
Migrate(app, db)  #Vincula comandos
CORS(app)
manager = Manager(app) ##Adminsitra el app
manager.add_command("db", MigrateCommand) #Genera comando db 



@app.route('/')
def main():
    return jsonify({'msg':'Exito'})


##############    REGISTRO GET   ##############

@app.route('/users', methods=['GET'])    
@app.route('/users/<int:id>', methods=['GET','PUT','DELETE'])
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
                map(lambda user : user.serialize_with_profile(),users)
            )
           
           
            return jsonify({
                "Total Usuarios":len(users), 
                "Usuarios":users
            }),200    
     
    if request.method == 'PUT':
        pass

    
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
    rut = request.json.get('rut')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')


    user = User()
    user.name=name
    user.last_name =last_name
    user.rut=rut
    user.email=email
    user.password=generate_password_hash(password)
    user.phone=phone
    profile = Profile()
    user.profile = profile
    user.save()


    return jsonify({'Usuario creado': user.serialize()}),201



########### PROFILE #############

@app.route('/user/<int:id>/profile', methods=['POST','PUT'])
def profile(id=None):

    if id is not None:
        user = User.query.filter_by(id=id).first()

        if not user: 
            return jsonify({
                "Error": "Usuario no encontrado"
        }),404

        if user:
            city=request.json.get('city',"")
            country=request.json.get('country',"")
    
            profile = Profile()

            profile.city=city
            profile.country=country
            profile.user_id=user.id
            #profile.id=user.id
            #user.profile = profile
            profile.save()

            return jsonify({'Datos Profile creados': profile.serialize()}),201


########### LOGIN ###############

@app.route('/user/signin', methods=['POST'])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            
            return jsonify({"Contraseña coindice": user.serialize()}), 200
        else:
            return jsonify({"message":"Usuario o contraseña invalida"}), 400
    else:
        return jsonify({"message":"Usuario o contraseña invalida"}), 400


if __name__ == '__main__':
    manager.run()

 