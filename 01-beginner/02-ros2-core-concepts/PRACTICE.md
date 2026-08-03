# Practice: ROS2 Core Concepts

1. **Change the message type.** Modify `talker.py`/`listener.py` to
   publish a `std_msgs/msg/Int32` counter instead of a `String`. Update
   both ends and confirm `ros2 topic echo` shows the new type.

2. **Three-way chat.** Write a third node that both subscribes to
   `/chatter` (like `listener.py`) and publishes its own counting
   message on a *new* topic, `/chatter2`, at a different rate. Run all
   three and use `rqt_graph` (you'll formally meet it in Chapter 6, but
   `ros2 run rqt_graph rqt_graph` works now) to see the resulting graph.

3. **Break it on purpose.** Rename the listener's subscribed topic to
   `/chater` (typo) and confirm nothing crashes but nothing arrives
   either — use `ros2 topic list` and `ros2 topic info` to diagnose it
   the way DEEP_DIVE.md describes, without looking at the code first.

4. **C++ version.** Modify the C++ talker to publish at 5 Hz instead of
   1 Hz by changing the timer period, rebuild with `colcon build`, and
   confirm the listener (Python or C++) sees the new rate with `ros2
   topic hz`.

5. **Stretch:** write a node that subscribes to `/chatter` and
   republishes every *other* message (skip every second one) on
   `/chatter_filtered` — your first "processing" node instead of a pure
   pass-through.
