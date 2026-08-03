#!/usr/bin/env python3
"""Publishes a forward-drive Twist on /cmd_vel and logs incoming
Odometry on /odom — a plain ROS2 node with no Isaac Sim imports at all,
run in a normal terminal exactly like Chapter 7's `ros2 topic pub` /
`ros2 topic echo` pattern against Gazebo. This is the point of this
chapter's demo (see OVERVIEW.md): from ROS2's side, driving the Isaac
Sim robot looks identical to driving the Chapter 7 Gazebo robot."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class DriveAndLogOdom(Node):
    def __init__(self):
        super().__init__("drive_and_log_odom")
        self._cmd_vel_publisher = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_subscription(Odometry, "odom", self._on_odom, 10)

        # Drive forward at a constant speed for as long as this node runs
        # — same idea as Chapter 7's `ros2 topic pub --rate 10`, just as
        # a script instead of a one-line CLI command.
        self._timer = self.create_timer(0.1, self._publish_cmd_vel)

    def _publish_cmd_vel(self):
        twist = Twist()
        twist.linear.x = 0.3
        twist.angular.z = 0.0
        self._cmd_vel_publisher.publish(twist)

    def _on_odom(self, msg: Odometry):
        pos = msg.pose.pose.position
        self.get_logger().info(f"odom: x={pos.x:.3f}, y={pos.y:.3f}")


def main():
    rclpy.init()
    node = DriveAndLogOdom()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
