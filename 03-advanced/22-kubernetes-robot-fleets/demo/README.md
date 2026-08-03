# Demo: Kubernetes Robot Fleet (talker/listener on a local cluster)

## Prerequisites

- Docker.
- `kind` (Kubernetes IN Docker): https://kind.sigs.k8s.io/ install docs.
- `kubectl`.

## Create a local cluster

```bash
kind create cluster --name ros2-demo
```

## Build and load the image

Reuses Chapter 21's Dockerfile/talker.py/listener.py directly:

```bash
docker build -t ros2-chatter-demo:latest ../../21-containerized-robotics-docker/demo
kind load docker-image ros2-chatter-demo:latest --name ros2-demo
```

(`kind load docker-image` is required because `kind`'s cluster nodes run
in their own Docker containers with their own separate image cache — a
locally-built image isn't automatically visible inside the cluster
without this step, which is also why `imagePullPolicy: Never` is set in
both Deployment YAMLs: it tells Kubernetes to use the loaded image
directly rather than trying to pull it from a registry.)

## Deploy

```bash
kubectl apply -f namespace.yaml
kubectl apply -f talker-deployment.yaml
kubectl apply -f listener-deployment.yaml
```

## Check status

```bash
kubectl get pods -n ros2-demo
```

Expected: two Pods, both `Running`:

```
NAME                        READY   STATUS    RESTARTS   AGE
talker-xxxxxxxxxx-xxxxx     1/1     Running   0          10s
listener-xxxxxxxxxx-xxxxx   1/1     Running   0          10s
```

## Check the logs

```bash
kubectl logs -n ros2-demo -l app=talker --tail=5
kubectl logs -n ros2-demo -l app=listener --tail=5
```

Expected: the talker Pod's logs show `Publishing: ...` lines; the
listener Pod's logs show matching `I heard: ...` lines — confirming DDS
discovery worked between the two Pods thanks to `hostNetwork: true` (see
DEEP_DIVE.md).

## Try it: break the pitfall on purpose

Remove `hostNetwork: true` and `dnsPolicy: ClusterFirstWithHostNet` from
both YAML files, re-`kubectl apply -f` both, and delete+recreate the
Pods (`kubectl delete pods -n ros2-demo -l app=talker` and same for
`listener`, letting the Deployment recreate them). Expected: both Pods
still report `Running` with no errors, but the listener's logs stay
empty — the cluster-networking version of DEEP_DIVE.md's multicast
pitfall, happening live.

## Clean up

```bash
kind delete cluster --name ros2-demo
```
