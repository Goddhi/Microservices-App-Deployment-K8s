### ow using Argo CD
23.1 Argo CD: introduction

Argo CD is an open-source continuous deployment (CD) tool for
Kubernetes environments, based on GitOps. It enables developers to deploy
their applications to a Kubernetes cluster simply by pushing to a specific
Git branch. This triggers a continuous deployment pipeline that updates
Kubernetes resources according to changes in the source code.
Argo CD uses concepts such as applications, environments, and syncs to
enable the management and deployment of applications in a Kubernetes
cluster. It offers a user interface and a REST API for managing and
monitoring applications deployed on a Kubernetes cluster. Additionally, it
provides a CLI tool that can be used to manage and monitor applications
deployed on a Kubernetes cluster, and can be integrated with CI/CD tools.

### Argo CD: installation and configuration
Argo CD can be installed on a Kubernetes cluster using the following
command:
`kubectl create namespace argocd`

`kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`

To access the Argo CD UI, you need to create a port-forward to the Argo
CD server (or expose the service using a LoadBalancer or an Ingress):

`kubectl port-forward svc/argocd-server -n argocd 8080:443`

access the UI https://localhost:8080

The default username is admin and the password can be retrieved using the
following command:

`kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo`

To install the Argo CD CLI, use the following commands:

`curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64`
`sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd`
`rm argocd-linux-amd64`

Connect the CLI to the Argo CD server:

`export password=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo)`
`argocd login localhost:8080 --username admin --password $password --insecure`

Now that we have installed the Argo CD CLI and connected it to the Argo
CD server, we can add our cluster to the Argo CD server. However, this step
is only required when Argo CD is not running on the same cluster that we
want to manage. In our case, we can skip this step.

`export cluster=$(kubectl config get-contexts -o name)`
`argocd cluster add $cluster -y`

We can double-check that our cluster has been added using the following
command:
`argocd cluster list`

