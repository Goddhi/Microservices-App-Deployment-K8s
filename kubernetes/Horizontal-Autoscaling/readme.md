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
used by HPA and later by the Vertical Pod Autoscaler (VPA).

