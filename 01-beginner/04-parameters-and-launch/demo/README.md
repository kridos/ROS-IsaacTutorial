# Demo: Parameters & Launch Files

## Run the node directly with default parameters

```bash
python3 configurable_talker.py
```

Expected: publishes once a second with the default message text
`"Hello, ROS2!"`.

## Override parameters from the command line (no launch file)

```bash
python3 configurable_talker.py --ros-args -p publish_rate_hz:=5.0 -p message_text:="Fast talker"
```

Expected: publishes 5 times a second with the overridden text.

## Run via the launch file (loads talker_config.yaml)

```bash
ros2 launch talker.launch.py
```

Expected: publishes twice a second (`publish_rate_hz: 2.0` from
`talker_config.yaml`) with text `"Configured from YAML"`.

## Override the launch file's rate argument

```bash
ros2 launch talker.launch.py rate:=5.0
```

Expected: publishes 5 times a second — the `rate:=5.0` launch argument
overrides the YAML file's `publish_rate_hz: 2.0`, while `message_text`
still comes from the YAML file (only `rate` is wired to a launch
argument in this demo).

## Inspect parameters while it's running

In another terminal, while any of the above is running:

```bash
ros2 param list
ros2 param get /configurable_talker publish_rate_hz
```
