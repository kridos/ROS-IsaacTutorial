#!/usr/bin/env python3
"""Publishes a counting string message on /chatter once per second.
Identical in substance to Chapter 2's talker.py — copied here (not
imported/referenced across chapters) because this chapter's Dockerfile
needs its own local copy inside its build context; a Docker build can't
reach outside its context directory to pull in another chapter's file."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__("talker")
        self._publisher = self.create_publisher(String, "chatter", 10)
        self._count = 0
        self._timer = self.create_timer(1.0, self._publish)

    def _publish(self):
        msg = String()
        msg.data = f'Hello from container! count={self._count}'
        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: '{msg.data}'")
        self._count += 1


def main():
    rclpy.init()
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
