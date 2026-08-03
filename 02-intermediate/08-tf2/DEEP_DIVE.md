# Chapter 8 Deep Dive: TF2

## The TF tree

Every frame in TF2 has exactly one parent (except the root frame, which
has none) — the whole set of frames forms a **tree**, never a graph with
cycles or a frame with two parents. This constraint is what makes "where
is A relative to B" always answerable and unambiguous: TF2 walks up from
A to the common ancestor of A and B, then back down to B, composing
transforms along the way. This chapter's demo relies on exactly this: the
listener asks for `sensor_mount -> moving_frame`, and TF2 walks
`sensor_mount -> base_link -> moving_frame` internally without the
listener needing to know that path exists.

## Static vs. dynamic transforms

- **Static**: a transform that never changes (e.g. a sensor rigidly
  bolted to a chassis — its offset from `base_link` is fixed for the
  robot's lifetime). Published once with `tf2_ros.StaticTransformBroadcaster`,
  which uses the `/tf_static` topic with a "latched"-like delivery
  (TRANSIENT_LOCAL durability QoS — forward reference to Chapter 10) so
  late-joining subscribers still get it without the publisher re-sending.
- **Dynamic**: a transform that changes over time (e.g. `odom ->
  base_link` as a robot drives, or a joint angle changing). Published
  repeatedly with `tf2_ros.TransformBroadcaster` on the plain `/tf`
  topic, each publish stamped with the time it's valid for.

Publishing a frequently-changing transform as static (or vice versa) is a
common beginner mix-up — a static transform published once will "freeze"
in RViz2/downstream code the instant the real relationship starts
changing, since nothing tells consumers to expect updates.

## Looking up a transform

```python
self._tf_buffer = tf2_ros.Buffer()
self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)
# ... later, inside a callback or timer:
transform = self._tf_buffer.lookup_transform(
    "sensor_mount", "moving_frame", rclpy.time.Time())
```

`TransformListener` subscribes to `/tf` and `/tf_static` in the
background and feeds everything into `Buffer`, which is what actually
does the tree-walking math when you call `lookup_transform`. Passing
`rclpy.time.Time()` (zero/default) means "give me the latest available
transform" — the most common choice; passing a specific timestamp asks
for the transform as it was (or will be) at that exact time, which can
raise an extrapolation exception if that time is too far in the past
(data aged out of the buffer) or the future (hasn't happened yet).

## Common exceptions

`tf2_ros.TransformException` (and its subclasses `LookupException`,
`ConnectivityException`, `ExtrapolationException`) covers the ways a
lookup can fail:
- **LookupException** — one of the frames doesn't exist yet (nobody has
  published it). Very common right after startup, before all broadcaster
  nodes have published their first message — code doing a lookup should
  expect this and retry, not treat it as fatal.
- **ConnectivityException** — the two frames exist but aren't connected
  (two separate trees, e.g. a second robot's TF tree with no link to the
  first).
- **ExtrapolationException** — asked for a time outside what's currently
  buffered (too old, or in the future).

## Debugging tools

- `ros2 run tf2_tools view_frames` — walks the whole current tree and
  generates a PDF diagram of every frame and its parent, with the
  publish rate of each — the fastest way to spot a frame that's missing,
  disconnected, or publishing far slower than expected.
- `ros2 run tf2_ros tf2_echo <frame1> <frame2>` — continuously prints the
  live transform between two frames to the terminal, exactly what this
  chapter's `frame_listener.py` does in code, useful for a quick manual
  check without writing a script.

## Common pitfall

Beyond the static/dynamic mix-up above: a `TransformListener` needs *some
time* to receive its first `/tf` and `/tf_static` messages after
construction before any lookup can succeed — calling `lookup_transform`
immediately in `__init__` (before spinning has had a chance to deliver
anything) will reliably raise `LookupException` even in a correctly-wired
system. This chapter's `frame_listener.py` sidesteps this by looking up
on a 1-second timer instead of at construction time, giving the listener
time to receive data first.
