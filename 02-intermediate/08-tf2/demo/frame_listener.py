#!/usr/bin/env python3
"""Looks up the sensor_mount -> moving_frame transform once a second and
logs it. Neither frame is the other's direct parent — TF2 composes the
path sensor_mount -> base_link -> moving_frame internally to answer this,
which is the whole point of this demo (see DEEP_DIVE.md)."""

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener, TransformException


class FrameListener(Node):
    def __init__(self):
        super().__init__("frame_listener")

        # Buffer stores recently-received transforms; TransformListener
        # subscribes to /tf and /tf_static in the background and feeds
        # them into the buffer. Neither does anything visible on its own
        # — lookup_transform() below is what actually queries them.
        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        # Deliberately NOT looking up a transform here in __init__ — the
        # listener hasn't had a chance to receive any /tf messages yet
        # (see DEEP_DIVE.md's common pitfall). A timer gives spin() time
        # to deliver data first.
        self._timer = self.create_timer(1.0, self._lookup_and_log)

    def _lookup_and_log(self):
        try:
            # rclpy.time.Time() (the default, unspecified time) means
            # "give me the latest transform you have" rather than asking
            # for a specific historical/future timestamp.
            t = self._tf_buffer.lookup_transform(
                "sensor_mount", "moving_frame", rclpy.time.Time()
            )
            translation = t.transform.translation
            self.get_logger().info(
                f"sensor_mount -> moving_frame: "
                f"x={translation.x:.3f}, y={translation.y:.3f}, z={translation.z:.3f}"
            )
        except TransformException as ex:
            # Expected transiently at startup, before both broadcaster
            # nodes have published their first message — log and retry
            # on the next timer tick rather than crashing.
            self.get_logger().warn(f"Could not look up transform: {ex}")


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
