#!/usr/bin/env python3
"""Subscribes to /chatter and logs every message it receives."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__("listener")

        # create_subscription(msg_type, topic_name, callback, queue_size).
        # The callback (_on_message) is invoked by the executor whenever
        # a message arrives — we never call it ourselves, and we never
        # poll for new data; ROS2's spin() loop delivers it to us.
        #
        # Note there's no code here that knows a "talker" node exists.
        # This subscriber would work identically if a completely
        # different program published on /chatter with the right message
        # type — that decoupling is the whole point of pub/sub.
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
