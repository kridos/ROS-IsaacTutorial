# Chapter 10 Deep Dive: DDS & QoS

## Why DDS, and decentralized discovery

ROS1 had a single central process, `roscore`, that every node had to
register with — if it died, the whole system's ability to discover new
connections died with it (though already-connected nodes kept talking).
ROS2 was rebuilt on DDS specifically to remove this single point of
failure: DDS implementations do **decentralized discovery** — each DDS
participant (each ROS2 node) broadcasts its own presence and listens for
others directly, with no central registry process at all. This is why
there's no ROS2 equivalent of starting `roscore` first; any node can
start in any order and they'll find each other.

`ROS_DOMAIN_ID` (from Chapter 1) is literally a DDS concept: it
partitions discovery so that nodes with different domain IDs never see
each other, even on the same network — DDS's mechanism for letting
multiple independent ROS2 systems coexist without interfering.

## The QoS policies that matter most

Every publisher and subscriber has a QoS **profile** — a bundle of
policies. The ones you'll actually touch in practice:

- **Reliability**: `RELIABLE` (guaranteed delivery, with retransmission
  — used for anything you can't afford to lose, like a one-off command)
  vs. `BEST_EFFORT` (send it once, don't retransmit if lost — used for
  high-rate data like camera frames, where a lost frame is fine but
  retransmitting stale ones is worse than useless).
- **Durability**: `VOLATILE` (subscribers only get messages published
  *after* they subscribed — the default) vs. `TRANSIENT_LOCAL` (the
  publisher keeps recent messages around and delivers them to
  late-joining subscribers too — this is what Chapter 8's
  `StaticTransformBroadcaster` uses on `/tf_static`, and what a map
  server typically uses so a late-starting Nav2 node still gets the map
  without the map server re-publishing it).
- **History**: `KEEP_LAST` with a `depth` (buffer only the N most recent
  messages — the common case) vs. `KEEP_ALL` (buffer everything, bounded
  only by resource limits — rare, mostly for cases where losing any
  message is unacceptable and you have the memory to spare).
- **Deadline**: an expected maximum period between messages — lets a
  subscriber be notified if a publisher stops publishing as often as
  promised, useful for detecting a stalled sensor rather than just
  silently receiving stale data forever.

## Compatibility and the silent-failure trap

A publisher and subscriber only connect if their QoS policies are
**compatible** — critically, this is not always symmetric or intuitive.
A `RELIABLE` publisher can talk to a `BEST_EFFORT` subscriber, but a
`BEST_EFFORT` publisher **cannot** connect to a `RELIABLE` subscriber
(the subscriber is asking for a guarantee the publisher never promised).
When this happens, there's no error, no exception, no log message by
default — `ros2 node list` and `ros2 topic list` both look completely
normal, the topic exists, but no messages ever arrive. This is a strictly
harder version of Chapter 2's topic-name-typo pitfall, because everything
that usually catches a typo (exact name match, exact type match) passes.

**Diagnosis**: `ros2 topic info /your_topic -v` (`-v` is the key flag —
without it you don't see QoS) shows the QoS profile of every connected
publisher and subscriber. A `Reliability: BEST_EFFORT` publisher next to
a `Reliability: RELIABLE` subscriber on the same topic is your answer.

## Practical conventions

- **Sensor data** (camera, lidar, IMU — everything from Chapter 9):
  `BEST_EFFORT`, `KEEP_LAST` with a small depth (e.g. 5). High rate,
  losing an old frame in favor of a newer one is the right trade-off,
  and this is in fact ROS2's predefined `sensor_data` QoS profile
  (`rclpy.qos.qos_profile_sensor_data`) — use it directly rather than
  hand-assembling the same three settings.
- **Commands and critical state** (Chapter 2's `/chatter`, action goals,
  `/cmd_vel`): `RELIABLE`, `KEEP_LAST` with a modest depth. You want
  every command delivered, and losing an old one in favor of a newer
  command is usually fine (though for some commands you'd want
  `KEEP_ALL` — depends on the specific use).
- **Static reference data** (a map, Chapter 8's static transforms):
  `RELIABLE` + `TRANSIENT_LOCAL`, so any node that starts later still
  gets it without the publisher needing to re-send anything.

## Common pitfall

Beyond the compatibility trap above: assuming a QoS mismatch will at
least log a warning somewhere. Depending on RMW implementation (the DDS
vendor ROS2 is configured to use) and log verbosity settings, an
incompatible match can be genuinely silent at default log levels — `ros2
topic info -v` is not just convenient, it's often the *only* way to see
what's actually happening, which is why it's worth reaching for early
whenever a topic that should be delivering messages isn't.
