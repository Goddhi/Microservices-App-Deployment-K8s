# Observability

### Prometheus
### Prometheus Installation

Clone the Prometheus Operator repository:


### Create the namespace and CRDs:

`git clone https://github.com/prometheus-operator/kube-prometheus.git`

### Create the namespace and CRDs:
`kubectl create -f manifests/setup`

To wait for the CRDs to be created, you can monitor the progress with the
following command:
`until kubectl get servicemonitors --all-namespaces ; do date; sleep 1;echo ""; done`


When you see a No resources found message, it means that the custom
resource definitions (CRDs) were created successfully. Now we can
proceed to create the rest of the components.

`kubectl create -f manifests/`

### Accessing Prometheus web UI

Next, we will create a port-forward to access the Prometheus UI:

`kubectl -n monitoring port-forward svc/prometheus-k8s 9090 > /dev/null \
2>&1 &`

`kubectl -n monitoring port-forward svc/prometheus-k8s 9090 > /dev/null 2>&1 &`

`kubectl apply --server-side -f manifests/setup -f manifests`


### 
kubectl apply --server-side -f manifests/setup -f manifests