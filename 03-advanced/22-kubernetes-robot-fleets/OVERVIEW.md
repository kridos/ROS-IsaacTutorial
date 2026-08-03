# Chapter 22: Orchestrating Robot Fleets with Kubernetes

## What this is

**Kubernetes** runs and manages many containers across potentially many
machines: scheduling them onto available hardware, restarting them if
they crash, and giving them stable network identities. Where Chapter 21's
Docker/docker-compose managed a handful of containers on one machine,
Kubernetes manages containers at fleet scale, across a cluster.

## Why it matters

A single robot's onboard software is usually just Docker (Chapter 21) —
Kubernetes isn't for that. It matters once you have *many* robots, or
many simulation/training jobs, that need to be managed, restarted on
failure, and scheduled onto available compute as a fleet — genuinely
different scale of problem than one robot's own software stack.

## Where this fits

Directly extends Chapter 21's Docker image and its DDS-networking
lesson — the same "check networking before assuming a ROS2 bug" habit
from Chapters 2, 7, 9, 10, 14, and 21, now applied one layer up at the
cluster-networking level.

## What the demo shows

Chapter 21's talker/listener Docker image, deployed as two Kubernetes
Deployments on a local single-node cluster (via `kind`), configured so
DDS discovery works between them — with `kubectl` as the primary tool
for observing and managing what's running, mirroring the role `ros2` CLI
tools and `docker`/`docker compose` played in earlier chapters.
