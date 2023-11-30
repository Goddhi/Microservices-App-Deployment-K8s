# Deploying Stateful Microservices: Persisting Data in Kubernetes

**Requirements**
In this part of the guide, we are going to deploy a PostgreSQL database and change our Flask application code to make it use the database to store its state. When a user adds an element to the todo list, it will not disappear when the Pod restarts or disappear since everything will be saved to the PostgreSQL database. This will not make our microservice stateful, but a stateless microservice that stores its state on an external datastore.

Make sure that you already installed virtualenvwrapper:

Now, create a folder for the new application:

`cd $HOME`
`mkdir -p stateful-flask`
`cd stateful-flask`
`mkdir -p app`
`mkdir -p kubernetes`

We are going to use stateful-namespace as a name as opposed to stateless-namespace in the previous part. However, as said, this does not mean that the new Flask application that we are going to create is stateful, it is still stateless but uses an external datastore (PostgreSQL) to store its state. The database, on the other hand, is a stateful service.

### Creating a Namespace
Let’s start by creating a namespace for the database:
check `postgres-namespace.yaml`

And a namespace for the Flask application:
check `stateful-namespace.yaml`


Then we apply the namespaces:

`kubectl apply -f postgres-namespace.yaml `
`kubectl apply -f stateful-namespace.yaml`


### Creating a ConfigMap for the PostgreSQL database
A ConfigMap is a resource that stores non-confidential configuration data
as key-value pairs. It allows configuration data to be decoupled from
containerized applications, making it easy to update and manage
configurations without having to rebuild and redeploy the entire
application.

ConfigMaps can store configuration data mainly environment variables,
configuration files, and any other non-confidential data that your
applications might need. When a Pod starts, it can read the configuration data of a container from the ConfigMap as environment variables or files mounted in a volume. This resource is particularly useful in several scenarios, including when multiple applications share the same configuration when the configuration data needs to be changed frequently without redeploying Pods, or when you want to organize your Deployments by decoupling operations from data. Instead of managing the configuration for each application separately, a single ConfigMap can be used to store the configuration data, which can then be accessed by multiple applications.
ConfigMaps can be created using the kubectl command-line tool or by
declaring a ConfigMap object in a manifest file.

### ConfigMap for PostgreSQL
In the following steps, we are going to create a ConfigMap for PostgreSQL.
The ConfigMap will contain the following files:
POSTGRES_DB - the name of the database to create
POSTGRES_USER - the name of the user to create
POSTGRES_PASSWORD - the password of the user to create

Apply the ConfigMap:
`kubectl apply -f postgres-config.yaml `

### Persisting data storage on PostgreSQL
#### Kubernetes Volumes
A volume is an abstraction layer between the container and physical
storage. It allows containers to store and access data independently of the underlying infrastructure (AWS, GCP, Azure, etc.).
Volumes provide a way to store and persist data in a container beyond the lifetime of a Pod and enable data sharing between Pods.
Kubernetes volumes can be created from various sources such as a local
disk, a network file system, or a cloud provider’s block storage. They can be mounted into a container as a directory or a file, and accessed and manipulated like any other file system.

#### VolumeClaims
A volume claim is a user’s request for storage. It specifies the amount of
storage that a Pod should have access to and uses a StorageClass to define how the storage should be provisioned.

#### StorageClass
The StorageClass is an object that defines the type of storage to be used to dynamically provision a Persistent Volume (PV) in response to a Persistent
Volume Claim (PVC) made by a Pod and configured by a user.

Some examples of StorageClass in Kubernetes are:
- aws-ebs: A storage class for Amazon Elastic Block Store (EBS)
volumes.
- azure-disk: A storage class for Azure disks.
- csi-cephfs: A storage class for CephFS volumes using the Container
Storage Interface (CSI) driver.

- do-block-storage: A type of persistent storage offered by DigitalOcean
(DO) that provides SSD-based storage volumes to store data.
- local-storage: A storage class for local storage on a node.

### Adding storage to PostgreSQL
check `postgres-pvc-pv.yaml`

Let’s create the PersistentVolume and PersistentVolumeClaim:
`kubectl apply -f kubernetes/postgres-pvc-pv.yaml`

You can check the status of the PersistentVolume and
PersistentVolumeClaim with the following commands:
1` kubectl get pv`
2 `kubectl get pvc -n postgres`


### Creating a Deployment for PostgreSQL
We are going to use the following command to create a Deployment for
PostgreSQL.
Although not the best resource to use with PostgreSQL, we will use the Deployment for now.

check `kubernetes/postgres-deployment.yaml`

NOTE: **Reasons why PVC status is pending**
StorageClass specified in the pvc  does not exist
Insufficient Available PVs
etc


**why is it more important to use a configmap volume rather than configmap environment variable**

