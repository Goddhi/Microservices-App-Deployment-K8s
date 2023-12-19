# Observability

### Prometheus
### Prometheus Installation

Clone the Prometheus Operator repository:


### Create the namespace and CRDs:

`git clone https://github.com/prometheus-operator/kube-prometheus.git`

### Create the namespace and CRDs:
`kubectl create -f manifests/setup`

CRD URL
`https://github.com/prometheus-operator/kube-prometheus`

To wait for the CRDs to be created, you can monitor the progress with the
following command:
`until kubectl get servicemonitors --all-namespaces ; do date; sleep 1;echo ""; done`

When you see a No resources found message, it means that the custom
resource definitions (CRDs) were created successfully. Now we can
proceed to create the rest of the components.
`kubectl apply --server-side -f manifests/setup -f manifests`

### Accessing Prometheus web UI

Next, we will create a port-forward to access the Prometheus UI:
`kubectl -n monitoring port-forward svc/prometheus-k8s 9091:9090`
NOTE: it is possible to port-forward a service 

### Metrics available in Prometheus

When you install Prometheus, you will have access to a Prometheus
instance, a Grafana instance, and a set of Prometheus exporters. The
Prometheus Operator also creates kube-state-metrics, which is an add-on
agent that listens to the Kubernetes API server and generates metrics about
the state of Kubernetes objects, such as Nodes, Pods, Deployments, and
more.
We can see a list of available metrics thanks to kube-state-metrics in its
official repository at https://github.com/kubernetes/kube-state-metrics. For
example, metrics for Pods are available here. The following are some
examples of available metrics:
The Pod overhead in regards to
memory associated with running a Pod
kube_node_status_capacity: The total amount of resources available
for a node
kube_pod_overhead_memory_bytes:
In addition to Prometheus metrics, Prometheus Operator also uses other
sources of metrics, such as the Kubernetes API, blackbox exporters, and
node exporters. You can find the list of available metrics in the Prometheus
documentation.
To view a complete list of metrics available in your Prometheus instance,
go to the Prometheus UI and enter the following search query in the search
bar: {__name__=~".+"}. This will display all the available metrics in your
Prometheus instance.
The syntax {__name__=~".+"} is a PromQL expression that allows
you to filter metrics by name.
The =~ operator is a regular expression match operator and it means
that the value of the __name__ label matches the regular expression
".+".
The ".+"
regular expression matches any string with at least one
character.

### Using Grafana to visualize Prometheus metrics

The Prometheus Operator also creates a Grafana instance for visualizing
metrics. To access Grafana, create a port-forward to the Grafana service:

`kubectl -n monitoring port-forward svc/grafana 3001:3000`

To access Grafana on a remote machine, create an SSH tunnel to it from
your local machine. Once the tunnel is established, you can access Grafana
at 
`http://localhost:3001/login`

The default username and password for Grafana are **admin** and **admin**.

Grafana supports multiple data sources, including Prometheus. In this
installation, Prometheus is already configured as a data source. To view the
list of data sources, click on the gear icon on the left panel (Administration),
and then click on Data Sources. You should see Prometheus listed as a data
source

You can customize your dashboards by adding new ones or importing
dashboards from Grafana.com.
To add a new dashboard, click on the plus icon on the left panel and then
click on “Add visualization”
. Choose Prometheus as the data source and
type a PromQL expression in the query field. For example, to visualize the
memory usage of our containers, type container_memory_usage_bytes.
Click on the “Run query” button to view the results.

To add a dashboard from Grafana.com, follow these steps:

1. Click on the plus icon on the left panel.
2. Click on Import.
3. In the “Import via grafana.com” section, type 1860 in the “Grafana
Dashboard” field and click on Load.
4. Choose Prometheus as the data source.
5. Click on Import to import the dashboard.

To visualize **logs**, we can create a dashboard. First, click on the plus icon in the left panel, then click on Import. In the Import via grafana.com section, type 15141 in the Grafana.com Dashboard field and click on Load. Choose Loki as the data source, and click on Import to load the Loki Kubernetes Logs dashboard.

You can view other available dashboards on Grafana.com by clicking here.