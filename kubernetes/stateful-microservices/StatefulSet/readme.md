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

### Check the StatefulSet:
`kubectl get statefulset -n postgres`

If you delete and recreate the StatefulSet, the Pods will have the same identifiers.

### Creating a Service for the StatefulSet
StatefulSets require a Headless Service. As a reminder, Kubernetes allows clients to discover Pods IPs through DNS lookups and this is possible thanks to the Headless Service. Without a Headless Service, the Pods IPs cannot be discovered directly, instead the DNS server returns a single IP which is the IP of the Service itself. The Service then may load-balances the traffic to the underlying Pods.

check `Statefulset/postgres-headless-service.yaml`
Then, create the Headless Service:
`kubectl apply -f postgres-headless-service.yaml`

### Post deployment tasks
Now that we have a new StatefulSet, we need to recreate the database schema and apply any SQL migrations.

`export pod=$(kubectl get pods -n stateful-namespace -l app=stateful-flask -o jsonpath='{.items[0].metadata.name}')`

`kubectl exec -it $pod -n stateful-namespace -- flask db init`
`kubectl exec -it $pod -n stateful-namespace -- flask db migrate`
`kubectl exec -it $pod -n stateful-namespace -- flask db upgrade`

Finally, check that the application is working:
curl -X POST -H "Content-Type: application/json" -d '{"title": "New task", "description": "Goddhi is fvcking good!!!!!"}' "http://drexii.me/tasks"

You can also delete and then recreate the StatefulSet and check that the data is persisted.

`kubectl delete -f kubernetes/postgres-statefulset.yaml`
`kubectl apply -f kubernetes/postgres-statefulset.yaml`

### StatefulSet vs Deployment: persistent storage
The Deployment will work fine, but it’s not the best way to persist data.
Once we scale the Deployment, the new Pods may not have access to the same PersistentVolumeClaim. This means that the new Pods will not have access to the same data. If you look back at the PersistentVolumeClaim, you will notice that we used:
```
accessModes:
- ReadWriteOnce
```

This means that the PersistentVolumeClaim can only be mounted as read-
write by a single node. Therefore, the new Pods created on new nodes may
not have access to the same PersistentVolumeClaim.

What if we change the accessModes to ReadWriteMany?

```
accessModes:
- ReadWriteMany
```
In order to avoid these problems and because we don’t want to manage data
concurrency at the application level, we will use VolumeClaimTemplates.
This is how we did in the StatefulSet manifest file:

```
volumeClaimTemplates:
- metadata:
name: postgredb-volume
spec:
accessModes: [ "ReadWriteOnce" ]
storageClassName: "do-block-storage"
resources:
requests:
storage: 5Gi
```
The VolumeClaimTemplates will request a PersistentVolumeClaim from
the StorageClass dynamically. If you have “x” Pods, the StatefulSet will
create “x” PersistentVolumeClaims, each with a name in the following format:
`<volumeClaimTemplate-name>-<pod-name>-<ordinal-index>`

When we delete the StatefulSet, the volumes associated with it will not be deleted. The Pod that was using a PersistentVolumeClaim will reuse the same volume when the StatefulSet is recreated.
This is done to ensure data safety and integrity.

### StatefulSet vs Deployment: associated service
In the very first example of the PostgreSQL Deployment, we create a ClusterIP, this is because we needed to create a Service for the Deployment that is accessible only from within the cluster. 


However, in the StatefulSet manifest file, we not only needed to access the
PostgreSQL Pod using a Service, but we also wanted to be able to scale the  number of Pods without impacting the data integrity, such as concurrent
read-write of the same file.
To solve this issue, we utilized StatefulSet and VolumeClaimTemplates to
allow all Pods to share the data directory /var/lib/postgresql/data.
However, accessing the Pods through a Service remained problematic. The
regular Kubernetes implementation of a Service does not work with
PostgreSQL because it uses a load balancer or proxy to direct traffic to the
Pods. Instead, each Pod must be discovered directly by the client. This is
why we employed a Headless Service.
Using a Headless Service ensures that the stateful application functions
properly by providing a stable network identity for the database cluster.
Even if something unexpected happens, such as the failure of a Pod and the
provisioning of a new one with a new IP address, the Headless Service
ensures that the new Pod has a stable network identity.


**OBSERVATION**:
Always make sure the number of deployment pods(appplication-pod) is same with the number statefulset pods(postgres-pod).. anything aside that an error will be prompted whem you curl the application url in this case http://drexii.me/tasks



No, a Service of type `ExternalName` in Kubernetes does not have an endpoint in the traditional sense that other Service types (like `ClusterIP`, `NodePort`, or `LoadBalancer`) do. Instead, `ExternalName` services provide a way to return an alias to an external service. 

When a DNS query is made for an `ExternalName` service, Kubernetes DNS (CoreDNS or Kube-DNS) returns a CNAME record with the value of the `externalName`. This DNS resolution directs network traffic directly to the specified external service, bypassing the usual in-cluster service routing mechanisms.

Here's a quick overview of how `ExternalName` services work:

1. **Definition**: In the definition of an `ExternalName` service, you specify an `externalName` which is the DNS name of the external service you want to point to.

   Example:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: my-service
   spec:
     type: ExternalName
     externalName: my.external-service.com
   ```

2. **DNS Resolution**: When a pod in the Kubernetes cluster looks up `my-service`, the cluster DNS returns a CNAME record pointing to `my.external-service.com`. 

3. **No Endpoints**: Unlike other service types, there is no list of pod IP addresses or a selector for pod matching. No endpoints are created or maintained for `ExternalName` services.

4. **Direct Traffic**: Any connection or request to `my-service` in the cluster is directed to `my.external-service.com` based on the DNS response.

### Use Cases for `ExternalName` Services

- **Simplifying Access to External Resources**: They are commonly used to provide an in-cluster DNS alias to an external service, like a database or an API that is hosted outside of the Kubernetes cluster.

- **Service Migration**: `ExternalName` services can also be useful during service migrations, allowing you to switch the backend without changing the DNS name that applications use to access the service.

### Limitations

- **Protocol and Port Specification**: An `ExternalName` service does not allow you to specify a port or protocol. The application must know and specify the port to use.

- **No Load Balancing or Health Checks**: Since it's just a DNS alias, there's no load balancing or health checks done by Kubernetes.

Remember, the use of `ExternalName` services is subject to the usual DNS limitations and behaviors, and it's essential to ensure that the external DNS name is resolvable from within the cluster.