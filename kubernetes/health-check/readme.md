
# Setting up Health Check
check deployment file `(kubernetes/stateful-microservices/stateful-app-deployment.yml)`



Health checks are a way to monitor the health of a microservice. They are
used by the infrastructure to determine if a microservice is healthy or not. If
a microservice is not healthy, it is cut off from the network and no longer
receives requests.


The initialDelaySeconds field is used to specify the number of
seconds to wait before executing the first probe. The default value is 0
seconds.
The periodSeconds field is used to specify the number of seconds to
wait between each probe. The default value is 10 seconds.
The timeoutSeconds field is used to specify the number of seconds to
wait for a probe to succeed before considering it failed. The default
value is 1 second.
The successThreshold field is used to specify the number of
consecutive successful probes before considering the container alive or
ready. The default value is 1.
The failureThreshold field is used to specify the number of
consecutive failed probes before considering the container dead or not
ready. The default value is 3.
The terminationGracePeriodSeconds field is used to specify the
number of seconds to wait before terminating a container after it
receives a SIGTERM signal. The default value is 30 seconds. This can
be set at the Pod level or at the container’s probe level. If set at the
probe level, it overrides the value set at the Pod level.