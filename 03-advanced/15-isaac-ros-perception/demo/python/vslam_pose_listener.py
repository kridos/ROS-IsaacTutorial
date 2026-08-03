#!/usr/bin/env python3
"""Subscribes to Isaac ROS Visual SLAM's output pose topic and logs it,
alongside a TF lookup (same Chapter 8 Buffer/TransformListener pattern)
confirming the odom -> base_link transform VSLAM publishes actually
exists — connecting Isaac ROS's output back to the TF machinery from
Chapter 8 rather than treating it as something new and unrelated."""

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener, TransformException
from isaac_ros_visual_slam_interfaces.msg import VisualSlamStatus
from nav_msgs.msg import Odometry


class VslamPoseListener(Node):
    def __init__(self):
        super().__init__("vslam_pose_listener")

        # Isaac ROS Visual SLAM publishes odometry on visual_slam/tracking/odometry
        # in the same nav_msgs/msg/Odometry shape Chapter 7/9's Gazebo demos
        # used — deliberately the same message type as wheel-odometry-based
        # sources, so downstream code (Nav2, etc.) doesn't need to care
        # which sensor produced the pose estimate.
        self.create_subscription(
            Odometry, "visual_slam/tracking/odometry", self._on_odometry, 10
        )
        # VisualSlamStatus reports tracking health (e.g. whether VSLAM
        # currently has a good lock on the scene or has lost tracking) —
        # worth watching alongside the pose itself, since a "confident"
        # pose from a lost-tracking state is misleading.
        self.create_subscription(
            VisualSlamStatus, "visual_slam/status", self._on_status, 10
        )

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)
        self._timer = self.create_timer(1.0, self._check_tf)

    def _on_odometry(self, msg: Odometry):
        pos = msg.pose.pose.position
        self.get_logger().info(f"VSLAM odometry: x={pos.x:.3f}, y={pos.y:.3f}, z={pos.z:.3f}")

    def _on_status(self, msg: VisualSlamStatus):
        self.get_logger().info(f"VSLAM tracking status: {msg.vo_state}")

    def _check_tf(self):
        # Confirms VSLAM is actually publishing the odom -> base_link
        # transform, not just the /visual_slam/tracking/odometry topic —
        # the same Buffer/TransformListener/lookup_transform pattern from
        # Chapter 8's frame_listener.py, applied to a real perception
        # pipeline's output instead of a toy orbiting frame.
        try:
            self._tf_buffer.lookup_transform("odom", "base_link", rclpy.time.Time())
            self.get_logger().info("TF check: odom -> base_link transform is present")
        except TransformException as ex:
            self.get_logger().warn(f"TF check failed: {ex}")


def main():
    rclpy.init()
    node = VslamPoseListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
