#!/usr/bin/env python3
"""Publishes a counting string message on /chatter once per second."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        # "talker" is this node's name — it's what shows up in
        # `ros2 node list` while this is running.
        super().__init__("talker")

        # create_publisher(msg_type, topic_name, queue_size).
        # queue_size (10 here) is how many outgoing messages ROS2 will
        # buffer if a subscriber can't keep up — irrelevant at 1 Hz, but
        # it's a required argument so we pick a small, conventional value.
        self._publisher = self.create_publisher(String, "chatter", 10)

        # A count we increment each publish, just so the message content
        # visibly changes each time — makes it obvious in the listener's
        # output that new messages are actually arriving, not the same
        # one being re-printed.
        self._count = 0

        # create_timer(period_seconds, callback) — the executor calls
        # self._publish() every 1.0 seconds once we start spinning below.
        # This is "push" style: the node acts on its own schedule, it
        # doesn't wait to be asked for data.
        self._timer = self.create_timer(1.0, self._publish)

    def _publish(self):
        msg = String()
        msg.data = f'Hello, ROS2! count={self._count}'
        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: '{msg.data}'")
        self._count += 1


def main():
    # rclpy.init() must run before any Node is constructed — it sets up
    # the underlying communication layer (DDS) this process will use to
    # talk to the rest of the ROS2 graph.
    rclpy.init()
    node = Talker()
    try:
        # spin() blocks here, handing control to the executor, which
        # invokes our timer callback repeatedly until Ctrl+C.
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Explicit cleanup: release the node's resources and shut down
        # the communication layer cleanly rather than relying on process
        # exit to do it implicitly.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
