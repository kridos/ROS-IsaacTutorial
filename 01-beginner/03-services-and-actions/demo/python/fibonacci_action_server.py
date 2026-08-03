#!/usr/bin/env python3
"""An action server that computes a Fibonacci sequence, reporting progress
and honoring cancel requests, using the built-in Fibonacci action type."""

import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__("fibonacci_action_server")

        # ActionServer wires up goal handling, cancel handling, and
        # execution all in one object — unlike a plain service, actions
        # need explicit callbacks for "should I accept this goal?" and
        # "should I accept this cancel request?" in addition to the work
        # itself, because a goal can be rejected or interrupted mid-run.
        self._action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",
            execute_callback=self._execute,
            goal_callback=self._handle_goal,
            cancel_callback=self._handle_cancel,
        )
        self.get_logger().info("fibonacci action server ready")

    def _handle_goal(self, goal_request: Fibonacci.Goal) -> GoalResponse:
        # Reject nonsensical goals up front rather than accepting them and
        # failing later — order must be at least 2 for a Fibonacci
        # sequence to mean anything.
        if goal_request.order < 2:
            self.get_logger().warn(f"Rejecting goal with order={goal_request.order}")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _handle_cancel(self, goal_handle) -> CancelResponse:
        self.get_logger().info("Received cancel request")
        return CancelResponse.ACCEPT

    def _execute(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(f"Executing goal: computing {order} Fibonacci numbers")

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, order - 1):
            # Check for a pending cancel request on every iteration — this
            # is what makes the action actually cancellable instead of
            # just accepting cancel requests without honoring them.
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info("Goal canceled")
                result = Fibonacci.Result()
                result.sequence = feedback_msg.partial_sequence
                return result

            next_value = feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1]
            feedback_msg.partial_sequence.append(next_value)

            # Publish feedback so the client can observe progress without
            # waiting for the final result — this is the capability a
            # plain service doesn't have.
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f"Feedback: {feedback_msg.partial_sequence}")

            # Simulated work — a real action would be doing something
            # that actually takes time (moving a robot, planning a path);
            # the sleep here just makes progress visible over multiple
            # feedback messages instead of finishing instantly.
            time.sleep(0.5)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main():
    rclpy.init()
    node = FibonacciActionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
