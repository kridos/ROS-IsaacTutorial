# Chapter 21 Deep Dive: Containerized Robotics (Docker)

## Building a ROS2-based image

A typical ROS2 Dockerfile starts from an official ROS2 base image
(`FROM ros:jazzy`), installs any additional apt/pip dependencies, copies
in your code, and (for a full colcon workspace) builds it:

```dockerfile
FROM ros:jazzy
RUN apt-get update && apt-get install -y <extra-packages> && rm -rf /var/lib/apt/lists/*
COPY talker.py listener.py /app/
WORKDIR /app
```

This chapter's demo keeps it simple (plain scripts, no colcon workspace,
matching Chapters 2-3's copy-paste-runnable Python style) — a real
project's Dockerfile would typically also `COPY` a `src/` workspace
directory and run `colcon build` as part of the image build.

## Layer caching and Dockerfile ordering

Docker builds an image as a stack of **layers**, one per instruction, and
caches each layer — if a layer's inputs haven't changed since the last
build, Docker reuses the cached result instead of re-running that
instruction. This means **instruction order matters for build speed**:
put steps that change rarely (installing system/apt dependencies) before
steps that change often (copying your own source code), so an edit to
your Python file only invalidates the cache from that `COPY` onward,
not the potentially-slow apt install steps above it. Reversing this order
(copying source first, installing dependencies after) works correctly
but rebuilds the dependency-install layer on every single code change,
needlessly slowing down iteration.

## Running GUI tools from a container

RViz2 or Gazebo running inside a container still need to open a window
on your actual display — this requires forwarding X11 (the Linux display
protocol) into the container, typically via `--net=host` (simplest, but
shares the container's networking with the host entirely) plus mounting
`/tmp/.X11-unix` and setting the `DISPLAY` environment variable, or a
more locked-down `xhost`-based approach for tighter access control. This
is a known, solvable problem with several documented approaches
depending on how much isolation you want — worth knowing it exists and
requires deliberate setup, rather than expecting a GUI tool to "just
work" in a container the way a headless node does.

## docker-compose for multi-container systems

`docker-compose.yaml` describes multiple containers (services) and how
they relate — this chapter's demo runs talker and listener as two
separate services, each built from the same image, started together with
one `docker-compose up`. This is the container-level analogue of Chapter
19's multi-robot namespacing: instead of separating concerns by ROS2
namespace within one process tree, you separate them by container
entirely — and the two approaches compose (a real multi-robot system
might run each robot's stack in its own container, each internally
namespaced too).

Containers on the same DDS domain still discover each other the same way
any two ROS2 processes would (per Chapter 10 — DDS discovery doesn't
care whether two participants are in the same container, different
containers, or different physical machines), **provided the network
configuration actually lets their discovery traffic through** — which is
the pitfall below.

## Common pitfall: default bridge networking breaks DDS discovery

Docker's **default bridge network** isolates each container's network
somewhat from the others — critically, it typically doesn't pass through
the multicast traffic DDS's default discovery mechanism relies on to find
other participants. Two ROS2 nodes in two containers on Docker's default
network can both start successfully, show no errors, and simply never
discover each other — `ros2 node list` inside either container shows
only that container's own node. This is yet another instance of the
"everything looks fine, nothing connects" pattern from Chapters 2, 7, 9,
10, and 14, now at the container-networking layer.

**Fix used in this chapter's demo**: `network_mode: host` in
`docker-compose.yaml` (the compose equivalent of `docker run --net=host`)
— containers share the host's network stack directly, so multicast
discovery works exactly as it would between two processes running
directly on the host. This is the simplest fix and what this chapter
uses; it does give up Docker's network isolation between containers,
which is a real trade-off for genuinely multi-tenant/security-sensitive
setups (not a concern for this chapter's demo, but worth knowing before
assuming host networking is always the right default).
