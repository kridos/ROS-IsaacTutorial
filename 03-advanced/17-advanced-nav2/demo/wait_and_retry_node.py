#!/usr/bin/env python3
"""Sends a NavigateToPose goal to a Nav2 instance running with
custom_bt.xml loaded (same action-client pattern as Chapter 11's
send_goal.py) and logs feedback with timestamps, so you can observe the
custom tree's more patient recovery timing (a 5s wait + 0.3m backup, per
custom_bt.xml) if the robot's path is blocked, rather than the stock
tree's faster-cycling recovery.

Usage: python3 wait_and_retry_node.py [x] [y]  (default: 1.5 1.5)
"""

import sys
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class NavigateWithTimingClient(Node):
    def __init__(self):
        super().__init__("wait_and_retry_client")
        self._client = ActionClient(self, NavigateToPose, "navigate_to_pose")
        self._start_time = None

    def send_goal(self, x: float, y: float):
        self._client.wait_for_server()

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0

        self._start_time = time.monotonic()
        self.get_logger().info(f"Sending navigation goal: x={x}, y={y}")
        send_goal_future = self._client.send_goal_async(
            goal_msg, feedback_callback=self._on_feedback
        )
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Goal was rejected by Nav2")
            return

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        elapsed = time.monotonic() - self._start_time
        self.get_logger().info(
            f"Navigation finished after {elapsed:.1f}s with status: "
            f"{result_future.result().status}"
        )

    def _on_feedback(self, feedback_msg):
        elapsed = time.monotonic() - self._start_time
        remaining = feedback_msg.feedback.distance_remaining
        # Logging elapsed time alongside distance remaining is what lets
        # you spot the custom tree's recovery timing in the log: a long
        # gap between feedback updates with distance_remaining unchanged
        # suggests the recovery branch (5s wait + backup) is running,
        # per custom_bt.xml.
        self.get_logger().info(f"[t={elapsed:.1f}s] Distance remaining: {remaining:.2f}m")


def main():
    x = float(sys.argv[1]) if len(sys.argv) > 1 else 1.5
    y = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5

    rclpy.init()
    node = NavigateWithTimingClient()
    node.send_goal(x, y)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
