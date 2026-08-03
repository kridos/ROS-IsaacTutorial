# Practice: Containerized Robotics (Docker)

1. **Add a real dependency.** Add `numpy` to the Dockerfile's apt/pip
   install step (in the correct layer-ordering position, per
   DEEP_DIVE.md), and modify `talker.py` to use it for something trivial
   (e.g. compute the message count using a numpy array) — confirm the
   image rebuilds correctly and the layer-caching behavior matches what
   DEEP_DIVE.md describes when you edit `talker.py` afterward.

2. **Time the cache.** Do a clean `docker compose build`, note the time,
   then touch only `talker.py` and rebuild — time that too. Then
   deliberately reorder the Dockerfile (COPY before the apt RUN step)
   and repeat both timings. Compare all four numbers against
   DEEP_DIVE.md's claim about instruction ordering.

3. **Break the pitfall, verify the fix.** Do demo/README.md's
   "Try it: break the pitfall on purpose" exercise, then apply the fix
   (`network_mode: host`) yourself instead of just reverting the change,
   and confirm messages flow again.

4. **A third service.** Add a `monitor` service to `docker-compose.yaml`
   that runs `ros2 topic hz /chatter` in a loop, confirming a third
   container can observe traffic between the other two without being
   either publisher or subscriber.

5. **Stretch:** containerize Chapter 6's `noisy_sensor_publisher.py`
   instead of the talker/listener pair, and add a volume mount so
   `ros2 bag record` output (run from inside the container) lands on
   your host filesystem instead of disappearing when the container stops.
