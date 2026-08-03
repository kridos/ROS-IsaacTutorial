#!/usr/bin/env python3
"""Subscribes to /chatter and logs every message it receives. Identical
in substance to Chapter 2's listener.py — see talker.py's comment for
why it's copied here rather than referenced."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__("listener")
        self._subscription = self.create_subscription(
            String, "chatter", self._on_message, 10
        )

    def _on_message(self, msg: String):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main():
    rclpy.init()
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
