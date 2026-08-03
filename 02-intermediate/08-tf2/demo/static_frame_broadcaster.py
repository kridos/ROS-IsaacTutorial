#!/usr/bin/env python3
"""Publishes a fixed sensor_mount -> base_link transform once, using a
StaticTransformBroadcaster — see DEEP_DIVE.md for why this uses /tf_static
instead of the repeatedly-published /tf that dynamic_frame_broadcaster.py
uses."""

import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class StaticFrameBroadcaster(Node):
    def __init__(self):
        super().__init__("static_frame_broadcaster")

        # StaticTransformBroadcaster publishes on /tf_static with
        # TRANSIENT_LOCAL durability under the hood — a listener that
        # starts up AFTER this publish still receives it, unlike a
        # normal topic where late subscribers miss earlier messages.
        self._broadcaster = StaticTransformBroadcaster(self)
        self._publish_static_transform()

    def _publish_static_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "sensor_mount"  # parent
        t.child_frame_id = "base_link"      # child

        # A fixed offset: base_link sits 0.1m below and behind
        # sensor_mount, with no rotation. Values are arbitrary for this
        # demo — the point is that they never change once published.
        t.transform.translation.x = -0.05
        t.transform.translation.y = 0.0
        t.transform.translation.z = -0.10
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0  # identity rotation (no rotation)

        # Published exactly once — a static transform broadcaster is
        # meant to "set and forget," relying on TRANSIENT_LOCAL delivery
        # rather than repeated publishing to reach late subscribers.
        self._broadcaster.sendTransform(t)
        self.get_logger().info("Published static transform: sensor_mount -> base_link")


def main():
    rclpy.init()
    node = StaticFrameBroadcaster()
    try:
        # Still need to spin (even though nothing repeats) so the node
        # stays alive and its publisher's message remains available to
        # late-joining subscribers for as long as this process runs.
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
