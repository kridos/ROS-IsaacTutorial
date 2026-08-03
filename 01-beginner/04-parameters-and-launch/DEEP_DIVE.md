# Chapter 4 Deep Dive: Parameters & Launch Files

## Declaring and reading parameters

A node must **declare** a parameter (with a default value) before it can
read it — this is deliberate: it means `ros2 param list` can always show
every parameter a node supports, even ones the user never overrode, and
it lets ROS2 catch typos (setting an undeclared parameter is an error
rather than silently doing nothing).

```python
self.declare_parameter("publish_rate_hz", 1.0)
rate = self.get_parameter("publish_rate_hz").get_parameter_value().double_value
```

Reading it once at startup (as above) is the common case. If a node needs
to react live to a parameter changing while it's running (dynamic
reconfiguration), it registers a callback with
`add_on_set_parameters_callback` — out of scope for this chapter's demo,
but worth knowing exists for later chapters where, e.g., you might want
to tune a controller gain without restarting the node.

## YAML parameter files

Instead of setting each parameter individually on the command line, a
YAML file can set many at once, scoped to a node name:

```yaml
configurable_talker:
  ros__parameters:
    publish_rate_hz: 2.0
    message_text: "Configured from YAML"
```

The top-level key must match the node's name (or use a wildcard `/**` to
apply to any node), and everything lives under a `ros__parameters` key —
both are ROS2 conventions the loader expects exactly.

## Launch file structure (Python)

A launch file is itself a small Python program that returns a
`LaunchDescription` — a list of actions to perform (mostly: start this
node, with these arguments). The demo's `talker.launch.py` shows the
core pieces:

- `Node(package=..., executable=..., parameters=[...])` — describes one
  node to start, optionally pointing `parameters` at a YAML file path
  and/or a dict of individual overrides.
- `DeclareLaunchArgument("rate", default_value="1.0")` — declares a
  command-line argument the launch file itself accepts
  (`ros2 launch ... rate:=5.0`), independent of the node's own ROS2
  parameters, though the demo wires the two together by passing the
  launch argument's value into the node's parameter list.
- `LaunchConfiguration("rate")` — a placeholder that resolves to whatever
  value the `rate` launch argument ends up with, used when building the
  `Node(...)` action.

## Precedence: launch argument vs. YAML file

When both a YAML file and an explicit parameter override are passed to a
`Node(...)` action, later entries in the `parameters=[...]` list win over
earlier ones. The demo puts the YAML file first and the launch-argument
override second specifically so the command-line `rate:=` argument can
override what the YAML file says — worth confirming this ordering
whenever you combine the two, since it's easy to get backwards and be
confused about why an override "isn't working."

## CLI tools

- `ros2 param list` — every declared parameter on every running node.
- `ros2 param get /configurable_talker publish_rate_hz` — read a live
  value.
- `ros2 param set /configurable_talker publish_rate_hz 5.0` — set a live
  value (only takes effect if the node implemented a set-parameters
  callback to react to it; otherwise it updates the stored value but the
  node's already-running logic won't notice unless it re-reads).

## Common pitfall: type mismatches

`declare_parameter("publish_rate_hz", 1.0)` declares the parameter as a
**double**, inferred from the Python type of the default value. Setting
it later to an integer-looking YAML value like `publish_rate_hz: 2` (no
decimal point) can be parsed as an integer by the YAML loader, and ROS2
will raise a type error rather than silently coercing it — this is one
of the most common "why won't my launch file start" errors for
beginners. Always write float defaults with an explicit decimal point in
YAML (`2.0`, not `2`) to avoid it.
