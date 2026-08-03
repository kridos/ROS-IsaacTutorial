# Demo: Containerized Talker/Listener

## Prerequisites

Docker (and Docker Compose, bundled with modern Docker installs as
`docker compose`).

## How to run

```bash
docker compose up --build
```

## Expected output

Interleaved logs from both containers, prefixed with the service name:

```
talker-1    | [INFO] [talker]: Publishing: 'Hello from container! count=0'
listener-1  | [INFO] [listener]: I heard: "Hello from container! count=0"
talker-1    | [INFO] [talker]: Publishing: 'Hello from container! count=1'
listener-1  | [INFO] [listener]: I heard: "Hello from container! count=1"
...
```

The listener container receiving messages from the talker container
confirms DDS discovery is working across the container boundary — thanks
to `network_mode: host` in `docker-compose.yaml` (see DEEP_DIVE.md).

## Try it: break the pitfall on purpose

Comment out (or remove) `network_mode: host` from both services in
`docker-compose.yaml`, then re-run:

```bash
docker compose up --build
```

Expected: both containers start and log no errors — `talker-1` keeps
publishing, but `listener-1` never logs a single `I heard` line. This is
DEEP_DIVE.md's common pitfall happening live: Docker's default bridge
network doesn't pass DDS discovery traffic between the two containers,
so they simply never find each other, with nothing in the logs pointing
directly at network configuration as the cause.

## Inspect a running container

```bash
docker exec -it chatter_listener bash
source /opt/ros/jazzy/setup.bash
ros2 node list
```

Expected (with `network_mode: host` restored): shows both `/talker` and
`/listener`, confirming the containerized nodes are visible to each
other exactly as two plain host processes would be.
