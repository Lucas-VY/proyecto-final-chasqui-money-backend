from flask import Flask, json, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User

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
manager = Manager(app)
manager.add_command("db", MigrateCommand)



@app.route('/')
def main():
    return jsonify({'msg':'Exito'})


@app.route('/registro', methods=['POST'])
def registrar():
    id=request.json.get('id')
    user_name=request.json.get('user_name')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')

    #Guarda datos en la tabla User
    user = User()
    user.id =id
    user.user_name=user_name
    user.first_name=first_name
    user.last_name =last_name
    user.email=email
    user.password=password
    user.phone=phone

    user.save()

    return jsonify({'Enviado': user.serialize()})


@app.route('/registro')
def getData():
    user = User.query.all()
    user = list(map(lambda user: user.serialize(),user))
    return jsonify(user),200




if __name__ == '__main__':
    manager.run()





if __name__ == '__main__':
    manager.run()