Let’s apply the Deployment:
Using a `ConfigMap` volume instead of environment variables from a `ConfigMap` in Kubernetes can have several advantages, depending on the use case. While both methods are valid and have their own applications, here are some reasons why using a `ConfigMap` as a volume might be more suitable in certain scenarios:

### 1. **File-Based Configuration**:
   - **Complex Configurations**: When the configuration data is complex and better represented in a file format (like `.ini`, `.yaml`, or `.json`), using a volume is more suitable. It's easier to mount the entire configuration file rather than breaking it down into individual environment variables.
   - **Application Design**: Some applications are designed to read configuration from files and might not support environment variable configurations.

### 2. **Dynamic Updates**:
   - **Reload without Restarting**: Changes to `ConfigMap` volumes can be reflected in the mounted files without restarting the pod (though it may take some time to update). In contrast, environment variables require the pod to be restarted to pick up changes.
   - **Dynamic Configuration Changes**: This is particularly important for applications that can reload their configuration files without needing a full restart.

### 3. **Configuration Size**:
   - **Large Configurations**: There's a practical limit to how much data you can place in environment variables. Large configuration data is more efficiently handled through volumes.

### 4. **Organization and Clarity**:
   - **Separation of Configuration**: Keeping configuration in files can be more organized, especially when dealing with multiple configuration files. It can help maintain clarity, as each config file can be dedicated to a specific aspect of the application settings.
   - **Ease of Management**: It’s often easier to manage and version control a file rather than several environment variables, especially when these configurations need to be replicated across multiple environments.

### 5. **Security**:
   - **Reduced Exposure**: Environment variables can be exposed to any process running in the container, and in some cases, might be logged or inadvertently exposed. Using files can limit this exposure, especially for sensitive configurations.

### 6. **Compatibility**:
   - **Non-String Data**: Some configurations might involve binary data, which is not well-suited for environment variables. Files can handle any type of data without issues.

### 7. **File System Abstractions**:
   - **Symlinks and File Structures**: Applications that expect certain file system structures (like symlinks, directories, etc.) can be more easily accommodated with volumes.

### Use Cases for Environment Variables
Despite these advantages, using environment variables for configuration is still suitable in many cases, especially when dealing with simple, flat configuration that doesn’t change often, or when the application is specifically designed to consume configuration from environment variables.

### Conclusion
The choice between using a `ConfigMap` volume or environment variables depends largely on the nature of the application, the complexity and size of the configuration data, security considerations, and the need for dynamic updates without restarting pods. It's important to evaluate these factors in the context of your specific use case.

#### Creating a Service for PostgreSQL
check `postgres-service.yaml`

Then we will create the service:
kubectl apply -f postgres-service.yaml

### Creating a Deployment for our application
We are going to change the application code in a way that it will connect to the PostgreSQL database and store every todo item in the database. To do this, we will use the following YAML file:

**setting up virtual enviroment**
```
pip install virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```
`mkvirtualenv 'directory-name'`

Freeze the dependencies:
`pip freeze > requirements.txt`

Now we will change the application code. We will add the following code
to the app.py file:

check `app/app.py`

Build the image:
`docker build -t stateful-flask:v0 -f app/Dockerfile app`

Run the container to test the application:
`docker run -it -p 5000:5000 stateful-flask:v0`

You should see an error while connecting to the database, which is normal
because we haven’t deployed the application to the cluster, it’s just a local
test.

We can re-tag and push the image to Docker Hub:

I’m using the image daredrexel/stateful-flask:v0 which is the image I pushed to Docker Hub. You can use your own image.

Then we will create the Deployment:
`kubectl apply -f app-deployment.yml`

We can check status of the Deployment
`kubectl get pods -n stateful-namespace`

Finally, we need to migrate the database:


`export pod=$(kubectl get pods -n stateful-namspace -l app=stateful-flask -o jsonpath='{.items[0].metadata.name}')`

`kubectl exec -it $pod -n stateful-namspace -- flask db init`
`kubectl exec -it $pod -n stateful-namspace -- flask db migrate`
`kubectl exec -it $pod -n stateful-namspace -- flask db upgrade`

### Creating a Service for our application
We are going to use a ClusterIP service to expose the application to the
cluster. To do this, we will use the following YAML file:
check `stateful-flask-service.yml`

Apply the service::
`kubectl apply -f stateful-flask-service.yml`


### Creating an external Service for our application
Since the Ingress controller is in a different namespace, we need to create an external service to expose the application to the cluster. To do this, we
will use the following YAML file:
**Although Ingress controller is a Cluster based resource**
check `stateful-flask-service-externalname.yml`

Apply the service:
`kubectl apply -f stateful-flask-service-externalname.yaml`

#### Creating an Ingress for our application
check `ingress.yml`


