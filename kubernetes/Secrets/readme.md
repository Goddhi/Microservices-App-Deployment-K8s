# Microservices Patterns: Externalized Configurations

### Storing configurations in the environment

One of the main benefits of microservices is the ability to scale and manage
each service independently.
However, managing configuration data for multiple services and multiple
environments can be challenging. For example, two or more services may
share the same configurations, if we decide to change the configuration, we
need to do the same for all services using it.
Another challenge comes from the fact that changing hard-coded
configurations requires redeploying the code, which involves different steps
such as building and deploying and this can become time-consuming when
changes are frequent.
Implementing the externalized configuration pattern addresses this problem
by storing all application configuration data outside of the codebase. In a
Twelve-factor App, configurations are stored in the environment.
This approach is language- and OS-agnostic and scales smoothly as the app
expands into more deployments. By externalizing configuration data,
microservices can run in multiple environments without modification or
recompilation, making it easier to manage and scale each service
independently.

### Kubernetes Secrets and environment variables: why?

In the previous example, we had this code:

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stateful-flask-us\
er:stateful-flask-password@postgres.postgres.svc.cluster.local:5432/sta
teful-flask-db'
..etc
..etc
..etc

There are three problems in this code:

- The database password is in the code, which is not a good practice
- Whenever we want to change a variable such as the database name, weneed to change it in multiple places in our code
- We need to change the code and redeploy the application

These problems can be solved by using environment variables and secrets.

### Kubernetes Secrets and environment variables: how?
Go the application directory:

set up virtual environmmemt
Use the following command to create a virtual environment named <venv_name>:
`python3 -m venv venv`

pip install Flask==2.2.3
pip install Flask-SQLAlchemy==3.0.3
pip install psycopg2-binary==2.9.6
pip install Flask-Migrate==4.0.4


Freeze the dependencies:
`pip freeze > requirements.txt`

Then, change the code to use environment variables:
check `app/app.py`

The following line we updated in our Flask app sets the URI for Flask’s
SQLAlchemy database connection.

```
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
```

It uses the string formatting method to create the URI using variables
defined earlier in the code (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, and DB_NAME). The resulting URI has the format:
`postgresql://<user>:<password>@<host>:<port>/<database>`

where each of the variables is replaced with the corresponding value.

Now, build and push after changing <DOCKERHUB_USERNAME> with your
Docker Hub username:

```
export DOCKERHUB_USERNAME=<DOCKERHUB_USERNAME>
docker build -t stateful-flask:v0 -f app/Dockerfile app
docker tag stateful-flask:v0 $DOCKERHUB_USERNAME/stateful-flask:v0
docker push $DOCKERHUB_USERNAME/stateful-flask:v0
```

Now, let’s create a Secret for the database user and password.

Kubernetes Secrets are objects that allow you to store and manage sensitive
information, such as passwords, tokens, and keys. They provide a secure way to store sensitive data, rather than hard-coding it in your application or configuration files.

We will use the same user and password as before.

When creating a Secret in Kubernetes, we need to encode the data using base64. We can do this using the echo command and the | base64 pipe.

The result should be:
c3RhdGVmdWwtZmxhc2stdXNlcg==
c3RhdGVmdWwtZmxhc2stcGFzc3dvcmQ=

Kubernetes secrets are stored in an encoded format for security reasons.
This is because Secrets can contain unrecognizable characters such as new lines or special charachters ..etc. The echo -n followed by the | base64 command encodes the data in base64 format without any unrecognizable character.

check `Secrets/stateful-flask-secret.yaml`
Then create the Secret object:

`kubectl apply -f kubernetes/Secrets/stateful-flask-secret.yaml`

To use these Secret, we need to update the Deployment manifest to use the Secret as environment variables.

update this deployment file by referencing the secret env 

check `kubernetes/stateful-microservices/stateful-app-deployment.yml`

Now, let’s create the Deployment:
`kubectl apply -f kubernetes/stateful-microservices/stateful-app-deployment.yml `

You can also view the Secret and Deployment using the kubectl get
command:

`kubectl get secret,deployment -n stateful-namespace`