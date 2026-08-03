# Chapter 21: Containerized Robotics (Docker)

## What this is

**Docker** packages an application together with its exact dependency
versions (OS libraries, ROS2 distro, Python packages) into a single,
portable image that runs identically wherever Docker runs — a dev
laptop, a CI server, or a robot's onboard computer.

## Why it matters

"Works on my machine" is a real, recurring problem in robotics: a
specific ROS2 distro, specific driver versions, and specific package
versions all need to line up, and that alignment is easy to lose as a
project grows or moves between machines. Chapter 15 already mentioned
that Isaac ROS itself ships this way, specifically because of how tightly
version-coupled it is — this chapter covers the general pattern properly.

## Where this fits

Uses Chapter 2's talker/listener as the payload (copied into this
chapter's own files, for reasons explained in DEEP_DIVE.md) — the ROS2
content here is intentionally familiar, so the new material is purely
about the containerization layer around it.

## What the demo shows

A Dockerfile building a minimal ROS2 image containing the talker/listener
pair, and a `docker-compose.yaml` running them in separate containers on
a shared network — demonstrating both how to containerize a ROS2 node
and the specific networking configuration DDS discovery needs to work
across container boundaries.
