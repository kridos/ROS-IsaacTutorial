#!/usr/bin/env python3
"""Subscribes to /qos_demo, with a QoS reliability policy chosen from the
command line — pair with qos_publisher.py. Try matched profiles (both
"reliable" or both "best_effort") vs. mismatched (publisher
"best_effort", subscriber "reliable") to see DEEP_DIVE.md's silent
non-connection case firsthand.

Usage: python3 qos_subscriber.py [reliable|best_effort]  (default: reliable)
"""

import sys

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String


def build_qos(profile_name: str) -> QoSProfile:
    reliability = (
        ReliabilityPolicy.RELIABLE
        if profile_name == "reliable"
        else ReliabilityPolicy.BEST_EFFORT
    )
    return QoSProfile(
        reliability=reliability,
        history=HistoryPolicy.KEEP_LAST,
        depth=10,
    )


class QosSubscriber(Node):
    def __init__(self, profile_name: str):
        super().__init__("qos_subscriber")
        qos = build_qos(profile_name)
        self.create_subscription(String, "qos_demo", self._on_message, qos)
        self.get_logger().info(
            f"Subscribing with reliability={profile_name} — "
            "if you don't see any 'I heard' messages below within a few "
            "seconds, check `ros2 topic info /qos_demo -v` for a QoS "
            "mismatch (see DEEP_DIVE.md)."
        )

    def _on_message(self, msg: String):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main():
    profile_name = sys.argv[1] if len(sys.argv) > 1 else "reliable"
    if profile_name not in ("reliable", "best_effort"):
        print("Usage: qos_subscriber.py [reliable|best_effort]")
        sys.exit(1)

    rclpy.init()
    node = QosSubscriber(profile_name)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
