### Canary Deployment with Istio

`curl -L https://istio.io/downloadIstio | sh -`

`cd istio-1.19.3`
`export PATH=$PWD/bin:$PATH`

`istioctl install --set profile=demo -y`

`istioctl verify-install`
### cretating namespace
`kubectl create ns canary`

### configuring istio, sidecar containers automatically deployed to all pods in canary namespace
`kubectl label namespace canary isito-injection=enabled `

### first version of the application:
`kubernetes/stateful-microservices/stateful-app-deployment.yml`

### second version of the application

`kubernetes/Canary-Deployment-Istio/stateful-app-deployment.yml`

We will use the following service to expose the application:

check `kubernetes/Canary-Deployment-istio/svc.yml`

Label the namespace with istio-injection=enabled 
Hereafter any pods started in this namespace will
have Envoy sidecars injected automatically
`kubectl label namespace canary istio-injection=canary`

Check which namespaces have istio injection enabled
`kubectl get namespace -L istio-injection`

