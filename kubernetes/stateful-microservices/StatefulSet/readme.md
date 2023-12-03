# Deploying Stateful Microservices: StatefulSets
When running stateful applications in Kubernetes, it is crucial to ensure
stability, scalability, and data integrity. The stateful application must:

Run in a stable and reliable manner.
Be scalable up and down without data loss.
Be upgradable without data loss.
Be rolled back to a previous version without data loss.
Be restartable without data loss.

StatefulSets are API objects in Kubernetes that are designed to manage stateful applications such as databases. They provide features such as scalability and upgradeability while preserving the ordering and uniqueness of the Pods.

In summary, StatefulSets are useful for applications that require specific
features such as unique and stable network identifiers, persistent storage
that remains unchanged when Pods are restarted, and a way to deploy and scale in a specific order.

### StatefulSet vs Deployment
A StatefulSet assigns a unique and persistent identifier to each Pod, unlike a
Deployment. This allows the Pod to maintain its identity even when
rescheduled. StatefulSets are particularly well-suited for workloads that
require persistence through the use of storage volumes.

The persistent identifiers assigned to the Pods make it easier to match the
volumes to the Pods that replace any that have failed, ensuring that data is
not lost in case of failure.
If an application does not require unique and stable network identifiers and
persistent storage that does not change when Pods are restarted, it is better
to use a Deployment instead.


### Creating a StatefulSet
In the previous examples, we deployed a stateful PostgreSQL database
using a Deployment. In this example, we will deploy the same database
using a StatefulSet instead. The StatefulSet is more suitable for our use case since we are running a persistent PostgreSQL database.

Before proceeding, delete the Deployment and the Service that we created in the previous example.

 `kubectl delete -f kubernetes/postgres-deployment.yaml`
 `kubectl delete -f kubernetes/postgres-service.yaml`

We can also delete the Volume and PersistentVolu
`kubectl delete -f kubernetes/postgres-pvc-pv.yaml`

Now, create the following StatefulSet manifest file:

check `Stateful/postgres-statefulset.yaml`

Then, create the StatefulSet:
`kubectl apply -f kubernetes/postgres-statefulset.yaml`
