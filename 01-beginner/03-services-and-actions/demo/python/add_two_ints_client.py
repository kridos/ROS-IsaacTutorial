#!/usr/bin/env python3
"""Calls the add_two_ints service once, asynchronously, and prints the result."""

import sys

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")
        self._client = self.create_client(AddTwoInts, "add_two_ints")

        # wait_for_service blocks (with a timeout, polled in a loop here)
        # until a server is actually advertising this service name. Without
        # this, calling the service before a server exists would just fail
        # — better to wait and tell the user what's happening.
        while not self._client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for add_two_ints service...")

    def add(self, a: int, b: int) -> int:
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        # call_async returns a Future immediately instead of blocking this
        # function — we then hand control back to spin (via
        # spin_until_future_complete) so the executor can process the
        # response when it arrives. This is the pattern DEEP_DIVE.md
        # recommends over a blocking synchronous call, even in a simple
        # script like this one, so the habit carries over to contexts
        # where a synchronous call would deadlock.
        future = self._client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result().sum


def main():
    # Accept two integers from the command line, defaulting to 2 and 3 so
    # the demo works with no arguments too.
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    rclpy.init()
    node = AddTwoIntsClient()
    result = node.add(a, b)
    node.get_logger().info(f"Result: {a} + {b} = {result}")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
