#!/usr/bin/env python3
"""Sends a Fibonacci action goal, prints feedback as it streams in, and
prints the final result."""

import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__("fibonacci_action_client")
        self._client = ActionClient(self, Fibonacci, "fibonacci")

    def send_goal(self, order: int):
        self._client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # send_goal_async with a feedback_callback is how you subscribe to
        # feedback for this specific goal — feedback is delivered as this
        # goal executes, before the final result is ready.
        send_goal_future = self._client.send_goal_async(
            goal_msg, feedback_callback=self._on_feedback
        )
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal was rejected")
            return

        self.get_logger().info("Goal accepted, waiting for result...")
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result
        self.get_logger().info(f"Final result: {result.sequence}")

    def _on_feedback(self, feedback_msg):
        self.get_logger().info(
            f"Feedback received: {feedback_msg.feedback.partial_sequence}"
        )


def main():
    order = int(sys.argv[1]) if len(sys.argv) > 1 else 6

    rclpy.init()
    node = FibonacciActionClient()
    node.send_goal(order)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
