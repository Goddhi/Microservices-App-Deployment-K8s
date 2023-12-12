## Scaling Stateful Microservices: PostgreSQL as an Example

For example, if we create an entry in the database using an API POST
request that is sent to the first replica, scaling the StatefulSet to 2 replicas
could result in a GET request being sent to the second replica before the
data is replicated. This would cause an error.

There are different tools and techniques available to solve the problem of data consistency.

Although it may seem easy on the surface, data consistency is actually a
complex problem. Therefore, it is better to use a stable tool that is already
available and maintained by a community, rather than reinventing the
wheel.

When it comes to Kubernetes, there are multiple tools we can use:

Patroni: PostgreSQL cluster using streaming
replication
Zalando PostgreSQL Operator: Postgres operator creates and manages
PostgreSQL clusters running in Kubernetes
PostgreSQL HA packaged by Bitnami: This PostgreSQL cluster
solution includes the PostgreSQL replication manager, an open-source
tool for managing replication and failover on PostgreSQL clusters.
PGO: Production PostgreSQL for Kubernetes, from high availability
Postgres clusters to full-scale database-as-a-service.
Stolon: PostgreSQL cloud native High Availability and more. And more

### Stolon: introduction
Stolon is a cloud-native PostgreSQL manager for high availability. It allows
you to maintain a highly available PostgreSQL instance within your
containers (with Kubernetes integration) as well as on other types of
infrastructure, such as cloud IaaS and old-style infrastructures.

- **Keeper**: It manages a PostgreSQL instance, converging to the
“clusterview” computed by the leader sentinel.
- **Sentinel**: It discovers and monitors keepers and proxies, and computes
the optimal “clusterview”.
- **Proxy**: The client’s access point. It enforces connections to the right
PostgreSQL master and forcibly closes connections to old masters.
![stlon-image](kubernetes/Scaling-Stateful-Microservices/stolon.png)

STOLON

Leverages PostgreSQL streaming replication.
Resilient to any kind of partitioning, it prefers consistency over
availability while trying to maintain maximum availability.

Provides Kubernetes integration for achieving PostgreSQL high
availability.
Uses a cluster store such as etcd, Consul, or Kubernetes API server as
a highly available data store and for leader election.
Supports asynchronous (default) and synchronous replication.
Allows for full cluster setup in minutes and easy cluster
administration.
Can perform point-in-time recovery by integrating with your preferred
backup/restore tool.
Supports standby cluster for multi-site replication and near-zero
downtime migration.
Offers automatic service discovery and dynamic reconfiguration,
handling PostgreSQL and Stolon processes changing their addresses.
Can use pg_rewind for fast instance resynchronization with the current
master.

Stolon: installation

kubectl run -i -t stolonctl --image=sorintlab stolon:master-pg10 --restart=Never --rm -- /usr/local/bin/stolonctl --cluster-name=minikube --kube-resource-kind=configmap init

ddd