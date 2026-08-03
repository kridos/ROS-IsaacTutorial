# Practice: ROS2 Architecture (DDS, QoS)

1. **Add durability to the mix.** Extend `qos_publisher.py`/
   `qos_subscriber.py` with a third CLI option controlling Durability
   (`VOLATILE` vs `TRANSIENT_LOCAL`) in addition to Reliability. Confirm
   a `TRANSIENT_LOCAL` publisher lets a subscriber that starts *after*
   the first message was published still receive it — the property
   Chapter 8's `StaticTransformBroadcaster` relies on.

2. **History depth in action.** Set the publisher to burst 20 messages
   instantly (a tight loop, no timer) with `KEEP_LAST` depth 3, and a
   subscriber that sleeps for a second before processing each message.
   Confirm the subscriber only ever sees the 3 most recent messages from
   each burst, not all 20 — a concrete look at what "history depth"
   actually drops.

3. **Diagnose a mismatch blind.** Have a partner (or your future self,
   a day later) set up a publisher/subscriber pair with a hidden QoS
   mismatch, and diagnose it using only `ros2 topic info -v` — no
   looking at the code — within 2 minutes.

4. **Use the built-in sensor profile.** Rewrite Chapter 9's
   `sensor_subscriber.py` to use `rclpy.qos.qos_profile_sensor_data`
   explicitly instead of the default QoS, and confirm subscribing still
   works against Gazebo's bridged sensor topics — check what QoS the
   bridge itself is actually using with `ros2 topic info -v` first.

5. **Stretch:** write a node that logs a warning if messages on a topic
   stop arriving for more than 2 seconds (using a resettable timer that
   the subscription callback keeps pushing back) — a hand-rolled
   approximation of what the Deadline QoS policy is meant to formalize.
