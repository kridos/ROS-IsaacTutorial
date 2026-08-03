# Demo: TF2 — static, dynamic, and composed lookups

## How to run

Three terminals:

```bash
python3 static_frame_broadcaster.py
```

```bash
python3 dynamic_frame_broadcaster.py
```

```bash
python3 frame_listener.py
```

## Expected output

`static_frame_broadcaster.py` logs once:

```
[INFO] [static_frame_broadcaster]: Published static transform: sensor_mount -> base_link
```

`dynamic_frame_broadcaster.py` publishes silently at 10 Hz (no per-publish
log — check it's working with `ros2 topic echo /tf` in another terminal).

`frame_listener.py` logs once a second:

```
[INFO] [frame_listener]: sensor_mount -> moving_frame: x=0.196, y=0.171, z=-0.100
```

The x/y values should trace a circle over time (matching `moving_frame`'s
orbit around `base_link`), offset by the fixed `sensor_mount -> base_link`
translation — confirming TF2 composed both transforms across the
`sensor_mount -> base_link -> moving_frame` path, even though
`frame_listener.py` never mentions `base_link` directly.

## Explore the tree

While all three are running:

```bash
ros2 run tf2_tools view_frames
```

Expected: `frames.pdf` (or `frames_<timestamp>.pdf`, depending on ROS2
version) showing `sensor_mount -> base_link -> moving_frame`, with
`base_link -> moving_frame` reporting a ~10 Hz publish rate and
`sensor_mount -> base_link` reporting as a static/latched transform.

```bash
ros2 run tf2_ros tf2_echo sensor_mount moving_frame
```

Expected: continuously prints the same transform `frame_listener.py` is
computing, confirming the CLI tool and the script agree.

## Try it: break it on purpose

Stop `static_frame_broadcaster.py` (Ctrl+C) before starting
`frame_listener.py`. Expected: `frame_listener.py` logs
`LookupException`-style warnings every second (`sensor_mount` frame never
existed) until you start the static broadcaster — a hands-on look at the
`LookupException` case from DEEP_DIVE.md.
