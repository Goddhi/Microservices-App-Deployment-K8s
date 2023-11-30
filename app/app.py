
### StateFul APP

# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stateful-flask-user:stateful-flask-password@postgres.postgress-namespace.svc.cluster.local:5432/stateful-flask-db'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), nullable=False)
#     description = db.Column(db.String(200))

# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     tasks = Task.query.all()
#     return jsonify({'tasks': [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]})

# @app.route('/tasks', methods=['POST'])
# def create_task():
#     data = request.get_json()
#     title = data['title']
#     description = data['description']
#     task = Task(title=title, description=description)
#     db.session.add(task)
#     db.session.commit()
#     return jsonify({'task': {'id': task.id, 'title': task.title, 'description': task.description}})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


### database connection explanation

# The line of code you've provided is a configuration statement typically found in a Flask application, specifically for setting up a connection to a SQL database using SQLAlchemy, which is an ORM (Object-Relational Mapping) tool for Python. Let's break down the components of this configuration:

# - `app.config['SQLALCHEMY_DATABASE_URI']`: In a Flask application, `app` is usually an instance of the Flask class, representing your web application. Flask uses a configuration dictionary, `app.config`, to store various configuration variables. Here, `'SQLALCHEMY_DATABASE_URI'` is the key in this dictionary used to set the database connection URL for SQLAlchemy.

# - `'postgresql://stateful-flask-user:stateful-flask-password@postgres.postgres.svc.cluster.local:5432/stateful-flask-db'`: This is the value assigned to the `'SQLALCHEMY_DATABASE_URI'` key. It's a database URI (Uniform Resource Identifier) that SQLAlchemy uses to connect to a PostgreSQL database. Here's a breakdown of its components:
  
#   - `postgresql://`: This is the scheme indicating the database system being used. In this case, it's PostgreSQL.
  
#   - `stateful-flask-user`: This is the username for the database. It's used for authentication.
  
#   - `stateful-flask-password`: This is the password associated with the above username, also used for authentication.
  
#   - `@postgres.postgres.svc.cluster.local`: This part specifies the host where the database server is running. The format suggests that the database service is hosted within a Kubernetes cluster, as indicated by the `.svc.cluster.local` domain, which is a default domain for services in Kubernetes. `postgres.postgres` represents the service name and its namespace in the cluster.
  
#   - `:5432`: This is the port number on which the PostgreSQL server is listening. `5432` is the default port for PostgreSQL.
  
#   - `/stateful-flask-db`: This is the specific database name to which SQLAlchemy will connect within the PostgreSQL server.

# In summary, this line of code configures the Flask application to connect to a PostgreSQL database named `stateful-flask-db` running in a Kubernetes cluster, using the specified username and password for authentication. The database server is accessible within the cluster at `postgres.postgres.svc.cluster.local` on port `5432`.


### Application Code Explanation
# The provided code is a Flask application with SQLAlchemy for database interactions and Flask-Migrate for database migrations. It's a simple REST API for managing tasks, with endpoints to create and retrieve tasks. Let's go through it step-by-step:

# ### Imports and Initial Setup
# - `from flask import Flask, jsonify, request`: Imports necessary components from Flask. `Flask` is used to create the app, `jsonify` for converting Python dictionaries to JSON responses, and `request` for accessing request data.
# - `from flask_sqlalchemy import SQLAlchemy`: Imports SQLAlchemy, an ORM (Object Relational Mapper) for Python.
# - `from flask_migrate import Migrate`: Imports Flask-Migrate for handling SQLAlchemy database migrations.

# ### Application and Database Configuration
# - `app = Flask(__name__)`: Initializes a new Flask web application.
# - `app.config['SQLALCHEMY_DATABASE_URL']`: Sets the database URI for SQLAlchemy. This URI includes the username, password, host, port, and database name for a PostgreSQL database. Note: This should be `SQLALCHEMY_DATABASE_URI`, not `URL`.
# - `db = SQLAlchemy(app)`: Initializes the SQLAlchemy object, linking it with the Flask app.
# - `migrate = Migrate(app, db)`: Initializes Flask-Migrate for handling database migrations with the app and SQLAlchemy instance.

# ### Defining a Database Model
# - `class Task(db.Model)`: Defines a `Task` model class, representing a task in the database.
#   - `id = db.Column(db.Integer, primary_key=True)`: An integer column that serves as the primary key.
#   - `title = db.Column(db.String(80), nullable=False)`: A string column for the task's title, with a maximum length of 80 characters. It cannot be null.
#   - `description = db.Column(db.String(200))`: A string column for the task's description, with a maximum length of 200 characters.

# ### API Endpoints
# - `@app.route('/tasks', methods=['GET'])`: Defines a route to handle GET requests to `/tasks`. This function retrieves all tasks from the database and returns them in JSON format.
# - `@app.route('/tasks', methods=['POST'])`: Defines a route to handle POST requests to `/tasks`. This function creates a new task based on the JSON data received in the request, adds it to the database, and returns the created task in JSON format.

# ### Running the Application
# - `if __name__ == '__main__':`: This conditional ensures that the app runs only if the script is executed directly (not imported as a module).
# - `app.run(debug=True, host='0.0.0.0', port=5000)`: Runs the Flask application with debug mode enabled on host `0.0.0.0` and port `5000`. Running on `0.0.0.0` makes the server accessible from external hosts.

# ### Corrections
# - The function `get tasks()` is incorrectly named. Python function names cannot contain spaces. It should be something like `get_tasks()`.
# - In the `jsonify` line inside `get_tasks`, there's a syntax error with the dictionary key 'description:'. It should be `'description': task.description`.

# ### Summary
# The code is a basic Flask application with REST API endpoints to create and retrieve tasks, using SQLAlchemy for database operations and Flask-Migrate for database migration handling. The application is configured to connect to a PostgreSQL database hosted in a Kubernetes cluster. It demonstrates fundamental concepts of REST API development, ORM usage, and basic CRUD (Create, Read, Update, Delete) operations in a web application.


### Stateless-App

# from flask import Flask, jsonify, request

# app = Flask(__name__)

# ### Define a list of tasks
# tasks = []

# ### route for getting all tasks
# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


# ### Route for get a single task
# @app.route('/tasks', methods=['POST'])
# def add_task():
#     task = {
#         'id': len(tasks) + 1,
#         'title': request.json['title'],
#         'description': request.json['description'],
#     }
#     tasks.append(task)
#     return jsonify(task), 201


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)









from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://stateful-flask-user:stateful-flask-password@postgres.postgress-namespace.svc.cluster.local:5432/stateful-flask-db'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify({'tasks': [
        {'id': task.id, 'title': task.title, 'description': task.description}
        for task in tasks
    ]})


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data['title']
    description = data['description']

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    return jsonify({'task': {
        'id': task.id,
        'title': task.title,
        'description': task.description
    }})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
