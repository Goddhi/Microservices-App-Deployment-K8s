check `/kubernetes/stateful-microservices/stateful-flask-service-externalname.yml`

# Resource management and risks: from Docker to Kubernetes
If you have used standalone Docker containers, you are probably aware of
the risks associated with not properly allocating memory and CPU
resources. If you have not, you may be surprised when your containers
crash due to running out of memory or CPU.
Containers running on a host should not consume excessive memory, as the
kernel may activate an Out Of Memory exception and start killing
processes, including the Docker daemon itself. Docker attempts to prevent
this by adjusting the OOM priority on the daemon, making it less likely to
be killed. However, this does not apply to container processes, which are
more likely to be killed.
It is therefore recommended to limit container access to the host’s
resources. Here are some examples:
1
2
3
4
5
6
# guarantees the container at most 50% of the CPU every second.
docker run -it --cpus=".5" ubuntu /bin/bash
# limit the maximum amount of memory the container can use to 256 megab\
ytes.
docker run -it --memory=256m ubuntu /bin/bash
If the node where a Pod is running has enough of a resource available, it’s
possible (and allowed) for a container to use more resources than its request
for that resource specifies. However, a container is not allowed to use more
than its resource limit.


If the node where a Pod is running has enough of a resource available, it’s
possible (and allowed) for a container to use more resources than its request
for that resource specifies. However, a container is not allowed to use more
than its resource limit.

## Requests and limits



If the node on which a Pod is running has enough of a resource available, a
container can use more of that resource than its request specifies. However,
a container is not allowed to use more than its resource limit.
The Kubernetes scheduler uses requests and limits to determine which
node to place a Pod on. It attempts to fit the total of the resource requests
for all scheduled containers onto available nodes. For example, if a Pod has
a CPU request of 100m and a memory request of 200Mi, the scheduler will
not place it on a node with less than 100m of CPU and 200Mi of memory
available.