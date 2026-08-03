# Minimal ROS2 image containing this chapter's talker/listener pair.
#
# Layer ordering matters for build speed (see DEEP_DIVE.md): the apt
# install step comes before COPYing our own source, so editing
# talker.py/listener.py and rebuilding doesn't re-run the apt install —
# Docker reuses that cached layer since its inputs (this Dockerfile's
# instructions above it) haven't changed.

FROM ros:jazzy

# No extra apt packages needed for this simple demo beyond the ros:jazzy
# base image's own ROS2 install — this RUN is a placeholder showing
# WHERE dependency installs belong (before COPYing source), for a real
# project that does need extra packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY talker.py listener.py ./

# Source ROS2's setup script in every shell this image's ENTRYPOINT
# spawns, so `ros2` and rclpy imports work without the user needing to
# remember to source it manually inside the container.
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["/bin/bash", "-c", "source /opt/ros/jazzy/setup.bash && exec \"$@\"", "--"]

# No CMD here — docker-compose.yaml supplies which script (talker.py or
# listener.py) each service actually runs, since both containers share
# this one image.