**Argo CD: creating an application**
We will use this [Github repository ](https://github.com/Goddhi/argocd-examples.git/)to deploy a simple Flask application on
our Kubernetes cluster using Argo CD. You can clone this repository to get
started. The repository contains several examples of applications that can be
deployed using Argo CD, each stored in a separate folder.

Let’s start by creating a namespace for our application:
`kubectl create namespace flask-app`

We can now deploy the application manifest using the following command:

argocd app create flask-app \
--repo https://github.com/Goddhi/argocd-examples.git/ \
--path flask-app \
--dest-server https://kubernetes.default.svc \
--dest-namespace flask-app \
--revision main \
--sync-policy automated

The above command will create an application named flask-app using the
manifest stored in the flask-app folder of the Github repository. The
application will be deployed in the flask-app namespace of the Kubernetes
cluster. The branch used is main. We are using the --sync-policy automated flag to enable automatic synchronization of the application when
a change is detected in the Git repository.

The folder flask-app contains a file kubernetes.yaml that defines the Deployment and Service resources required to deploy the application.

---
apiVersion: apps/v1
kind: Deployment
metadata:
name: flask-app
spec:
replicas: 1
revisionHistoryLimit: 3
selector:
matchLabels:
app: flask-app
template:
metadata:
labels:
app: flask-app
spec:
containers:
- image: eon01/stateless-flask:v0
name: flask-app
ports:
- containerPort: 5000
resources:
limits:
cpu: 100m
memory: 128Mi
requests:
cpu: 100m
memory: 128Mi
readinessProbe:
httpGet:
path: /tasks
port: 5000
initialDelaySeconds: 5
periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
name: flask-app
spec:
ports:
- port: 5000
protocol: TCP
targetPort: 5000
selector:
app: flask-app
type: LoadBalancer

You can visit the Argo CD UI to see the new application using
`https://localhost:8080/application`s. Here, you can view the status, health,
and history of the application, as well as the application details tree...

You can also see that the application has been deployed in the flask-app
namespace of the Kubernetes cluster.
`kubectl get all -n flask-ap`

`Argo CD: automatic synchronization and self-healing`

Since we activated the automatic synchronization of the application, any changes made to the application manifest will trigger a synchronization of the application. For example, we can change the number of replicas from 1 to 2 in the kubernetes.yaml file and push the change to the Github repository. This will trigger a synchronization of the application and update the number of replicas to 2. By default, Argo CD polls the Git repository every 3 minutes to check for changes.
Remember to commit and push the changes to the Github repository.

The concept of the desired state is central to Argo CD. The desired state is
the state defined in the application’s Git repository. Argo CD will
continuously compare the desired state with the actual state and will
automatically synchronize the application if there is a difference between
the two states.
However, sometimes the automated sync policy also means deleting
resources. To prevent accidents, Argo CD will not delete resources by
default. However, if you know what you are doing, you can enable the
deletion of resources using the following command:

`argocd app set $APPNAME --auto-prune`

Another safety mechanism that is enabled by default is protection against
having empty resources. If you want to allow empty resources, you can
disable this safety mechanism using the following command:

`argocd app set $APPNAME --allow-empty`

Another useful mechanism is the ability to return to the desired state when
the current state has been modified. For example, if you manually change the number of replicas to 3, Argo CD will automatically revert the change
to 2. You can enable this mechanism using the following command:
`argocd app set $APPNAME --self-heal`

To activate automated synchronization without having to wait for the next
poll, you can use the following command:
`argocd app sync $APPNAME`

Alternatively, you can set up a webhook in your GitHub repository that is
triggered when a change is detected. The webhook should use the following
URL: https://<argocd>/api/webhook, where <argocd> is the public
domain that points to your Argo CD installation. You can find more
information about webhooks [here](https://argo-cd.readthedocs.io/en/stable/operator-manual/webhook/).

### Argo CD: rollback
You can see the revision history of the application by using the following
command:
`argocd app history flask-app`

You can rollback to a previous revision using the following command:
`argocd app rollback $APPNAME <revision-number>`

However, a rollback cannot be performed against an application with
automated sync enabled. You need to disable automated sync before
performing a rollback.
`argocd app set $APPNAME --sync-policy none`

You can re-enable automated sync after the rollback:
`argocd app set $APPNAME --sync-policy automated`

### Argo CD the declarative way
Previously, we created an application using the following command:
```
argocd app create flask-app \
--repo https://github.com/eon01/argocd-examples/ \
--path flask-app \
--dest-server https://kubernetes.default.svc \
--dest-namespace flask-app \
--revision main \
--sync-policy automated \
--self-heal \
--auto-prune \
--allow-empty
```

This is the imperative way of creating an application, but since we are in a
world of “everything-as-code,” it is also possible to create an application
using a declarative approach. This means that we can define the application
in a manifest file and then apply the manifest file to create the application.

And let’s recreate it using the declarative approach.
check `kubernetes/GitOPs-ArgoCD/app.yml`


### Argo CD: configuration management
If you are continuously deploying applications, you will need to manage the
configuration of your applications. There are several ways to manage the
configuration of your applications. Some of them are native to Argo CD,
like Helm, Jsonnet, and Kustomize, but you can also write your own configuration management plugin and use it with Argo CD.

Helm uses charts to define the structure of the application. A chart is a collection of files that describe a related set of Kubernetes resources.

A Helm chart is composed of the following files:
Chart.yaml: contains the metadata of the chart
values.yaml: contains the default values for the chart
templates/: contains the templates of the Kubernetes resources
_helpers.tpl: contains the helper functions used in the templates
of the Kubernetes resources

Helm uses Go template language to generate Kubernetes resource files
based on the provided values. You can define variables in templates using
the {{ .Values.variableName }} syntax, where variableName
corresponds to a key in the values.yaml file.

Conditionals and loops can be used in templates to generate different
configurations based on certain conditions or to iterate over lists of values.

Helpers are reusable template functions that can simplify complex logic or
calculations. You can define custom helper functions in the _helpers.tpl
file located in the root directory of your chart. Helper functions can be used
in your templates to perform actions like string manipulation, calculations, or conditional checks.

Let’s use Helm with Argo CD in the next examples. We already have
another subfolder in the same GitHub repository that contains a Helm chart.
Let’s update the application to use the Helm chart instead of the Kubernetes
manifests.

**check line 13, in app.yml**
check the helm templates, Chart and values.yml
This is a brief explanation of how the Helm templating language works:
Variables like {{ .Values.replicaCount }} are replaced with the
corresponding values defined in the values.yaml file. The .Values
object allows you to access the values defined in the chart’s
values.yaml file and use them within your templates.
Variables like {{ .Release.Service }} are replaced with the values
from the release object created by Helm. The .Release object provides
access to information about the current release, such as the release
name, release namespace, and release timestamp. The
.Release.Service refers to the service field of the release object
which is set to Helm by default.
Variables like {{ template "flask-app.fullname" . }} are
replaced with the values returned by the helper functions defined in the
_helpers.tpl file. Helper functions allow you to define reusable template logic and call them from within your templates. In this case,
the flask-app.fullname helper function returns the full name of the
application by combining the release name and the chart name.
The “Helm template language” is not exclusive to Helm itself; it
is a combination of the Go template language, additional functions,
and wrappers that provide access to specific objects within the
templates. This means that many resources and guides available for Go
templates can be valuable references when learning about Helm templating.

Currently, we have deployed the application using Helm by utilizing the
following YAML: `kubernetes/GitOPs-ArgoCD/app.yml`


As you can see, the values file that Argo CD will use to deploy the
application is the values.yaml file, which should be provided in the helm
section of the source field.

Alternatively, we can define the values directly in the values field of the
source section.
check `kubernetes/GitOPs-ArgoCD/app.yml`

### Argo CD: managing different environments
As seen previously, you can manage different clusters using the same
instance of Argo CD. This is very useful when you want to manage
different environments of the same application. For example, you can have
a development environment, a staging environment, and a production
environment.

To add a cluster, use the following command:
`export cluster=<cluster-name>`
`argocd cluster add $cluster -y`


For example, we have a production cluster called production and a staging
cluster called staging. We can add them to Argo CD using the following
commands:

`export cluster=production`
`argocd cluster add $cluster -y`

`export cluster=staging`
`argocd cluster add $cluster -y`


In the Argo CD UI, you can see the different clusters in the Settings tab.
Otherwise, list your cluster using:

`argocd cluster list`

Export the name of the cluster you want to use, depending on the
environment to which you want to deploy the application

`export CLUSTER=<cluster-name>`

Deploy the application to that cluster using the following command:
```
piVersion: argoproj.io/v1alpha1
kind: Application
metadata:
name: flask-app
namespace: argocd
spec:
destination:
namespace: flask-app
# $CLUSTER is the name of the cluster you want to deploy the applic\
ation to
server: $CLUSTER
project: default
source:
repoURL: https://github.com/eon01/argocd-examples
targetRevision: main
path: flask-app-helm
helm:
valueFiles:
- values.yaml
syncPolicy:
automated:
prune: true
selfHeal: true
allowEmpty: true
```

Additionally, you can create different values for each environment. For
example, you can create a values-production.yaml file and a values-staging.yaml file. file. Then, you can use the following command to deploy the
application to the production environment:

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
name: flask-app
namespace: argocd
spec:
destination:
namespace: flask-app
# $CLUSTER is the name of the cluster you want to deploy the applic\
ation to
server: $CLUSTER
project: default
source:
repoURL: https://github.com/eon01/argocd-examples
targetRevision: main
path: flask-app-helm
helm:
valueFiles:
- values-production.yaml # or values-staging.yaml ...etc
syncPolicy:
automated:
prune: true
selfHeal: true
allowEmpty: true
```
### Argo CD: deployment hooks

It is possible to define hooks that will be executed before or after the
deployment of the application. For example, you can execute a script that
sends a notification to a Slack channel or an email to your team.
To define a hook, you should define a Job. For instance, you can define a
Job that sends an email

```
kubectl create -f - <<EOF
apiVersion: batch/v1
kind: Job
metadata:
generateName: email-
namespace: argocd
annotations:
argocd.argoproj.io/hook: PostSync
argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
template:
spec:
containers:
- name: email
image: bytemark/smtp
command: ["/bin/sh"]
args: ["-c", "echo 'Hello World!' | mail -s 'Hello World!' <ema\
il>"]
env:
- name: RELAY_HOST
value: <smtp-host>
- name: RELAY_PORT
value: <smtp-port>
- name: RELAY_USERNAME
value: <smtp-username>
- name: RELAY_PASSWORD
valueFrom:
secretKeyRef:
name: smtp-password
key: password
restartPolicy: Never
backoffLimit: 4
---
apiVersion: v1
kind: Secret
metadata:
name: smtp-password
namespace: argocd
type: Opaque
stringData:
password: <smtp-password>
```
Then, you can redeploy the application to trigger the hook:

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
name: flask-app
namespace: argocd
spec:
destination:
namespace: flask-app
server: https://kubernetes.default.svc
project: default
source:
repoURL: https://github.com/eon01/argocd-examples
targetRevision: main
path: flask-app-helm
helm:
valueFiles:
- values.yaml
syncPolicy:
automated:
prune: true
selfHeal: true
allowEmpty: true
```
You should be able to see the Job after executing the previous command:

`kubectl get jobs -n argocd`

As well as the created container logs:
`kubectl logs -n argocd email-<pod-id>-<container-id>`

Same as the above, we can create a Job that will send a notification to a
Slack channel:

```apiVersion: batch/v1
kind: Job
metadata:
generateName: slack-
namespace: argocd
annotations:
argocd.argoproj.io/hook: PostSync
argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
template:
spec:
containers:
- name: slack
image: curlimages/curl
command:
- "curl"
- "-X"
- "POST"
- "--data-urlencode"
- "payload={\"channel\": \"#<channel-name>\", \"username\": \\
"hello\", \"text\": \"App Sync failed\", \"icon_emoji\": \":ghost:\"}"
- "https://hooks.slack.com/services/..."
restartPolicy: Never
backoffLimit: 2```

In addition to PostSync hooks, you can define other hooks such as:
PreSync
SyncFail
Skip
Sync

And instead of HookSucceeded, you can use HookFailed or
BeforeHookCreation.