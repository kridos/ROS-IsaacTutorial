#!/usr/bin/env python3
"""Sends a NavigateToPose action goal to Nav2 and logs feedback
(distance remaining) as the robot drives there — the same
goal/feedback/result action-client pattern from Chapter 3's
fibonacci_action_client.py, now driving a real navigation task.

Usage: python3 send_goal.py [x] [y]  (default: 1.5 1.5)

Note: AMCL needs an initial pose before this will work meaningfully —
publish one via RViz2's "2D Pose Estimate" tool first (see demo/README.md).
"""

import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class NavigateToPoseClient(Node):
    def __init__(self):
        super().__init__("send_goal_client")
        self._client = ActionClient(self, NavigateToPose, "navigate_to_pose")

    def send_goal(self, x: float, y: float):
        self._client.wait_for_server()

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0  # facing along +X, no rotation

        self.get_logger().info(f"Sending navigation goal: x={x}, y={y}")
        send_goal_future = self._client.send_goal_async(
            goal_msg, feedback_callback=self._on_feedback
        )
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Goal was rejected by Nav2")
            return

        self.get_logger().info("Goal accepted, navigating...")
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        self.get_logger().info(f"Navigation finished with status: {result_future.result().status}")

    def _on_feedback(self, feedback_msg):
        remaining = feedback_msg.feedback.distance_remaining
        self.get_logger().info(f"Distance remaining: {remaining:.2f}m")


def main():
    x = float(sys.argv[1]) if len(sys.argv) > 1 else 1.5
    y = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5

    rclpy.init()
    node = NavigateToPoseClient()
    node.send_goal(x, y)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
