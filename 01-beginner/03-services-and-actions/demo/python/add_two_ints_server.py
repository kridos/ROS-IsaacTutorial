#!/usr/bin/env python3
"""A service server that adds two integers on request."""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__("add_two_ints_server")

        # create_service(srv_type, service_name, callback). Unlike a
        # subscription callback, this callback both receives an argument
        # (the request) AND must return a value (the response) — the
        # client is waiting on that return value.
        self._service = self.create_service(
            AddTwoInts, "add_two_ints", self._handle_request
        )
        self.get_logger().info("add_two_ints service ready")

    def _handle_request(
        self, request: AddTwoInts.Request, response: AddTwoInts.Response
    ) -> AddTwoInts.Response:
        # ROS2 service callbacks are handed an already-constructed
        # response object to fill in and return, rather than constructing
        # a new one — this is the rclpy convention for service callbacks.
        response.sum = request.a + request.b
        self.get_logger().info(
            f"Incoming request: {request.a} + {request.b} = {response.sum}"
        )
        return response


def main():
    rclpy.init()
    node = AddTwoIntsServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
