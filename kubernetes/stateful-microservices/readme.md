# Deploying Stateful Microservices: Persisting Data in Kubernetes

**Requirements**
In this part of the guide, we are going to deploy a PostgreSQL database and change our Flask application code to make it use the database to store its state. When a user adds an element to the todo list, it will not disappear when the Pod restarts or disappear since everything will be saved to the PostgreSQL database. This will not make our microservice stateful, but a stateless microservice that stores its state on an external datastore.

Make sure that you already installed virtualenvwrapper: