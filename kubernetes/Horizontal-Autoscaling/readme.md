### Horizontal Pod Autoscaler
Kubernetes offers automatic scaling as a feature, allowing a workload
resource like a StatefulSet or Deployment to adjust to changing demand.
Known as Horizontal Pod Autoscaling (HPA), this feature scales the
workload up or down based on metrics monitored by the HPA controller.

The HPA adds more Pods to the workload to respond to increased load.
To use HPA, a metric server must be running in the cluster. This server is
responsible for aggregating resource usage data across the cluster. The
metric server collects metrics from various resources and exposes them
through the Kubernetes apiserver via the Metrics API. These metrics are
used by HPA and later by the Vertical Pod Autoscaler (VPA)....

### Setting up HPA on minikube cluster
`minikube enable addons metrics-server `

To create the  metrics-server  when using a single master node, execute this command.

`kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`

Utilize either  `kubectl top nodes`  or  `kubectl top pods -A`  to obtain a result of cpu and memory utilization:

Next, we will create a Horizontal Pod Autoscaler (HPA) for the API. The
HPA will scale the API based on CPU usage. If the CPU usage exceeds
20%, the HPA will add more Pods. If the CPU usage falls below 20%, the
HPA will remove Pods.

check `kubernetes/Horizon-Autocaling/hpa.yml`

You can see the HPA by running the following command:
`kubectl get hpa -n stateful-namespace`

Let’s stress the API to see how the HPA works. Run the following
command:

`kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://drexii.me/tasks; done"`

we are scaling based on CPU usage. We instruct the
HPA to scale when CPU usage exceeds 20% of the requested CPU. Instead
of using Utilization, we can opt to use AverageValue or Value.
The AverageValue is calculated by dividing the value returned by the
metrics server by the number of Pods in the scale target.
Value is the raw value as returned by the metrics server.

```
kind: HorizontalPodAutoscaler
metadata:
name: stateful-flask-hpa-custom
namespace: stateful-flask
spec:
scaleTargetRef:
apiVersion: apps/v1
kind: Deployment
name: stateful-flask
minReplicas: 1
maxReplicas: 10
metrics:
- type: Resource
resource:
name: cpu
target:
type: AverageValue
averageValue: 45m
```

When target.type is set to AverageValue or Value, we need to use values
(e.g. 45m), unlike the previous example where we used a percentage ( 20).
Kubernetes supports the following metric types by default:
cpu: the CPU usage of the Pods in the scale target.
memory: the memory usage of the Pods in the scale
target.
They are both called Resource metrics.
Kubernetes also supports other non-resource metrics types:
the number of objects in a Kubernetes object store, as
reported by a metrics adapter.
Pods: the number of Pods in the scale target.
External: a metric from an external metrics provider.

### Autoscaling based on more specific custom Kubernetes metrics