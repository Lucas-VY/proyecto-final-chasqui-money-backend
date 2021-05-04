from flask import Flask, json, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, 
#JWT

app = Flask(__name__)
app.url_map.strict_slashes = False #no errores si incluyo o no un / en una ruta ó endpoints
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"


db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)



@app.route('/')
def main():
    return render_template('index.html')










if __name__ == '__main__':
    manager.run()