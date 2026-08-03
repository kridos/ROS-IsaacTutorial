# Practice: Parameters & Launch Files

1. **New parameter.** Add a `use_uppercase` boolean parameter to
   `configurable_talker.py` that, when true, publishes the message text
   in all caps. Set it via a launch argument, not just the YAML file.

2. **Two nodes, one launch file.** Extend `talker.launch.py` to also
   launch a `listener.py` (from Chapter 2) alongside the configurable
   talker, so one `ros2 launch` command starts both.

3. **Dynamic reconfiguration.** DEEP_DIVE.md mentions
   `add_on_set_parameters_callback` for reacting to live parameter
   changes without a restart, but doesn't implement it. Add one to
   `configurable_talker.py` so `ros2 param set
   /configurable_talker publish_rate_hz 5.0` actually changes the
   running publish rate immediately, not just the stored value.

4. **Break the type-mismatch pitfall on purpose.** Edit
   `talker_config.yaml` to set `publish_rate_hz: 2` (no decimal point)
   and confirm you get the type error DEEP_DIVE.md warns about — then
   fix it and explain in one sentence why `2.0` and `2` differ here.

5. **Stretch:** write a launch file that starts three copies of
   `configurable_talker.py`, each with a different `message_text` value
   passed via three separate YAML files — a preview of Chapter 19's
   multi-robot namespacing problem, one launch file at a time.
