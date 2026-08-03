# Practice: Debugging & Visualization Tools

1. **Multi-topic plot.** Modify `noisy_sensor_publisher.py` to also
   publish a second, differently-shaped signal (e.g. a slow ramp instead
   of a sine wave) on `/sensor/reading2`, then plot both at once in a
   single `rqt_plot` window.

2. **Filter the noise.** Write a small node that subscribes to
   `/sensor/reading`, applies a simple moving average (e.g. average of
   the last 5 readings), and republishes on `/sensor/reading_filtered`.
   Plot raw vs. filtered in `rqt_plot` side by side.

3. **Record a "bug."** Modify `noisy_sensor_publisher.py` to occasionally
   (say, 1 in 50 messages) publish a wildly out-of-range value, simulating
   a sensor glitch. Record 30 seconds with `ros2 bag record`, then use
   `ros2 bag play` plus `ros2 topic echo` to find the glitch in the
   recording — practice using a bag for after-the-fact debugging.

4. **rqt_console in a busy system.** Run Chapter 2's talker AND this
   chapter's noisy publisher at once, open `rqt_console`, and filter to
   show only one node's messages — get comfortable with the filter UI
   before you actually need it on a bigger system.

5. **Stretch:** write a script using `ros2 bag`'s Python API (not just
   the CLI) to read back a recorded bag file and print summary statistics
   (min/max/mean) of the recorded sensor values — a first step toward
   programmatic log analysis.
