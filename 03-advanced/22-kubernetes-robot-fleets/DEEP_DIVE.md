# Chapter 22 Deep Dive: Kubernetes for Robot Fleets

## Core vocabulary

- **Pod**: the smallest deployable unit in Kubernetes — one or more
  containers that are always scheduled together onto the same cluster
  node, sharing a network namespace. Conceptually similar to a
  docker-compose service group, but scheduled onto whichever cluster
  node has room, rather than always running on your local machine.
- **Deployment**: declares "keep N replicas of this Pod spec running." If
  a Pod crashes or its node fails, the Deployment's controller notices
  and starts a replacement automatically. This is the capability Chapter
  21's docker-compose doesn't have — `docker compose up` starts
  containers, but nothing restarts them onto different hardware if the
  machine they were on goes away; a Kubernetes Deployment does.
- **Service**: a stable network name/address for a set of Pods. Pods are
  ephemeral — a replacement Pod gets a new IP — so anything that needs to
  reliably reach "the talker," rather than one specific Pod instance,
  addresses it through a Service instead of a Pod's IP directly. (This
  chapter's demo doesn't need one, since both Deployments use host
  networking and reach each other via DDS discovery directly, not via a
  Kubernetes Service — worth knowing Services exist for the more typical
  case of a Kubernetes-networked, non-host-network application.)
- **Namespace**: Kubernetes' own namespacing concept, grouping related
  resources — conceptually parallel to, but a completely separate
  mechanism from, Chapter 19's ROS2 namespaces. This chapter's demo uses
  a `ros2-demo` Kubernetes namespace purely to group its own resources
  cleanly, unrelated to any ROS2-level namespacing.

## DDS discovery across a cluster: a real practical hurdle

DDS's default discovery relies on multicast traffic (same underlying
mechanism Chapter 21's Docker networking pitfall involved) — most
Kubernetes cluster networking setups (the CNI, Container Network
Interface, plugin managing pod-to-pod networking) **don't** pass
multicast through by default, for the same reasons Docker's default
bridge network doesn't. At real multi-node cluster scale, this is a
genuine, actively-discussed problem in the ROS2/Kubernetes community, with
two common practical fixes: switching DDS to a **discovery server**
(unicast-based discovery instead of multicast — most DDS
implementations support this as a configuration option) rather than
relying on multicast at all, or choosing/configuring a CNI plugin that
specifically supports multicast. This chapter presents this as "the
concept and vocabulary to search for," not a fully worked production
setup — genuinely getting this right for a multi-node production cluster
is more involved than a learning chapter can responsibly compress.

## kubectl

`kubectl` is Kubernetes' primary CLI, mirroring the role `ros2` CLI tools
and `docker`/`docker compose` played in earlier chapters:

- `kubectl apply -f <file>.yaml` — creates or updates resources
  described in a YAML file (the declarative model: you describe desired
  state, Kubernetes reconciles toward it, rather than issuing imperative
  "start this" commands).
- `kubectl get pods -n <namespace>` — lists running Pods and their
  status.
- `kubectl logs <pod-name> -n <namespace>` — same role as `docker logs`
  or a terminal running a ROS2 node directly.
- `kubectl describe pod <pod-name> -n <namespace>` — detailed status,
  including recent events — the first thing to check when a Pod won't
  start or keeps restarting.

## Running a local cluster for learning

Most readers won't have a real multi-machine cluster available. **`kind`**
(Kubernetes IN Docker) runs a full Kubernetes cluster as Docker
containers on your own machine — enough to learn and exercise real
`kubectl`/Deployment/Service concepts without needing actual cluster
hardware. (`minikube` is a similar, commonly-used alternative.)

## Common pitfall

The multicast/DDS-discovery gap described above gets mistaken for "ROS2
is broken" more often than it gets correctly identified as a cluster
networking configuration gap — a Pod's logs show the node started
cleanly, `kubectl get pods` shows everything `Running`, yet two
Deployments' ROS2 nodes never discover each other. This is the same
"check networking/discovery before assuming a ROS2 bug" lesson from
Chapters 10 and 21, now one layer up the infrastructure stack — worth
checking cluster networking/CNI multicast support specifically before
assuming a code-level ROS2 problem when Pods that should be talking to
each other aren't.
