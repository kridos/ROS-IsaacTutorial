# Practice: TF2

1. **A third dynamic frame.** Add a `dynamic_frame_broadcaster2.py`
   publishing a `moving_frame -> moving_frame2` transform (another
   orbit, different radius/speed), and modify `frame_listener.py` to
   look up `sensor_mount -> moving_frame2` — a three-hop chain instead
   of two, confirming TF2 composes across an arbitrary number of frames.

2. **Static vs. dynamic, swapped.** Change `dynamic_frame_broadcaster.py`
   to publish via `StaticTransformBroadcaster` instead (publish once,
   don't update). Run `frame_listener.py` and watch the looked-up
   position freeze instead of orbiting — a hands-on look at
   DEEP_DIVE.md's static/dynamic mix-up pitfall.

3. **Extrapolation exception, on purpose.** Modify `frame_listener.py`
   to request a transform at a specific timestamp 5 seconds in the
   future (`self.get_clock().now() + Duration(seconds=5)`) instead of
   `rclpy.time.Time()`. Confirm you get an `ExtrapolationException` and
   explain in one sentence why.

4. **view_frames on a bigger tree.** Run this chapter's three nodes
   alongside Chapter 5's `display.launch.py` (different terminal) and
   run `ros2 run tf2_tools view_frames` — confirm the PDF shows two
   separate, unconnected trees (this chapter's toy frames, and Chapter
   5's arm), since nothing links them.

5. **Stretch:** write a node that looks up `sensor_mount -> moving_frame`
   every step and publishes the *distance* between them (a `Float64`) —
   your first node that derives a new value from a TF lookup rather than
   just logging the transform.
