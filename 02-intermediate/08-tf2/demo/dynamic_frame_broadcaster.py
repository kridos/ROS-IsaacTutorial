#!/usr/bin/env python3
"""Publishes a base_link -> moving_frame transform that rotates over
time, simulating something like an orbiting sensor or a spinning
turret — a stand-in for any transform that actually changes, unlike
static_frame_broadcaster.py's fixed offset."""

import math

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class DynamicFrameBroadcaster(Node):
    def __init__(self):
        super().__init__("dynamic_frame_broadcaster")

        # TransformBroadcaster (not the Static variant) publishes on the
        # plain /tf topic — appropriate here since this transform changes
        # every publish and downstream consumers need each new value, not
        # just the latest one delivered once to late joiners.
        self._broadcaster = TransformBroadcaster(self)
        self._angle = 0.0
        self._timer = self.create_timer(0.1, self._publish_transform)  # 10 Hz

    def _publish_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "base_link"     # parent
        t.child_frame_id = "moving_frame"   # child

        # Orbit moving_frame around base_link at radius 0.3m in the XY
        # plane — translation traces a circle as _angle advances.
        radius = 0.3
        t.transform.translation.x = radius * math.cos(self._angle)
        t.transform.translation.y = radius * math.sin(self._angle)
        t.transform.translation.z = 0.0

        # Rotate moving_frame to face outward along its orbit (yaw =
        # _angle), expressed as a quaternion since TF2 transforms always
        # use quaternions, never raw Euler angles.
        half_angle = self._angle / 2.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(half_angle)
        t.transform.rotation.w = math.cos(half_angle)

        self._broadcaster.sendTransform(t)
        self._angle += 0.05  # advance the orbit a little each publish


def main():
    rclpy.init()
    node = DynamicFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
