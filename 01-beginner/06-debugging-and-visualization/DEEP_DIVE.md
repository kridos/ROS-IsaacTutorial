# Chapter 6 Deep Dive: RViz2, rqt, ros2 bag

## rqt_graph — see the node/topic graph

`ros2 run rqt_graph rqt_graph` draws the live ROS2 graph from Chapter 2's
mental model as an actual diagram: boxes for nodes, arrows for topics,
direction showing publisher-to-subscriber. This is the fastest way to
answer "is anything actually connected to anything" when a system isn't
behaving — if an arrow you expect isn't there, that's your bug, before
you've read a single line of code.

## rqt_console — filtered log viewing

Every `self.get_logger().info(...)` / `.warn(...)` / `.error(...)` call
goes to your terminal, but with many nodes running, terminal logs
interleave into an unreadable mess. `ros2 run rqt_console rqt_console`
aggregates log messages from every running node into one filterable
table — filter by node name, by severity (only show warnings and above),
or search message text. This is usually faster than `grep`-ing terminal
scrollback once more than 2-3 nodes are running at once.

## rqt_plot — live numeric plotting

`ros2 run rqt_plot rqt_plot /sensor/reading/data` opens a live scrolling
plot of a numeric topic field. You give it a topic *and field path*
(`/sensor/reading/data` for a `Float64` message's `data` field) — useful
for eyeballing whether a sensor value is noisy, drifting, or has a step
change you didn't expect, without writing any code to visualize it.

## ros2 bag — record and replay

```bash
ros2 bag record /sensor/reading -o my_recording
```

records every message on `/sensor/reading` (with real timestamps) into
a directory (`my_recording/`) containing a SQLite database and metadata.
Stop with Ctrl+C.

```bash
ros2 bag info my_recording
```

shows what's in it: topics, message counts, duration, message types —
useful to sanity-check a recording actually captured what you expected
before you rely on it.

```bash
ros2 bag play my_recording
```

republishes every recorded message on the same topics, at the same
relative timing it was recorded at (by default) — any node subscribed to
`/sensor/reading` can't tell the difference between the live sensor and
a bag replaying old data, which is exactly the point: you can debug
against a captured problematic run as many times as you need.

## Bag replay and simulated time

By default, `ros2 bag play` uses wall-clock time to pace replay. If the
nodes consuming the data expect **simulated time** instead (common once
you're working with Gazebo — Chapter 7 — where a simulator can run
faster or slower than real time), both the bag player and the consuming
nodes need `use_sim_time` set consistently:

```bash
ros2 bag play my_recording --clock
```

`--clock` makes the bag player publish `/clock`, and any node with its
`use_sim_time` parameter set to `true` will read simulated time from
there instead of the wall clock. Mismatched `use_sim_time` between a bag
player and its consumers is a common, confusing bug: timestamps in
messages look fine, but time-dependent logic (timeouts, TF lookups)
behaves as if no time is passing, or passes at the wrong rate.

## Common pitfall

Forgetting `--clock` / mismatched `use_sim_time` (above) is the single
most common `ros2 bag` gotcha. A close second: recording *every* topic
with `ros2 bag record -a` on a system with high-rate sensors (cameras,
lidar) produces enormous files very fast — prefer recording only the
specific topics you need (as this chapter's demo does) unless you
specifically need a full-system capture.
