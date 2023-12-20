#Crear Pipfile
#Ejecutar pipenv --python 3.6.9
#Ejecutar pipenv shell
#Ejecutar pipenv install flask flask-migrate flask-script flask-sqlalchemy
#Para trabajar con Mysql ejecutar pipenv install pymysql
#Para ejecutar server python app.py runserver
from flask import Flask, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Task
from flask_cors import CORS
import json

app = Flask(__name__) # Creando app con Flask
app.url_map.strict_slashes = False # Evitar Restriccion con o sin slash en el url
app.config['DEBUG'] = True # Modo depuracion ver los errores (True o False)
app.config['ENV'] = 'development' # Modo desarrollo (development o production)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Evitar registro de modificaciones en la db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users_tasks.db" # Ruta de la base de datos

db.init_app(app) # Vinculamos app con db
Migrate(app, db) # Create el entorno de migraciones
manager = Manager(app) # Generamos un administrador de ejecucion de app
manager.add_command("db", MigrateCommand) # operaciones de base de datos: db init, db migrate, db upgrade
CORS(app)

@app.route('/todos/user/', methods=['GET'])
@app.route('/todos/user/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def main(username=None):
    if request.method == 'GET':
        if username:
            user = Task.query.filter_by(user=username).first()
            if user:
                return jsonify(json.loads(user.task)), 200
            else:
                return jsonify({"msg": "This user does not exist, call the POST method first to create the list for this username"}), 404
        else:
            tasks = Task.query.all()
            tasks = list(map(lambda task: task.user, tasks))
            return jsonify(tasks), 200

    if request.method == 'POST':
        data = request.get_json()
        if data != []:
            return jsonify({"msg": "The request body must be an empty array"}), 500
        else:
            user = Task.query.filter_by(user=username).first()
            if user:
                return jsonify({"msg": "This user already has a list of todos, use PUT instead to update it"}), 400
            else:
                task = Task()
                task.user = username
                task.task = json.dumps([{"label": "sample task","done": False}])
                db.session.add(task)
                db.session.commit()
                return jsonify({"result": "ok"}), 200

    if request.method == 'PUT':
        data = request.get_json()

        
        if not data or type(data) != list:
            return jsonify({"msg": "The request body is empty but it must be an array of todo's"}), 400
        else:
            user = Task.query.filter_by(user=username).first()
            if user:
                user.task = json.dumps(data)
                db.session.commit()
                return jsonify({"result": f"A list with {len(data)} todo's was successfully saved"}), 200
            else:
                return jsonify({"msg":"This user does not exist, call the POST method first to create the todo list for this username"}),404
    
    if request.method == 'DELETE':
        user = Task.query.filter_by(user=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"result": "ok"}), 200
        else:
            return jsonify({"msg": f"JSON file {username} does not exist"}),500



if __name__ == '__main__':
    manager.run()